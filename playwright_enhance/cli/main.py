"""
Command-line interface for playwright-enhance.

Provides utilities for testing, benchmarking, configuration management, and more.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Optional

import click
from playwright.async_api import async_playwright

from playwright_enhance import enhance, Config, __version__
from playwright_enhance.capabilities.smart_waiting import SmartWaitingPlugin


@click.group()
@click.version_option(version=__version__, prog_name='playwright-enhance')
def cli():
    """
    Playwright-Enhance CLI - Performance-optimized browser automation.
    
    Provides tools for testing, benchmarking, and configuration management.
    """
    pass


@cli.command()
@click.argument('url')
@click.option('--headless/--no-headless', default=True, help='Run in headless mode')
@click.option('--enhanced/--native', default=True, help='Use enhanced or native Playwright')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--output', '-o', type=click.Path(), help='Save results to file')
@click.option('--format', type=click.Choice(['json', 'text']), default='text', help='Output format')
def benchmark(url: str, headless: bool, enhanced: bool, config: Optional[str], 
              output: Optional[str], format: str):
    """
    Benchmark page loading performance.
    
    Compare enhanced vs native Playwright performance on a given URL.
    
    Example:
        playwright-enhance-cli benchmark https://example.com
        playwright-enhance-cli benchmark https://github.com --no-headless
    """
    async def run_benchmark():
        results = {
            'url': url,
            'enhanced': enhanced,
            'headless': headless,
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            
            # Load config if provided
            cfg = Config(config_file=config) if config else Config()
            
            if enhanced:
                # Enable smart waiting
                cfg.set('smart_waiting.enabled', True)
                browser = enhance(browser, cfg.to_dict())
                
                page = await browser.new_page()
                
                # Register and enable smart waiting plugin
                plugin = SmartWaitingPlugin(cfg.get('smart_waiting'))
                page.register_plugin('smart_waiting', plugin)
                page.enable_plugin('smart_waiting')
            else:
                page = await browser.new_page()
            
            # Measure page load time
            start_time = time.time()
            await page.goto(url)
            await page.wait_for_load_state('domcontentloaded' if enhanced else 'load')
            load_time = time.time() - start_time
            
            results['load_time'] = round(load_time, 3)
            results['load_time_ms'] = round(load_time * 1000)
            
            # Get page title
            results['title'] = await page.title()
            
            await browser.close()
        
        return results
    
    # Run benchmark
    results = asyncio.run(run_benchmark())
    
    # Format output
    if format == 'json':
        output_text = json.dumps(results, indent=2)
    else:
        mode = "Enhanced" if enhanced else "Native"
        output_text = f"""
Benchmark Results
{'=' * 50}
URL:        {results['url']}
Mode:       {mode}
Headless:   {headless}
Title:      {results['title']}
Load Time:  {results['load_time']}s ({results['load_time_ms']}ms)
"""
    
    # Output
    if output:
        Path(output).write_text(output_text)
        click.echo(f"Results saved to: {output}")
    else:
        click.echo(output_text)


@cli.command()
@click.argument('url')
@click.option('--headless/--no-headless', default=True, help='Run in headless mode')
@click.option('--runs', '-n', default=3, help='Number of runs for each mode')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--output', '-o', type=click.Path(), help='Save results to file')
def compare(url: str, headless: bool, runs: int, config: Optional[str], output: Optional[str]):
    """
    Compare enhanced vs native performance.
    
    Run multiple tests to compare enhanced and native Playwright performance.
    
    Example:
        playwright-enhance-cli compare https://example.com --runs 5
    """
    async def run_single_test(enhanced: bool):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            
            cfg = Config(config_file=config) if config else Config()
            
            if enhanced:
                cfg.set('smart_waiting.enabled', True)
                browser = enhance(browser, cfg.to_dict())
                page = await browser.new_page()
                plugin = SmartWaitingPlugin(cfg.get('smart_waiting'))
                page.register_plugin('smart_waiting', plugin)
                page.enable_plugin('smart_waiting')
            else:
                page = await browser.new_page()
            
            start_time = time.time()
            await page.goto(url)
            await page.wait_for_load_state('domcontentloaded' if enhanced else 'load')
            load_time = time.time() - start_time
            
            await browser.close()
            return load_time
    
    # Run tests
    click.echo(f"Running comparison tests ({runs} runs each)...")
    
    native_times = []
    enhanced_times = []
    
    for i in range(runs):
        click.echo(f"  Run {i+1}/{runs} - Native...", nl=False)
        native_time = asyncio.run(run_single_test(enhanced=False))
        native_times.append(native_time)
        click.echo(f" {native_time:.3f}s")
        
        click.echo(f"  Run {i+1}/{runs} - Enhanced...", nl=False)
        enhanced_time = asyncio.run(run_single_test(enhanced=True))
        enhanced_times.append(enhanced_time)
        click.echo(f" {enhanced_time:.3f}s")
    
    # Calculate statistics
    native_avg = sum(native_times) / len(native_times)
    enhanced_avg = sum(enhanced_times) / len(enhanced_times)
    improvement = ((native_avg - enhanced_avg) / native_avg) * 100
    
    results = {
        'url': url,
        'runs': runs,
        'native': {
            'times': [round(t, 3) for t in native_times],
            'average': round(native_avg, 3),
            'min': round(min(native_times), 3),
            'max': round(max(native_times), 3),
        },
        'enhanced': {
            'times': [round(t, 3) for t in enhanced_times],
            'average': round(enhanced_avg, 3),
            'min': round(min(enhanced_times), 3),
            'max': round(max(enhanced_times), 3),
        },
        'improvement_percent': round(improvement, 1),
        'speedup': round(native_avg / enhanced_avg, 2),
    }
    
    # Format output
    output_text = f"""
Performance Comparison
{'=' * 60}
URL:        {url}
Runs:       {runs}

Native Playwright:
  Average:  {results['native']['average']}s
  Min:      {results['native']['min']}s
  Max:      {results['native']['max']}s

Enhanced Playwright:
  Average:  {results['enhanced']['average']}s
  Min:      {results['enhanced']['min']}s
  Max:      {results['enhanced']['max']}s

Improvement: {results['improvement_percent']}% faster ({results['speedup']}x speedup)
"""
    
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        click.echo(output_text)
        click.echo(f"\nDetailed results saved to: {output}")
    else:
        click.echo(output_text)


@cli.group()
def config_cmd():
    """Configuration management commands."""
    pass


@config_cmd.command('show')
@click.option('--file', '-f', type=click.Path(exists=True), help='Config file to show')
def config_show(file: Optional[str]):
    """
    Show current configuration.
    
    Example:
        playwright-enhance-cli config show
        playwright-enhance-cli config show --file config.json
    """
    cfg = Config(config_file=file) if file else Config()
    click.echo(json.dumps(cfg.to_dict(), indent=2))


@config_cmd.command('init')
@click.argument('output', type=click.Path())
@click.option('--minimal', is_flag=True, help='Generate minimal config')
def config_init(output: str, minimal: bool):
    """
    Initialize a new configuration file.
    
    Example:
        playwright-enhance-cli config init config.json
        playwright-enhance-cli config init config.json --minimal
    """
    if minimal:
        config = {
            'smart_waiting': {
                'enabled': True,
                'initial_timeout': 5000,
                'max_timeout': 10000,
            }
        }
    else:
        cfg = Config()
        config = cfg.to_dict()
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    click.echo(f"Configuration file created: {output}")


@config_cmd.command('validate')
@click.argument('file', type=click.Path(exists=True))
def config_validate(file: str):
    """
    Validate a configuration file.
    
    Example:
        playwright-enhance-cli config validate config.json
    """
    try:
        cfg = Config(config_file=file)
        click.echo(f"✓ Configuration file is valid: {file}")
        click.echo(f"\nLoaded configuration:")
        click.echo(json.dumps(cfg.to_dict(), indent=2))
    except Exception as e:
        click.echo(f"✗ Configuration file is invalid: {file}", err=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('script', type=click.Path(exists=True))
@click.option('--headless/--no-headless', default=True, help='Run in headless mode')
@click.option('--enhanced/--native', default=True, help='Use enhanced or native Playwright')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def run(script: str, headless: bool, enhanced: bool, config: Optional[str]):
    """
    Run a Playwright test script.
    
    Example:
        playwright-enhance-cli run test.py
        playwright-enhance-cli run test.py --no-headless --native
    """
    # Set environment variables
    import os
    os.environ['PLAYWRIGHT_ENHANCE_ENABLED'] = str(enhanced)
    os.environ['PLAYWRIGHT_HEADLESS'] = str(headless)
    if config:
        os.environ['PLAYWRIGHT_ENHANCE_CONFIG'] = config
    
    # Run the script
    import subprocess
    result = subprocess.run([sys.executable, script], check=False)
    sys.exit(result.returncode)


@cli.command()
def info():
    """
    Show system and installation information.
    
    Example:
        playwright-enhance-cli info
    """
    import platform
    try:
        from playwright import __version__ as pw_version
    except ImportError:
        pw_version = "not installed"
    
    info_text = f"""
Playwright-Enhance Information
{'=' * 50}
Version:        {__version__}
Python:         {platform.python_version()}
Platform:       {platform.system()} {platform.release()}
Playwright:     {pw_version}

Installation:
  Package:      playwright-enhance
  CLI Command:  playwright-enhance-cli

Features:
  ✓ Smart Waiting (adaptive timeouts)
  ✓ Core Architecture (plugin system)
  ⚠ Multi-Locator (coming soon)
  ⚠ Concurrent Engine (coming soon)
  ⚠ Cache System (coming soon)

Documentation:  https://github.com/playwright-enhance/playwright-enhance
"""
    click.echo(info_text)


@cli.command()
@click.option('--port', '-p', default=8080, help='Server port')
@click.option('--host', '-h', default='127.0.0.1', help='Server host')
def demo(port: int, host: str):
    """
    Start an interactive demo server.
    
    Example:
        playwright-enhance-cli demo
        playwright-enhance-cli demo --port 3000
    """
    click.echo(f"Starting demo server on http://{host}:{port}")
    click.echo("Press Ctrl+C to stop")
    click.echo("\nFeature: Interactive demo server coming soon!")
    click.echo("For now, try running example scripts:")
    click.echo("  python examples/real_wikipedia_test.py --visible")


if __name__ == '__main__':
    cli()
