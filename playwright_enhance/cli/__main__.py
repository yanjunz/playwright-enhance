"""
Entry point for running CLI as a module.
Allows running with: python -m playwright_enhance.cli
"""
from playwright_enhance.cli.main import cli

if __name__ == '__main__':
    cli()
