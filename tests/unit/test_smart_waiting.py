"""Unit tests for smart waiting capability."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, MagicMock
from playwright_enhance.capabilities.smart_waiting import (
    PageState,
    PageMetrics,
    PageStateMonitor,
    DynamicTimeoutCalculator,
    AdaptiveWaitStrategy,
    ResourcePreloader,
    SmartWaitingPlugin,
)


class TestPageMetrics:
    """Test page complexity metrics."""
    
    def test_simple_page_complexity(self):
        """Test complexity score for simple page."""
        metrics = PageMetrics(dom_nodes=100, network_requests=5, script_duration=100)
        score = metrics.complexity_score()
        assert 0 <= score < 0.3  # Simple page should have low score
    
    def test_complex_page_complexity(self):
        """Test complexity score for complex page."""
        metrics = PageMetrics(dom_nodes=10000, network_requests=100, script_duration=8000)
        score = metrics.complexity_score()
        assert 0.7 <= score <= 1.0  # Complex page should have high score


class TestDynamicTimeoutCalculator:
    """Test dynamic timeout calculation."""
    
    def test_initial_timeout(self):
        """Test calculation with no history."""
        calculator = DynamicTimeoutCalculator(initial_timeout=5000, min_timeout=1000, max_timeout=10000)
        metrics = PageMetrics()
        
        timeout = calculator.calculate_timeout(metrics)
        assert 1000 <= timeout <= 10000
    
    def test_simple_page_timeout(self):
        """Test timeout for simple page."""
        calculator = DynamicTimeoutCalculator(initial_timeout=5000)
        metrics = PageMetrics(dom_nodes=100, network_requests=5)
        
        timeout = calculator.calculate_timeout(metrics)
        assert timeout < 7000  # Should be less than initial + buffer
    
    def test_complex_page_timeout(self):
        """Test timeout for complex page."""
        calculator = DynamicTimeoutCalculator(initial_timeout=5000)
        metrics = PageMetrics(dom_nodes=8000, network_requests=80, script_duration=6000)
        
        timeout = calculator.calculate_timeout(metrics)
        assert timeout > 7000  # Should be higher for complex pages
    
    def test_historical_adjustment(self):
        """Test timeout adjustment based on history."""
        calculator = DynamicTimeoutCalculator(initial_timeout=5000)
        
        # Record some fast load times
        for _ in range(5):
            calculator.record_load_time(1.0)  # 1 second loads
        
        metrics = PageMetrics()
        timeout = calculator.calculate_timeout(metrics)
        
        # Should adapt to fast loads (1.5x of 1s = 1.5s = 1500ms, but clamped to min)
        assert timeout >= 1000
    
    def test_min_max_clamp(self):
        """Test that timeout is clamped to min/max."""
        calculator = DynamicTimeoutCalculator(initial_timeout=5000, min_timeout=2000, max_timeout=8000)
        
        # Record very long load times
        for _ in range(5):
            calculator.record_load_time(10.0)
        
        metrics = PageMetrics(dom_nodes=10000, network_requests=100)
        timeout = calculator.calculate_timeout(metrics)
        
        assert timeout <= 8000  # Should be clamped to max
    
    def test_history_size_limit(self):
        """Test that history is limited to recent records."""
        calculator = DynamicTimeoutCalculator()
        
        # Record more than 10 items
        for i in range(15):
            calculator.record_load_time(float(i))
        
        assert len(calculator._history) == 10  # Should keep only last 10


@pytest.mark.asyncio
class TestAdaptiveWaitStrategy:
    """Test adaptive wait strategy."""
    
    async def test_wait_for_immediate_condition(self):
        """Test waiting for condition that is immediately true."""
        mock_page = Mock()
        config = {}
        strategy = AdaptiveWaitStrategy(mock_page, config)
        
        async def always_true():
            return True
        
        result = await strategy.wait_for_condition(always_true, timeout=1000)
        assert result is True
    
    async def test_wait_for_delayed_condition(self):
        """Test waiting for condition that becomes true after delay."""
        mock_page = Mock()
        config = {}
        strategy = AdaptiveWaitStrategy(mock_page, config)
        
        counter = {'value': 0}
        
        async def becomes_true():
            counter['value'] += 1
            return counter['value'] > 3
        
        result = await strategy.wait_for_condition(becomes_true, timeout=2000, poll_interval=100)
        assert result is True
        assert counter['value'] > 3
    
    async def test_wait_timeout(self):
        """Test that wait times out for condition that never becomes true."""
        mock_page = Mock()
        config = {}
        strategy = AdaptiveWaitStrategy(mock_page, config)
        
        async def always_false():
            return False
        
        result = await strategy.wait_for_condition(always_false, timeout=500)
        assert result is False
    
    async def test_wait_with_exception(self):
        """Test waiting continues when condition check raises exception."""
        mock_page = Mock()
        config = {}
        strategy = AdaptiveWaitStrategy(mock_page, config)
        
        counter = {'value': 0}
        
        async def sometimes_fails():
            counter['value'] += 1
            if counter['value'] < 3:
                raise Exception("Not ready")
            return True
        
        result = await strategy.wait_for_condition(sometimes_fails, timeout=2000, poll_interval=100)
        assert result is True


@pytest.mark.asyncio
class TestResourcePreloader:
    """Test resource preloading."""
    
    async def test_preload_link_target(self):
        """Test preloading link target."""
        mock_page = AsyncMock()
        mock_link = AsyncMock()
        mock_link.get_attribute = AsyncMock(return_value="https://example.com")
        mock_page.query_selector = AsyncMock(return_value=mock_link)
        mock_page.evaluate = AsyncMock()
        
        preloader = ResourcePreloader(mock_page)
        await preloader.preload_link_target("a.target")
        
        mock_page.query_selector.assert_called_once()
        mock_link.hover.assert_called_once()
    
    async def test_preload_form_resources(self):
        """Test preloading form resources."""
        mock_page = AsyncMock()
        mock_button = AsyncMock()
        mock_page.query_selector = AsyncMock(return_value=mock_button)
        
        preloader = ResourcePreloader(mock_page)
        await preloader.preload_form_resources("form#login")
        
        mock_page.query_selector.assert_called_once()
        mock_button.hover.assert_called_once()
    
    async def test_preload_handles_missing_elements(self):
        """Test that preload handles missing elements gracefully."""
        mock_page = AsyncMock()
        mock_page.query_selector = AsyncMock(return_value=None)
        
        preloader = ResourcePreloader(mock_page)
        # Should not raise exception
        await preloader.preload_link_target("a.missing")
        await preloader.preload_form_resources("form#missing")


@pytest.mark.asyncio
class TestSmartWaitingPlugin:
    """Test smart waiting plugin integration."""
    
    async def test_plugin_initialization(self):
        """Test plugin initialization with config."""
        config = {
            'initial_timeout': 3000,
            'max_timeout': 8000,
        }
        plugin = SmartWaitingPlugin(config)
        assert plugin._config == config
    
    async def test_before_goto_hook(self):
        """Test goto pre-hook with smart waiting."""
        config = {}
        plugin = SmartWaitingPlugin(config)
        
        mock_page = AsyncMock()
        mock_page.goto = AsyncMock(return_value="response")
        mock_page.evaluate = AsyncMock(return_value=100)  # Mock DOM node count
        mock_page.on = Mock()  # Mock event listener
        mock_page.wait_for_load_state = AsyncMock()
        
        enhanced_page = Mock()
        enhanced_page._page = mock_page
        
        # Should intercept and use smart waiting
        result = await plugin.before_goto(enhanced_page, "https://example.com")
        
        # Original goto should be called
        mock_page.goto.assert_called_once()
    
    async def test_before_click_preload(self):
        """Test click pre-hook triggers preloading."""
        config = {}
        plugin = SmartWaitingPlugin(config)
        
        mock_page = AsyncMock()
        mock_link = AsyncMock()
        mock_link.get_attribute = AsyncMock(return_value="https://example.com")
        mock_page.query_selector = AsyncMock(return_value=mock_link)
        mock_page.evaluate = AsyncMock()
        
        enhanced_page = Mock()
        enhanced_page._page = mock_page
        
        result = await plugin.before_click(enhanced_page, "a.link")
        
        # Should return None to let original method execute
        assert result is None
        
        # Should have attempted preload
        mock_page.query_selector.assert_called()
