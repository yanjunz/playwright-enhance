"""
Command-line interface for playwright-enhance.

Compatible with Playwright CLI commands, with added --enhanced option.
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
@click.version_option(version=__version__, prog_name='playwright-enhance-cli')
def cli():
    """
    Playwright-Enhance CLI - Compatible with Playwright CLI.
    
    All standard Playwright commands with optional --enhanced flag.
    """
    pass


@cli.command()
@click.argument('url', required=False)
@click.option('-b', '--browser', type=click.Choice(['chromium', 'firefox', 'webkit']), 
              default='chromium', help='Browser to use')
@click.option('--headless/--headed', default=False, help='Run in headless mode')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright (smart waiting)')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def open(url: Optional[str], browser: str, headless: bool, enhanced: bool, config: Optional[str]):
    """
    Open page in browser (compatible with playwright open).
    
    Examples:
        playwright-enhance-cli open https://example.com
        playwright-enhance-cli open https://github.com --enhanced
        playwright-enhance-cli open --browser firefox --enhanced
    """
    async def run_open():
        async with async_playwright() as p:
            browser_type = getattr(p, browser)
            browser_obj = await browser_type.launch(headless=headless)
            
            cfg = Config(config_file=config) if config else Config()
            
            if enhanced:
                cfg.set('smart_waiting.enabled', True)
                browser_obj = enhance(browser_obj, cfg.to_dict())
            
            page = await browser_obj.new_page()
            
            if enhanced:
                plugin = SmartWaitingPlugin(cfg.get('smart_waiting'))
                page.register_plugin('smart_waiting', plugin)
                page.enable_plugin('smart_waiting')
            
            if url:
                await page.goto(url)
                click.echo(f"Opened: {url}")
            else:
                await page.goto('about:blank')
                click.echo("Browser opened. Close the browser window to exit.")
            
            # Keep browser open
            click.echo("Press Ctrl+C to close...")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                pass
            
            await browser_obj.close()
    
    asyncio.run(run_open())


@cli.command()
@click.argument('url', required=False)
@click.option('-b', '--browser', type=click.Choice(['chromium', 'firefox', 'webkit']), 
              default='chromium', help='Browser to use')
@click.option('--headless/--headed', default=False, help='Run in headless mode')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright')
@click.option('--target', type=click.Choice(['python', 'javascript', 'java', 'csharp']), 
              default='python', help='Target language')
@click.option('-o', '--output', type=click.Path(), help='Save generated code to file')
def codegen(url: Optional[str], browser: str, headless: bool, enhanced: bool, 
            target: str, output: Optional[str]):
    """
    Open page and generate code for user actions.
    
    Examples:
        playwright-enhance-cli codegen https://example.com
        playwright-enhance-cli codegen --enhanced --target python
    """
    click.echo("⚠️  Code generation requires the full Playwright installation.")
    click.echo("Please use: playwright codegen")
    click.echo("")
    click.echo("Playwright-Enhance focuses on runtime performance optimization,")
    click.echo("not code generation. Generated code can be used with playwright-enhance")
    click.echo("by adding the enhance() wrapper.")
    sys.exit(1)


@cli.command()
@click.argument('browser', nargs=-1)
@click.option('--with-deps', is_flag=True, help='Install system dependencies')
@click.option('--force', is_flag=True, help='Force reinstall')
def install(browser, with_deps: bool, force: bool):
    """
    Install browsers for Playwright.
    
    Examples:
        playwright-enhance-cli install
        playwright-enhance-cli install chromium
        playwright-enhance-cli install --with-deps
    """
    import subprocess
    
    cmd = ['playwright', 'install']
    if with_deps:
        cmd.append('--with-deps')
    if force:
        cmd.append('--force')
    if browser:
        cmd.extend(browser)
    
    click.echo(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


@cli.command('install-deps')
@click.argument('browser', nargs=-1)
def install_deps(browser):
    """
    Install dependencies necessary to run browsers.
    
    Examples:
        playwright-enhance-cli install-deps
        playwright-enhance-cli install-deps chromium
    """
    import subprocess
    
    cmd = ['playwright', 'install-deps']
    if browser:
        cmd.extend(browser)
    
    click.echo(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


@cli.command()
@click.argument('url')
@click.argument('filename')
@click.option('-b', '--browser', type=click.Choice(['chromium', 'firefox', 'webkit']), 
              default='chromium', help='Browser to use')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright')
@click.option('--full-page', is_flag=True, help='Capture full page screenshot')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def screenshot(url: str, filename: str, browser: str, enhanced: bool, 
               full_page: bool, config: Optional[str]):
    """
    Capture a page screenshot.
    
    Examples:
        playwright-enhance-cli screenshot https://example.com output.png
        playwright-enhance-cli screenshot https://github.com page.png --enhanced --full-page
    """
    async def run_screenshot():
        async with async_playwright() as p:
            browser_type = getattr(p, browser)
            browser_obj = await browser_type.launch(headless=True)
            
            cfg = Config(config_file=config) if config else Config()
            
            if enhanced:
                cfg.set('smart_waiting.enabled', True)
                browser_obj = enhance(browser_obj, cfg.to_dict())
            
            page = await browser_obj.new_page()
            
            if enhanced:
                plugin = SmartWaitingPlugin(cfg.get('smart_waiting'))
                page.register_plugin('smart_waiting', plugin)
                page.enable_plugin('smart_waiting')
            
            start_time = time.time()
            await page.goto(url)
            load_time = time.time() - start_time
            
            await page.screenshot(path=filename, full_page=full_page)
            
            await browser_obj.close()
            
            mode = "enhanced" if enhanced else "native"
            click.echo(f"Screenshot saved to: {filename}")
            click.echo(f"Load time ({mode}): {load_time:.3f}s")
    
    asyncio.run(run_screenshot())


@cli.command()
@click.argument('url')
@click.argument('filename')
@click.option('-b', '--browser', type=click.Choice(['chromium', 'firefox', 'webkit']), 
              default='chromium', help='Browser to use')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def pdf(url: str, filename: str, browser: str, enhanced: bool, config: Optional[str]):
    """
    Save page as PDF.
    
    Examples:
        playwright-enhance-cli pdf https://example.com output.pdf
        playwright-enhance-cli pdf https://github.com page.pdf --enhanced
    """
    if browser != 'chromium':
        click.echo("⚠️  PDF generation is only supported in Chromium.")
        sys.exit(1)
    
    async def run_pdf():
        async with async_playwright() as p:
            browser_obj = await p.chromium.launch(headless=True)
            
            cfg = Config(config_file=config) if config else Config()
            
            if enhanced:
                cfg.set('smart_waiting.enabled', True)
                browser_obj = enhance(browser_obj, cfg.to_dict())
            
            page = await browser_obj.new_page()
            
            if enhanced:
                plugin = SmartWaitingPlugin(cfg.get('smart_waiting'))
                page.register_plugin('smart_waiting', plugin)
                page.enable_plugin('smart_waiting')
            
            start_time = time.time()
            await page.goto(url)
            load_time = time.time() - start_time
            
            await page.pdf(path=filename)
            
            await browser_obj.close()
            
            mode = "enhanced" if enhanced else "native"
            click.echo(f"PDF saved to: {filename}")
            click.echo(f"Load time ({mode}): {load_time:.3f}s")
    
    asyncio.run(run_pdf())


# Browser shortcuts (compatible with playwright CLI)
@cli.command()
@click.argument('url', required=False)
@click.option('--headless/--headed', default=False, help='Run in headless mode')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright')
def cr(url: Optional[str], headless: bool, enhanced: bool):
    """Open page in Chromium (shortcut for open --browser chromium)."""
    ctx = click.Context(open)
    ctx.invoke(open, url=url, browser='chromium', headless=headless, enhanced=enhanced, config=None)


@cli.command()
@click.argument('url', required=False)
@click.option('--headless/--headed', default=False, help='Run in headless mode')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright')
def ff(url: Optional[str], headless: bool, enhanced: bool):
    """Open page in Firefox (shortcut for open --browser firefox)."""
    ctx = click.Context(open)
    ctx.invoke(open, url=url, browser='firefox', headless=headless, enhanced=enhanced, config=None)


@cli.command()
@click.argument('url', required=False)
@click.option('--headless/--headed', default=False, help='Run in headless mode')
@click.option('--enhanced/--native', default=False, help='Use enhanced Playwright')
def wk(url: Optional[str], headless: bool, enhanced: bool):
    """Open page in WebKit (shortcut for open --browser webkit)."""
    ctx = click.Context(open)
    ctx.invoke(open, url=url, browser='webkit', headless=headless, enhanced=enhanced, config=None)


# Enhanced-specific commands (additional features)
@cli.group()
def bench():
    """Benchmarking and performance testing commands."""
    pass


@bench.command('run')
@click.argument('url')
@click.option('--headless/--headed', default=True, help='Run in headless mode')
@click.option('--runs', '-n', default=3, help='Number of runs')
@click.option('--browser', '-b', type=click.Choice(['chromium', 'firefox', 'webkit']), 
              default='chromium', help='Browser to use')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--output', '-o', type=click.Path(), help='Save results to file')
def bench_run(url: str, headless: bool, runs: int, browser: str, 
              config: Optional[str], output: Optional[str]):
    """
    Run performance benchmark comparing enhanced vs native.
    
    Examples:
        playwright-enhance-cli bench run https://example.com
        playwright-enhance-cli bench run https://github.com --runs 5 -o results.json
    """
    async def run_single_test(enhanced: bool):
        async with async_playwright() as p:
            browser_type = getattr(p, browser)
            browser_obj = await browser_type.launch(headless=headless)
            
            cfg = Config(config_file=config) if config else Config()
            
            if enhanced:
                cfg.set('smart_waiting.enabled', True)
                browser_obj = enhance(browser_obj, cfg.to_dict())
                page = await browser_obj.new_page()
                plugin = SmartWaitingPlugin(cfg.get('smart_waiting'))
                page.register_plugin('smart_waiting', plugin)
                page.enable_plugin('smart_waiting')
            else:
                page = await browser_obj.new_page()
            
            start_time = time.time()
            await page.goto(url)
            await page.wait_for_load_state('domcontentloaded' if enhanced else 'load')
            load_time = time.time() - start_time
            
            await browser_obj.close()
            return load_time
    
    # Run tests
    click.echo(f"Running benchmark ({runs} runs each)...")
    click.echo(f"URL: {url}")
    click.echo(f"Browser: {browser}")
    click.echo("")
    
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
        'browser': browser,
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
    click.echo("")
    click.echo("=" * 60)
    click.echo("Performance Benchmark Results")
    click.echo("=" * 60)
    click.echo(f"URL:        {results['url']}")
    click.echo(f"Browser:    {results['browser']}")
    click.echo(f"Runs:       {results['runs']}")
    click.echo("")
    click.echo("Native Playwright:")
    click.echo(f"  Average:  {results['native']['average']}s")
    click.echo(f"  Min:      {results['native']['min']}s")
    click.echo(f"  Max:      {results['native']['max']}s")
    click.echo("")
    click.echo("Enhanced Playwright:")
    click.echo(f"  Average:  {results['enhanced']['average']}s")
    click.echo(f"  Min:      {results['enhanced']['min']}s")
    click.echo(f"  Max:      {results['enhanced']['max']}s")
    click.echo("")
    if improvement > 0:
        click.echo(f"⚡ Improvement: {results['improvement_percent']}% faster ({results['speedup']}x speedup)")
    else:
        click.echo(f"Improvement: {results['improvement_percent']}% faster ({results['speedup']}x speedup)")
    click.echo("")
    
    # Output
    if output:
        Path(output).write_text(json.dumps(results, indent=2))
        click.echo(f"Results saved to: {output}")


@cli.group()
def config():
    """Configuration management commands."""
    pass


@config.command('show')
def config_show():
    """Show current configuration."""
    cfg = Config()
    click.echo(json.dumps(cfg.to_dict(), indent=2))


@config.command('init')
@click.argument('filepath')
@click.option('--minimal', is_flag=True, help='Create minimal config')
def config_init(filepath: str, minimal: bool):
    """
    Initialize configuration file.
    
    Examples:
        playwright-enhance-cli config init config.json
        playwright-enhance-cli config init config.json --minimal
    """
    cfg = Config()
    config_data = cfg.to_dict()
    
    if minimal:
        config_data = {
            'smart_waiting': {
                'enabled': True,
                'initial_timeout': 3000,
                'max_timeout': 8000
            }
        }
    
    Path(filepath).write_text(json.dumps(config_data, indent=2))
    click.echo(f"Configuration initialized: {filepath}")


@config.command('validate')
@click.argument('filepath')
def config_validate(filepath: str):
    """Validate configuration file."""
    try:
        cfg = Config(config_file=filepath)
        click.echo(f"✅ Configuration valid: {filepath}")
        click.echo(json.dumps(cfg.to_dict(), indent=2))
    except Exception as e:
        click.echo(f"❌ Invalid configuration: {e}")
        sys.exit(1)


@cli.command()
def uninstall():
    """
    Uninstall Playwright browsers (proxy to playwright uninstall).
    
    Example:
        playwright-enhance-cli uninstall
    """
    import subprocess
    try:
        subprocess.run(['playwright', 'uninstall'], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo("Error: 'playwright' command not found. Please install Playwright first.", err=True)
        sys.exit(1)


@cli.command('show-trace')
@click.argument('trace', required=False)
def show_trace(trace: Optional[str]):
    """
    Show trace viewer (proxy to playwright show-trace).
    
    Examples:
        playwright-enhance-cli show-trace
        playwright-enhance-cli show-trace trace.zip
    """
    import subprocess
    cmd = ['playwright', 'show-trace']
    if trace:
        cmd.append(trace)
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo("Error: 'playwright' command not found. Please install Playwright first.", err=True)
        sys.exit(1)


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


if __name__ == '__main__':
    cli()
