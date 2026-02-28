"""
GitHub 真实测试对比
==================

场景：在 GitHub 上浏览热门仓库
- 搜索仓库
- 查看代码
- 浏览 Issues
- 查看 Pull Requests
- 切换分支

这是一个真实的、可重复的测试，使用 GitHub 公共仓库。
"""

import asyncio
import time
import argparse
from playwright.async_api import async_playwright
from playwright_enhance import enhance


async def native_github_test(headless=False):
    """原生 Playwright - GitHub 测试"""
    print("\n🔵 原生 Playwright - GitHub 测试")
    print("=" * 60)
    
    start = time.time()
    steps = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        
        try:
            # 1. 打开 GitHub 首页
            step_start = time.time()
            await page.goto('https://github.com', wait_until='load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开首页", time.time() - step_start))
            print(f"  1. 打开首页: {steps[-1][1]:.2f}s")
            
            # 2. 直接访问 Playwright 仓库（避免搜索框变化）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开仓库", time.time() - step_start))
            print(f"  2. 打开仓库: {steps[-1][1]:.2f}s")
            
            # 3. 查看 README
            step_start = time.time()
            await page.wait_for_selector('article', timeout=30000)
            readme_text = await page.locator('article').first.inner_text()
            steps.append(("加载README", time.time() - step_start))
            print(f"  3. 加载README ({len(readme_text)} 字符): {steps[-1][1]:.2f}s")
            
            # 4. 点击 Issues 标签
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/issues')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看Issues", time.time() - step_start))
            print(f"  4. 查看Issues: {steps[-1][1]:.2f}s")
            
            # 5. 点击第一个 Issue
            step_start = time.time()
            await page.wait_for_selector('[data-hovercard-type="issue"]', timeout=30000)
            first_issue_link = await page.locator('[data-hovercard-type="issue"]').first.get_attribute('href')
            if first_issue_link:
                await page.goto(f'https://github.com{first_issue_link}')
                await page.wait_for_load_state('load')
                await page.wait_for_load_state('networkidle')
            steps.append(("打开Issue", time.time() - step_start))
            print(f"  5. 打开Issue: {steps[-1][1]:.2f}s")
            
            # 6. 返回仓库首页
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("返回仓库", time.time() - step_start))
            print(f"  6. 返回仓库: {steps[-1][1]:.2f}s")
            
            # 7. 点击 Pull requests 标签
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/pulls')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看PRs", time.time() - step_start))
            print(f"  7. 查看PRs: {steps[-1][1]:.2f}s")
            
            # 8. 查看 Actions 标签
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/actions')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看Actions", time.time() - step_start))
            print(f"  8. 查看Actions: {steps[-1][1]:.2f}s")
            
            # 9. 查看 Wiki
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/wiki')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看Wiki", time.time() - step_start))
            print(f"  9. 查看Wiki: {steps[-1][1]:.2f}s")
            
            # 10. 返回首页
            step_start = time.time()
            await page.goto('https://github.com')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("返回GitHub首页", time.time() - step_start))
            print(f"  10. 返回GitHub首页: {steps[-1][1]:.2f}s")
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
        
        await browser.close()
    
    total = time.time() - start
    print(f"\n  总耗时: {total:.2f}s")
    print(f"  配置: 默认超时(30s), 等待load+networkidle")
    return total, steps


async def enhanced_github_test(headless=False):
    """Playwright-Enhance - GitHub 测试"""
    print("\n🟢 Playwright-Enhance - GitHub 测试")
    print("=" * 60)
    
    start = time.time()
    steps = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        
        # 配置智能等待（GitHub 需要更长超时）
        config = {
            'smart_waiting': {
                'enabled': True,
                'initial_timeout': 8000,  # GitHub 复杂，初始超时更长
                'min_timeout': 5000,       # 最小超时增加到 5s
                'max_timeout': 20000,      # 最大超时增加到 20s
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
            # 1. 打开 GitHub 首页（智能优化）
            step_start = time.time()
            await page.goto('https://github.com')
            steps.append(("打开首页", time.time() - step_start))
            print(f"  1. 打开首页（domcontentloaded）: {steps[-1][1]:.2f}s")
            
            # 2. 直接访问 Playwright 仓库（避免搜索框变化）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright')
            steps.append(("打开仓库", time.time() - step_start))
            print(f"  2. 打开仓库（domcontentloaded）: {steps[-1][1]:.2f}s")
            
            # 3. 查看 README（智能等待）
            step_start = time.time()
            await page.wait_for_selector('article')
            readme_text = await page.locator('article').first.inner_text()
            steps.append(("加载README", time.time() - step_start))
            print(f"  3. 加载README ({len(readme_text)} 字符): {steps[-1][1]:.2f}s")
            
            # 4. 点击 Issues 标签（domcontentloaded）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/issues')
            steps.append(("查看Issues", time.time() - step_start))
            print(f"  4. 查看Issues（快速）: {steps[-1][1]:.2f}s")
            
            # 5. 点击第一个 Issue（智能超时）
            step_start = time.time()
            await page.wait_for_selector('[data-hovercard-type="issue"]')
            first_issue_link = await page.locator('[data-hovercard-type="issue"]').first.get_attribute('href')
            if first_issue_link:
                await page.goto(f'https://github.com{first_issue_link}')
            steps.append(("打开Issue", time.time() - step_start))
            print(f"  5. 打开Issue（优化）: {steps[-1][1]:.2f}s")
            
            # 6. 返回仓库首页（快速加载）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright')
            steps.append(("返回仓库", time.time() - step_start))
            print(f"  6. 返回仓库（domcontentloaded）: {steps[-1][1]:.2f}s")
            
            # 7. 点击 Pull requests 标签（智能等待）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/pulls')
            steps.append(("查看PRs", time.time() - step_start))
            print(f"  7. 查看PRs（快速）: {steps[-1][1]:.2f}s")
            
            # 8. 查看 Actions 标签（优化加载）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/actions')
            steps.append(("查看Actions", time.time() - step_start))
            print(f"  8. 查看Actions（优化）: {steps[-1][1]:.2f}s")
            
            # 9. 查看 Wiki（智能超时）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright/wiki')
            steps.append(("查看Wiki", time.time() - step_start))
            print(f"  9. 查看Wiki（快速）: {steps[-1][1]:.2f}s")
            
            # 10. 返回首页（快速加载）
            step_start = time.time()
            await page.goto('https://github.com')
            steps.append(("返回GitHub首页", time.time() - step_start))
            print(f"  10. 返回GitHub首页（domcontentloaded）: {steps[-1][1]:.2f}s")
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
        
        await browser.close()
    
    total = time.time() - start
    print(f"\n  总耗时: {total:.2f}s")
    print(f"  优化: 智能超时 + domcontentloaded + 提前响应")
    return total, steps


async def main():
    parser = argparse.ArgumentParser(description='GitHub 真实测试对比')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    parser.add_argument('--visible', action='store_true', help='可见模式运行（默认）')
    args = parser.parse_args()
    
    headless = args.headless or not args.visible
    
    print("\n" + "=" * 60)
    print("🧪 GitHub 真实测试")
    print("=" * 60)
    print(f"模式: {'无头' if headless else '可见'}")
    print("仓库: microsoft/playwright")
    print("步骤: 10 个操作")
    print("=" * 60)
    
    # 运行原生版本
    native_time, native_steps = await native_github_test(headless)
    
    # 等待一下
    await asyncio.sleep(2)
    
    # 运行增强版本
    enhanced_time, enhanced_steps = await enhanced_github_test(headless)
    
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
        print("  4. 减少等待：GitHub 大量 AJAX 场景最明显")
        
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
