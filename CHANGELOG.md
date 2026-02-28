# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Node.js/TypeScript support (v0.2.0)
- Java support (v0.3.0)
- .NET support (v0.4.0)

---

## [0.1.0] - 2024-02-28

### Added

#### Core Features
- **Smart Waiting Strategies** - Adaptive timeouts based on page complexity
  - Dynamic timeout calculation (3-8s instead of fixed 30s)
  - Intelligent wait states (`domcontentloaded` vs `load`)
  - Element visibility detection with retry logic
- **Performance Optimization** - 40-50% faster page loads
  - `domcontentloaded` wait strategy by default
  - Resource hints and preloading
  - Parallel operation execution
- **100% Playwright API Compatibility** - Drop-in replacement
  - `enhance()` function wraps existing Playwright objects
  - All original methods preserved
  - Backward compatible with existing scripts

#### CLI Tool
- `playwright-enhance-cli` command-line interface
  - `screenshot` - Capture page screenshots with enhanced mode
  - `pdf` - Generate PDF from web pages
  - `open` - Open pages in browser with enhanced mode
  - `bench` - Performance benchmarking tool
- Compatible with Playwright CLI commands
- Optional `--enhanced` flag for performance mode

#### Configuration System
- YAML-based configuration (`playwright-enhance.yml`)
- Flexible per-operation config override
- Presets: `default`, `aggressive`, `conservative`, `ai-agent`

#### Documentation
- Comprehensive README with examples
- API Reference for Python (`docs/api-reference.md`)
- CLI Guide (`docs/cli-guide.md`)
- Performance Guide with real-world benchmarks (`docs/performance.md`)
- Comparison Guide (`docs/comparison-guide.md`)
- Distribution Guide (`docs/distribution-guide.md`)

#### Examples
- Real-world test scripts (Wikipedia, GitHub, Hacker News, Bilibili)
- Performance comparison demos
- Async/sync API usage examples

#### Testing
- 56 passing tests with 83% coverage
- Unit tests for core wrapper functionality
- Integration tests with real websites
- Performance benchmark tests

### Technical Details

#### Dependencies
- Python 3.8+
- playwright >= 1.40.0
- opencv-python-headless >= 4.8.0
- pyyaml >= 6.0
- click >= 8.1.0

#### Supported Platforms
- Linux (Ubuntu 20.04+)
- macOS (12.0+)
- Windows (10+)

#### Browser Support
- Chromium (primary)
- Firefox (compatible)
- WebKit (compatible)

---

## Versioning Strategy

- **0.x.x** - Alpha releases (Python only)
- **0.2.x** - Beta with Node.js support
- **1.0.0** - First stable release
- **1.x.x** - Stable with backward compatibility
- **2.0.0+** - Major versions with breaking changes

---

## Links

- [GitHub Repository](https://github.com/yanjunz/playwright-enhance)
- [Issue Tracker](https://github.com/yanjunz/playwright-enhance/issues)
- [Documentation](https://github.com/yanjunz/playwright-enhance/blob/master/docs/)
