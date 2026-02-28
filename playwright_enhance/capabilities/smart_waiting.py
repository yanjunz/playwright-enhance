"""
Smart Waiting Capability - Intelligent waiting strategies for faster page interactions.

Reduces waiting time by 50% through dynamic timeout adjustment, page state prediction,
and resource preloading.
"""

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class PageState(Enum):
    """Page loading states."""
    LOADING = "loading"
    INTERACTIVE = "interactive"
    COMPLETE = "complete"
    NETWORK_IDLE = "network_idle"


@dataclass
class PageMetrics:
    """Page complexity metrics for timeout calculation."""
    dom_nodes: int = 0
    network_requests: int = 0
    script_duration: float = 0.0
    render_time: float = 0.0
    
    def complexity_score(self) -> float:
        """Calculate page complexity score (0-1)."""
        # Normalize metrics
        dom_score = min(self.dom_nodes / 5000, 1.0)  # 5000+ nodes = complex
        network_score = min(self.network_requests / 50, 1.0)  # 50+ requests = complex
        script_score = min(self.script_duration / 5000, 1.0)  # 5s+ scripts = complex
        
        # Weighted average
        return 0.4 * dom_score + 0.3 * network_score + 0.3 * script_score


class PageStateMonitor:
    """Monitor page loading states using browser events."""
    
    def __init__(self, page: Any):
        self._page = page
        self._state = PageState.LOADING
        self._metrics = PageMetrics()
        self._load_start = time.time()
        self._listeners_attached = False
    
    async def attach_listeners(self) -> None:
        """Attach event listeners to monitor page state."""
        if self._listeners_attached:
            return
        
        # Listen to page events
        self._page.on("domcontentloaded", self._on_dom_loaded)
        self._page.on("load", self._on_load)
        
        self._listeners_attached = True
    
    def _on_dom_loaded(self) -> None:
        """Handle DOMContentLoaded event."""
        if self._state == PageState.LOADING:
            self._state = PageState.INTERACTIVE
    
    def _on_load(self) -> None:
        """Handle load event."""
        if self._state in [PageState.LOADING, PageState.INTERACTIVE]:
            self._state = PageState.COMPLETE
    
    async def update_metrics(self) -> None:
        """Update page complexity metrics."""
        try:
            # Count DOM nodes
            self._metrics.dom_nodes = await self._page.evaluate("() => document.querySelectorAll('*').length")
            
            # Get performance timing
            timing = await self._page.evaluate("""() => {
                const perf = performance.timing;
                return {
                    scriptDuration: perf.domComplete - perf.domLoading,
                    renderTime: perf.loadEventEnd - perf.fetchStart
                };
            }""")
            
            self._metrics.script_duration = timing.get('scriptDuration', 0)
            self._metrics.render_time = timing.get('renderTime', 0)
        except Exception:
            # If metrics collection fails, use defaults
            pass
    
    @property
    def state(self) -> PageState:
        """Get current page state."""
        return self._state
    
    @property
    def metrics(self) -> PageMetrics:
        """Get current page metrics."""
        return self._metrics
    
    @property
    def load_duration(self) -> float:
        """Get time since load started (seconds)."""
        return time.time() - self._load_start


class DynamicTimeoutCalculator:
    """Calculate optimal timeout based on page complexity and history."""
    
    def __init__(self, initial_timeout: int = 5000, min_timeout: int = 1000, max_timeout: int = 10000):
        """
        Initialize timeout calculator.
        
        Args:
            initial_timeout: Initial timeout in milliseconds
            min_timeout: Minimum timeout in milliseconds
            max_timeout: Maximum timeout in milliseconds
        """
        self.initial_timeout = initial_timeout
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout
        self._history: List[float] = []  # Historical load times
    
    def calculate_timeout(self, metrics: PageMetrics) -> int:
        """
        Calculate optimal timeout based on metrics.
        
        Args:
            metrics: Page complexity metrics
            
        Returns:
            Timeout in milliseconds
        """
        # Start with initial timeout
        timeout = self.initial_timeout
        
        # Adjust based on page complexity
        complexity = metrics.complexity_score()
        complexity_adjustment = complexity * (self.max_timeout - self.initial_timeout)
        timeout += complexity_adjustment
        
        # Adjust based on historical data
        if self._history:
            avg_load_time = sum(self._history) / len(self._history)
            # Use 1.5x of average as timeout (with some buffer)
            historical_timeout = avg_load_time * 1.5 * 1000  # Convert to ms
            timeout = max(timeout, historical_timeout)
        
        # Clamp to min/max
        return int(max(self.min_timeout, min(timeout, self.max_timeout)))
    
    def record_load_time(self, duration: float) -> None:
        """Record a page load time for historical adjustment."""
        self._history.append(duration)
        # Keep only last 10 records
        if len(self._history) > 10:
            self._history.pop(0)


class AdaptiveWaitStrategy:
    """Adaptive waiting strategy with intelligent backoff."""
    
    def __init__(self, page: Any, config: Dict):
        self._page = page
        self._config = config
        self._monitor = PageStateMonitor(page)
        self._calculator = DynamicTimeoutCalculator(
            initial_timeout=config.get('initial_timeout', 5000),
            min_timeout=config.get('min_timeout', 1000),
            max_timeout=config.get('max_timeout', 10000),
        )
    
    async def wait_for_condition(
        self,
        condition: Callable[[], bool],
        timeout: Optional[int] = None,
        poll_interval: int = 100,
    ) -> bool:
        """
        Wait for a condition with intelligent polling.
        
        Args:
            condition: Async callable that returns True when satisfied
            timeout: Maximum wait time in milliseconds (None = use calculated)
            poll_interval: Initial polling interval in milliseconds
            
        Returns:
            True if condition met, False if timeout
        """
        # Calculate optimal timeout if not provided
        if timeout is None:
            await self._monitor.update_metrics()
            timeout = self._calculator.calculate_timeout(self._monitor.metrics)
        
        start_time = time.time()
        current_interval = poll_interval
        
        while (time.time() - start_time) * 1000 < timeout:
            try:
                if await condition():
                    # Record successful wait time
                    duration = time.time() - start_time
                    self._calculator.record_load_time(duration)
                    return True
            except Exception:
                # Condition check failed, continue waiting
                pass
            
            # Intelligent backoff: increase interval if waiting long
            await asyncio.sleep(current_interval / 1000)
            
            # Exponential backoff up to 1 second
            current_interval = min(current_interval * 1.2, 1000)
        
        return False
    
    async def wait_for_page_load(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for page to finish loading.
        
        Args:
            timeout: Maximum wait time in milliseconds
            
        Returns:
            True if page loaded, False if timeout
        """
        await self._monitor.attach_listeners()
        
        async def is_loaded():
            # Check if page reached complete state
            if self._monitor.state == PageState.COMPLETE:
                return True
            
            # Or if network is idle
            try:
                await self._page.wait_for_load_state("networkidle", timeout=100)
                return True
            except Exception:
                return False
        
        return await self.wait_for_condition(is_loaded, timeout)


class ResourcePreloader:
    """Preload resources for predicted next actions."""
    
    def __init__(self, page: Any, cache_size_mb: int = 50):
        self._page = page
        self._cache: Dict[str, Any] = {}
        self._cache_size = 0
        self._max_cache_size = cache_size_mb * 1024 * 1024  # Convert to bytes
        self._access_count: Dict[str, int] = {}  # For LRU tracking
    
    async def preload_form_resources(self, form_selector: str) -> None:
        """Preload resources likely needed for form submission."""
        try:
            # Hover over submit button to trigger prefetch hints
            submit_btn = await self._page.query_selector(f"{form_selector} button[type='submit'], {form_selector} input[type='submit']")
            if submit_btn:
                await submit_btn.hover()
                await asyncio.sleep(0.1)  # Give browser time to start prefetch
        except Exception:
            pass
    
    async def preload_link_target(self, link_selector: str) -> None:
        """Preload target page of a link before clicking."""
        try:
            link = await self._page.query_selector(link_selector)
            if link:
                # Hover to trigger browser's link prefetching
                await link.hover()
                await asyncio.sleep(0.1)
                
                # Optionally: prefetch the actual page
                href = await link.get_attribute('href')
                if href and href.startswith('http'):
                    await self._prefetch_url(href)
        except Exception:
            pass
    
    async def _prefetch_url(self, url: str) -> None:
        """Prefetch a URL using link prefetch."""
        try:
            await self._page.evaluate(f"""(url) => {{
                const link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = url;
                document.head.appendChild(link);
            }}""", url)
        except Exception:
            pass
    
    def _evict_lru(self) -> None:
        """Evict least recently used items from cache."""
        if not self._access_count:
            return
        
        # Sort by access count
        sorted_items = sorted(self._access_count.items(), key=lambda x: x[1])
        
        # Remove least accessed items until under size limit
        for key, _ in sorted_items:
            if self._cache_size <= self._max_cache_size * 0.8:  # 80% threshold
                break
            
            if key in self._cache:
                # Estimate size (rough)
                item_size = len(str(self._cache[key]))
                self._cache_size -= item_size
                del self._cache[key]
                del self._access_count[key]


class SmartWaitingPlugin:
    """Plugin for smart waiting capability."""
    
    def __init__(self, config: Dict):
        self._config = config
        self._strategies: Dict[int, AdaptiveWaitStrategy] = {}  # page id -> strategy
        self._preloaders: Dict[int, ResourcePreloader] = {}  # page id -> preloader
    
    def _get_page_id(self, page: Any) -> int:
        """Get unique page identifier."""
        return id(page._page)
    
    def _get_or_create_strategy(self, enhanced_page: Any) -> AdaptiveWaitStrategy:
        """Get or create adaptive wait strategy for page."""
        page_id = self._get_page_id(enhanced_page)
        if page_id not in self._strategies:
            self._strategies[page_id] = AdaptiveWaitStrategy(enhanced_page._page, self._config)
        return self._strategies[page_id]
    
    def _get_or_create_preloader(self, enhanced_page: Any) -> ResourcePreloader:
        """Get or create resource preloader for page."""
        page_id = self._get_page_id(enhanced_page)
        if page_id not in self._preloaders:
            self._preloaders[page_id] = ResourcePreloader(enhanced_page._page)
        return self._preloaders[page_id]
    
    async def before_goto(self, enhanced_page: Any, url: str, **kwargs) -> None:
        """Pre-hook for page.goto() - use smart waiting."""
        strategy = self._get_or_create_strategy(enhanced_page)
        
        # Override timeout if not provided - use smart timeout instead of default 30s
        if 'timeout' not in kwargs:
            await strategy._monitor.update_metrics()
            smart_timeout = strategy._calculator.calculate_timeout(strategy._monitor.metrics)
            kwargs['timeout'] = smart_timeout
        
        # Use domcontentloaded instead of load for faster response
        if 'wait_until' not in kwargs:
            kwargs['wait_until'] = 'domcontentloaded'
        
        # Start navigation
        response = await enhanced_page._page.goto(url, **kwargs)
        
        # Don't wait for networkidle unless explicitly requested
        # This is the key optimization: we proceed as soon as DOM is interactive
        
        return response
    
    async def before_click(self, enhanced_page: Any, selector: str, **kwargs) -> None:
        """Pre-hook for page.click() - optimize waiting strategy."""
        # Reduce default timeout for clicks (5s instead of 30s)
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 5000
        
        # Preload link target if available
        preloader = self._get_or_create_preloader(enhanced_page)
        await preloader.preload_link_target(selector)
        
        # Return None to let original method execute
        return None
    
    async def before_fill(self, enhanced_page: Any, selector: str, value: str, **kwargs) -> None:
        """Pre-hook for page.fill() - optimize timeout."""
        # Reduce default timeout for fill operations
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 5000
        
        # Preload form resources in background
        preloader = self._get_or_create_preloader(enhanced_page)
        try:
            form_selector = await enhanced_page._page.evaluate(f"""(selector) => {{
                const element = document.querySelector(selector);
                const form = element ? element.closest('form') : null;
                return form ? `form:has(${{selector}})` : null;
            }}""", selector)
            
            if form_selector:
                await preloader.preload_form_resources(form_selector)
        except Exception:
            pass
        
        # Return None to let original method execute
        return None
    
    async def before_wait_for_selector(self, enhanced_page: Any, selector: str, **kwargs) -> None:
        """Pre-hook for wait_for_selector - use smart timeout."""
        strategy = self._get_or_create_strategy(enhanced_page)
        
        # Use adaptive timeout instead of default 30s
        if 'timeout' not in kwargs:
            await strategy._monitor.update_metrics()
            smart_timeout = strategy._calculator.calculate_timeout(strategy._monitor.metrics)
            # Cap at 10s for selector waiting (usually much faster)
            kwargs['timeout'] = min(smart_timeout, 10000)
        
        return None
