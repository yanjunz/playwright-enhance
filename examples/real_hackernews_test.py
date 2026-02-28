"""
Hacker News 真实测试对比
=======================

场景：在 Hacker News 上浏览新闻
- 浏览首页文章
- 查看评论
- 切换分类（new, top, best）
- 查看用户信息

这是一个轻量级、快速的真实测试。
"""

import asyncio
import time
import argparse
from playwright.async_api import async_playwright
from playwright_enhance import enhance


async def native_hackernews_test(headless=False):
    """原生 Playwright - Hacker News 测试"""
    print("\n🔵 原生 Playwright - Hacker News 测试")
    print("=" * 60)
    
    start = time.time()
    steps = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        
        try:
            # 1. 打开 Hacker News 首页
            step_start = time.time()
            await page.goto('https://news.ycombinator.com', wait_until='load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开首页", time.time() - step_start))
            print(f"  1. 打开首页: {steps[-1][1]:.2f}s")
            
            # 2. 统计首页文章数
            step_start = time.time()
            await page.wait_for_selector('.athing', timeout=30000)
            articles = await page.locator('.athing').count()
            steps.append(("加载文章", time.time() - step_start))
            print(f"  2. 加载文章 ({articles} 篇): {steps[-1][1]:.2f}s")
            
            # 3. 点击第一篇文章的评论
            step_start = time.time()
            await page.locator('text=comments').first.click()
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开评论", time.time() - step_start))
            print(f"  3. 打开评论: {steps[-1][1]:.2f}s")
            
            # 4. 统计评论数
            step_start = time.time()
            await page.wait_for_selector('.comment', timeout=30000)
            comments = await page.locator('.comment').count()
            steps.append(("加载评论", time.time() - step_start))
            print(f"  4. 加载评论 ({comments} 条): {steps[-1][1]:.2f}s")
            
            # 5. 返回首页
            step_start = time.time()
            await page.goto('https://news.ycombinator.com')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("返回首页", time.time() - step_start))
            print(f"  5. 返回首页: {steps[-1][1]:.2f}s")
            
            # 6. 访问 "newest" 页面
            step_start = time.time()
            await page.goto('https://news.ycombinator.com/newest')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看新闻", time.time() - step_start))
            print(f"  6. 查看新闻: {steps[-1][1]:.2f}s")
            
            # 7. 访问 "best" 页面
            step_start = time.time()
            await page.goto('https://news.ycombinator.com/best')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("最佳文章", time.time() - step_start))
            print(f"  7. 最佳文章: {steps[-1][1]:.2f}s")
            
            # 8. 点击第一个用户名
            step_start = time.time()
            await page.locator('.hnuser').first.click()
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("用户信息", time.time() - step_start))
            print(f"  8. 用户信息: {steps[-1][1]:.2f}s")
            
            # 9. 查看用户提交的文章
            step_start = time.time()
            await page.wait_for_selector('.athing', timeout=30000)
            user_articles = await page.locator('.athing').count()
            steps.append(("用户文章", time.time() - step_start))
            print(f"  9. 用户文章 ({user_articles} 篇): {steps[-1][1]:.2f}s")
            
            # 10. 返回首页
            step_start = time.time()
            await page.goto('https://news.ycombinator.com')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("返回首页", time.time() - step_start))
            print(f"  10. 返回首页: {steps[-1][1]:.2f}s")
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
        
        await browser.close()
    
    total = time.time() - start
    print(f"\n  总耗时: {total:.2f}s")
    print(f"  配置: 默认超时(30s), 等待load+networkidle")
    return total, steps


async def enhanced_hackernews_test(headless=False):
    """Playwright-Enhance - Hacker News 测试"""
    print("\n🟢 Playwright-Enhance - Hacker News 测试")
    print("=" * 60)
    
    start = time.time()
    steps = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        
        # 配置智能等待
        config = {
            'smart_waiting': {
                'enabled': True,
                'initial_timeout': 3000,
                'max_timeout': 8000,
            }
        }
        
        enhanced = enhance(browser, config)
        page = await enhanced.new_page()
        
        # 启用智能等待插件
        from playwright_enhance.capabilities import SmartWaitingPlugin
        plugin = SmartWaitingPlugin(config['smart_waiting'])
        page.register_plugin('smart_waiting', plugin)
        page.enable_plugin('smart_waiting')
        
        try:
            # 1. 打开 Hacker News 首页（智能优化）
            step_start = time.time()
            await page.goto('https://news.ycombinator.com')
            steps.append(("打开首页", time.time() - step_start))
            print(f"  1. 打开首页（domcontentloaded）: {steps[-1][1]:.2f}s")
            
            # 2. 统计首页文章数（智能等待）
            step_start = time.time()
            await page.wait_for_selector('.athing')
            articles = await page.locator('.athing').count()
            steps.append(("加载文章", time.time() - step_start))
            print(f"  2. 加载文章 ({articles} 篇): {steps[-1][1]:.2f}s")
            
            # 3. 点击第一篇文章的评论（快速响应）
            step_start = time.time()
            await page.locator('text=comments').first.click()
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("打开评论", time.time() - step_start))
            print(f"  3. 打开评论（优化）: {steps[-1][1]:.2f}s")
            
            # 4. 统计评论数（智能超时）
            step_start = time.time()
            await page.wait_for_selector('.comment')
            comments = await page.locator('.comment').count()
            steps.append(("加载评论", time.time() - step_start))
            print(f"  4. 加载评论 ({comments} 条): {steps[-1][1]:.2f}s")
            
            # 5. 返回首页（快速加载）
            step_start = time.time()
            await page.goto('https://news.ycombinator.com')
            steps.append(("返回首页", time.time() - step_start))
            print(f"  5. 返回首页（domcontentloaded）: {steps[-1][1]:.2f}s")
            
            # 6. 访问 "newest" 页面（智能等待）
            step_start = time.time()
            await page.goto('https://news.ycombinator.com/newest')
            steps.append(("查看新闻", time.time() - step_start))
            print(f"  6. 查看新闻（快速）: {steps[-1][1]:.2f}s")
            
            # 7. 访问 "best" 页面（优化加载）
            step_start = time.time()
            await page.goto('https://news.ycombinator.com/best')
            steps.append(("最佳文章", time.time() - step_start))
            print(f"  7. 最佳文章（优化）: {steps[-1][1]:.2f}s")
            
            # 8. 点击第一个用户名（智能超时）
            step_start = time.time()
            await page.locator('.hnuser').first.click()
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("用户信息", time.time() - step_start))
            print(f"  8. 用户信息（快速）: {steps[-1][1]:.2f}s")
            
            # 9. 查看用户提交的文章（智能等待）
            step_start = time.time()
            await page.wait_for_selector('.athing')
            user_articles = await page.locator('.athing').count()
            steps.append(("用户文章", time.time() - step_start))
            print(f"  9. 用户文章 ({user_articles} 篇): {steps[-1][1]:.2f}s")
            
            # 10. 返回首页（快速加载）
            step_start = time.time()
            await page.goto('https://news.ycombinator.com')
            steps.append(("返回首页", time.time() - step_start))
            print(f"  10. 返回首页（domcontentloaded）: {steps[-1][1]:.2f}s")
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
        
        await browser.close()
    
    total = time.time() - start
    print(f"\n  总耗时: {total:.2f}s")
    print(f"  优化: 智能超时 + domcontentloaded + 提前响应")
    return total, steps


async def main():
    parser = argparse.ArgumentParser(description='Hacker News 真实测试对比')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    parser.add_argument('--visible', action='store_true', help='可见模式运行（默认）')
    args = parser.parse_args()
    
    headless = args.headless or not args.visible
    
    print("\n" + "=" * 60)
    print("🧪 Hacker News 真实测试")
    print("=" * 60)
    print(f"模式: {'无头' if headless else '可见'}")
    print("网站: https://news.ycombinator.com")
    print("步骤: 10 个操作")
    print("特点: 轻量级，加载快")
    print("=" * 60)
    
    # 运行原生版本
    native_time, native_steps = await native_hackernews_test(headless)
    
    # 等待一下
    await asyncio.sleep(2)
    
    # 运行增强版本
    enhanced_time, enhanced_steps = await enhanced_hackernews_test(headless)
    
    # 对比结果
    print("\n" + "=" * 60)
    print("📊 测试结果对比")
    print("=" * 60)
    
    print(f"\n原生版本:     {native_time:.2f}s")
    print(f"增强版本:     {enhanced_time:.2f}s")
    
    if enhanced_time < native_time:
        improvement = (native_time - enhanced_time) / native_time * 100
        saved = native_time - enhanced_time
        speedup = native_time / enhanced_time
        
        print(f"\n⚡ 性能提升:   {improvement:.1f}%")
        print(f"⏱️  节省时间:   {saved:.2f}s")
        print(f"🚀 速度倍数:   {speedup:.2f}x")
        
        print("\n🔑 关键优化技术：")
        print("  1. 智能超时：3-8s自适应 vs 30s固定")
        print("  2. 快速加载：domcontentloaded vs load+networkidle")
        print("  3. 提前响应：元素可用即继续")
        print("  4. HN轻量页面：优化效果最明显")
        
        print("\n📈 各步骤对比：")
        for i, (native_step, enhanced_step) in enumerate(zip(native_steps, enhanced_steps), 1):
            native_desc, native_t = native_step
            enhanced_desc, enhanced_t = enhanced_step
            if native_t > 0:
                step_improvement = (native_t - enhanced_t) / native_t * 100
                print(f"  {i:2d}. {native_desc:12s} {native_t:5.2f}s → {enhanced_t:5.2f}s  ({step_improvement:+.0f}%)")
    else:
        print("\n⚠️  增强版本在此次测试中未体现优势")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
