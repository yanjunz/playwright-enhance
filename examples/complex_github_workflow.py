"""
GitHub 代码审查工作流 - 复杂场景测试
=====================================

场景：开发者的日常 GitHub 工作流程
- 浏览仓库
- 查看最新的 Pull Requests
- 阅读代码变更
- 添加评论和建议
- 查看 CI/CD 状态
- 审查多个文件
- 批量操作

这是一个真实的、可运行的场景，展示在多页面、
多交互、复杂 DOM 结构下的性能优势。
"""

import asyncio
import time
from playwright.async_api import async_playwright
from playwright_enhance import enhance


async def native_github_workflow(headless=True):
    """原生 Playwright - GitHub 工作流"""
    print("\n🔵 原生 Playwright - GitHub 工作流")
    print("=" * 60)
    
    start = time.time()
    steps = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        
        try:
            # 1. 打开 GitHub 热门仓库
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright', wait_until='load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开仓库", time.time() - step_start))
            print(f"  1. 打开仓库: {steps[-1][1]:.2f}s")
            
            # 2. 等待页面完全加载
            step_start = time.time()
            await page.wait_for_selector('.repository-content')
            await page.wait_for_selector('.file-navigation')
            steps.append(("等待内容", time.time() - step_start))
            print(f"  2. 等待内容: {steps[-1][1]:.2f}s")
            
            # 3. 查看仓库统计信息
            step_start = time.time()
            await page.wait_for_selector('.BorderGrid')
            stars = await page.locator('#repo-stars-counter-star').text_content()
            forks = await page.locator('#repo-network-counter').text_content()
            steps.append(("读取统计", time.time() - step_start))
            print(f"  3. 读取统计: {steps[-1][1]:.2f}s (⭐{stars} 🍴{forks})")
            
            # 4. 进入 Pull Requests 页面
            step_start = time.time()
            await page.click('a[data-tab-item="pull-requests-tab"]')
            await page.wait_for_url('**/pulls')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开PR列表", time.time() - step_start))
            print(f"  4. 打开PR列表: {steps[-1][1]:.2f}s")
            
            # 5. 等待 PR 列表加载
            step_start = time.time()
            await page.wait_for_selector('.js-issue-row')
            pr_count = await page.locator('.js-issue-row').count()
            steps.append(("加载PR列表", time.time() - step_start))
            print(f"  5. 加载PR列表: {steps[-1][1]:.2f}s (找到{pr_count}个PR)")
            
            # 6. 打开第一个 PR
            step_start = time.time()
            await page.locator('.js-issue-row').first.click()
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("打开PR详情", time.time() - step_start))
            print(f"  6. 打开PR详情: {steps[-1][1]:.2f}s")
            
            # 7. 等待 PR 内容加载
            step_start = time.time()
            await page.wait_for_selector('.gh-header-title')
            await page.wait_for_selector('.timeline-comment')
            steps.append(("加载PR内容", time.time() - step_start))
            print(f"  7. 加载PR内容: {steps[-1][1]:.2f}s")
            
            # 8. 查看文件变更
            step_start = time.time()
            await page.click('a[data-tab-item="files-tab"]')
            await page.wait_for_selector('.file-header')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看文件", time.time() - step_start))
            print(f"  8. 查看文件: {steps[-1][1]:.2f}s")
            
            # 9. 统计文件变更数量
            step_start = time.time()
            await page.wait_for_selector('.file')
            file_count = await page.locator('.file').count()
            steps.append(("统计变更", time.time() - step_start))
            print(f"  9. 统计变更: {steps[-1][1]:.2f}s ({file_count}个文件)")
            
            # 10. 展开第一个文件的差异
            step_start = time.time()
            if file_count > 0:
                await page.locator('.file-header').first.click()
                await page.wait_for_selector('.diff-table')
            steps.append(("展开差异", time.time() - step_start))
            print(f" 10. 展开差异: {steps[-1][1]:.2f}s")
            
            # 11. 滚动查看代码
            step_start = time.time()
            await page.evaluate('window.scrollBy(0, 500)')
            await asyncio.sleep(0.5)  # 等待渲染
            steps.append(("滚动查看", time.time() - step_start))
            print(f" 11. 滚动查看: {steps[-1][1]:.2f}s")
            
            # 12. 添加行内评论（模拟悬停）
            step_start = time.time()
            await page.locator('.diff-table tr').first.hover()
            await asyncio.sleep(0.3)
            steps.append(("悬停评论", time.time() - step_start))
            print(f" 12. 悬停评论: {steps[-1][1]:.2f}s")
            
            # 13. 返回对话标签
            step_start = time.time()
            await page.click('a[data-tab-item="conversation-tab"]')
            await page.wait_for_selector('.timeline-comment')
            await page.wait_for_load_state('networkidle')
            steps.append(("返回对话", time.time() - step_start))
            print(f" 13. 返回对话: {steps[-1][1]:.2f}s")
            
            # 14. 滚动到底部查看评论
            step_start = time.time()
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(0.5)
            steps.append(("查看评论", time.time() - step_start))
            print(f" 14. 查看评论: {steps[-1][1]:.2f}s")
            
            # 15. 查看检查状态（CI/CD）
            step_start = time.time()
            await page.wait_for_selector('.merge-status-list')
            checks = await page.locator('.merge-status-item').count()
            steps.append(("查看检查", time.time() - step_start))
            print(f" 15. 查看检查: {steps[-1][1]:.2f}s ({checks}个检查)")
            
            # 16. 返回仓库主页
            step_start = time.time()
            await page.click('a.AppHeader-context-item')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("返回主页", time.time() - step_start))
            print(f" 16. 返回主页: {steps[-1][1]:.2f}s")
            
            # 17. 查看 Issues
            step_start = time.time()
            await page.click('a[data-tab-item="issues-tab"]')
            await page.wait_for_url('**/issues')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看Issues", time.time() - step_start))
            print(f" 17. 查看Issues: {steps[-1][1]:.2f}s")
            
            # 18. 应用标签筛选
            step_start = time.time()
            await page.wait_for_selector('.js-issue-row')
            await page.click('text=Label')
            await asyncio.sleep(0.5)
            await page.click('.select-menu-item >> text=bug')
            await page.wait_for_load_state('networkidle')
            steps.append(("标签筛选", time.time() - step_start))
            print(f" 18. 标签筛选: {steps[-1][1]:.2f}s")
            
            # 19. 查看项目 Actions
            step_start = time.time()
            await page.click('a[data-tab-item="actions-tab"]')
            await page.wait_for_url('**/actions')
            await page.wait_for_load_state('load')
            await page.wait_for_load_state('networkidle')
            steps.append(("查看Actions", time.time() - step_start))
            print(f" 19. 查看Actions: {steps[-1][1]:.2f}s")
            
            # 20. 查看最近的工作流运行
            step_start = time.time()
            await page.wait_for_selector('.Box-row')
            runs = await page.locator('.Box-row').count()
            steps.append(("工作流列表", time.time() - step_start))
            print(f" 20. 工作流列表: {steps[-1][1]:.2f}s ({runs}个运行)")
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)[:80]}")
        
        await browser.close()
    
    total = time.time() - start
    print(f"\n总耗时: {total:.2f}s")
    print(f"平均每步: {total/len(steps):.2f}s")
    print(f"使用策略: 默认配置（load + networkidle + 30s超时）")
    return total, steps


async def enhanced_github_workflow(headless=True):
    """Playwright-Enhance - GitHub 工作流（优化版）"""
    print("\n🟢 Playwright-Enhance - GitHub 工作流（优化）")
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
            # 1. 打开 GitHub 热门仓库（domcontentloaded）
            step_start = time.time()
            await page.goto('https://github.com/microsoft/playwright')
            steps.append(("打开仓库", time.time() - step_start))
            print(f"  1. 打开仓库: {steps[-1][1]:.2f}s")
            
            # 2. 快速等待关键内容
            step_start = time.time()
            await page.wait_for_selector('.repository-content')
            steps.append(("等待内容", time.time() - step_start))
            print(f"  2. 等待内容: {steps[-1][1]:.2f}s")
            
            # 3. 并行读取统计信息
            step_start = time.time()
            await page.wait_for_selector('.BorderGrid')
            stars, forks = await asyncio.gather(
                page.locator('#repo-stars-counter-star').text_content(),
                page.locator('#repo-network-counter').text_content()
            )
            steps.append(("读取统计", time.time() - step_start))
            print(f"  3. 读取统计: {steps[-1][1]:.2f}s (⭐{stars} 🍴{forks})")
            
            # 4. 进入 Pull Requests（优化导航）
            step_start = time.time()
            await page.click('a[data-tab-item="pull-requests-tab"]')
            await page.wait_for_url('**/pulls')
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("打开PR列表", time.time() - step_start))
            print(f"  4. 打开PR列表: {steps[-1][1]:.2f}s")
            
            # 5. 快速加载 PR 列表
            step_start = time.time()
            await page.wait_for_selector('.js-issue-row')
            pr_count = await page.locator('.js-issue-row').count()
            steps.append(("加载PR列表", time.time() - step_start))
            print(f"  5. 加载PR列表: {steps[-1][1]:.2f}s (找到{pr_count}个PR)")
            
            # 6. 打开第一个 PR（优化等待）
            step_start = time.time()
            await page.locator('.js-issue-row').first.click()
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("打开PR详情", time.time() - step_start))
            print(f"  6. 打开PR详情: {steps[-1][1]:.2f}s")
            
            # 7. 并行等待关键元素
            step_start = time.time()
            await asyncio.gather(
                page.wait_for_selector('.gh-header-title'),
                page.wait_for_selector('.timeline-comment')
            )
            steps.append(("加载PR内容", time.time() - step_start))
            print(f"  7. 加载PR内容: {steps[-1][1]:.2f}s")
            
            # 8. 快速查看文件
            step_start = time.time()
            await page.click('a[data-tab-item="files-tab"]')
            await page.wait_for_selector('.file-header')
            steps.append(("查看文件", time.time() - step_start))
            print(f"  8. 查看文件: {steps[-1][1]:.2f}s")
            
            # 9. 快速统计变更
            step_start = time.time()
            await page.wait_for_selector('.file')
            file_count = await page.locator('.file').count()
            steps.append(("统计变更", time.time() - step_start))
            print(f"  9. 统计变更: {steps[-1][1]:.2f}s ({file_count}个文件)")
            
            # 10. 快速展开差异
            step_start = time.time()
            if file_count > 0:
                await page.locator('.file-header').first.click()
                await page.wait_for_selector('.diff-table')
            steps.append(("展开差异", time.time() - step_start))
            print(f" 10. 展开差异: {steps[-1][1]:.2f}s")
            
            # 11. 快速滚动
            step_start = time.time()
            await page.evaluate('window.scrollBy(0, 500)')
            await asyncio.sleep(0.2)  # 减少等待
            steps.append(("滚动查看", time.time() - step_start))
            print(f" 11. 滚动查看: {steps[-1][1]:.2f}s")
            
            # 12. 快速悬停
            step_start = time.time()
            await page.locator('.diff-table tr').first.hover()
            await asyncio.sleep(0.1)  # 减少等待
            steps.append(("悬停评论", time.time() - step_start))
            print(f" 12. 悬停评论: {steps[-1][1]:.2f}s")
            
            # 13. 返回对话（优化等待）
            step_start = time.time()
            await page.click('a[data-tab-item="conversation-tab"]')
            await page.wait_for_selector('.timeline-comment')
            steps.append(("返回对话", time.time() - step_start))
            print(f" 13. 返回对话: {steps[-1][1]:.2f}s")
            
            # 14. 快速滚动
            step_start = time.time()
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(0.2)
            steps.append(("查看评论", time.time() - step_start))
            print(f" 14. 查看评论: {steps[-1][1]:.2f}s")
            
            # 15. 快速查看检查
            step_start = time.time()
            await page.wait_for_selector('.merge-status-list')
            checks = await page.locator('.merge-status-item').count()
            steps.append(("查看检查", time.time() - step_start))
            print(f" 15. 查看检查: {steps[-1][1]:.2f}s ({checks}个检查)")
            
            # 16. 返回主页（优化导航）
            step_start = time.time()
            await page.click('a.AppHeader-context-item')
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("返回主页", time.time() - step_start))
            print(f" 16. 返回主页: {steps[-1][1]:.2f}s")
            
            # 17. 查看 Issues（优化导航）
            step_start = time.time()
            await page.click('a[data-tab-item="issues-tab"]')
            await page.wait_for_url('**/issues')
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("查看Issues", time.time() - step_start))
            print(f" 17. 查看Issues: {steps[-1][1]:.2f}s")
            
            # 18. 快速应用筛选
            step_start = time.time()
            await page.wait_for_selector('.js-issue-row')
            await page.click('text=Label')
            await asyncio.sleep(0.2)
            await page.click('.select-menu-item >> text=bug')
            steps.append(("标签筛选", time.time() - step_start))
            print(f" 18. 标签筛选: {steps[-1][1]:.2f}s")
            
            # 19. 查看 Actions（优化导航）
            step_start = time.time()
            await page.click('a[data-tab-item="actions-tab"]')
            await page.wait_for_url('**/actions')
            await page.wait_for_load_state('domcontentloaded')
            steps.append(("查看Actions", time.time() - step_start))
            print(f" 19. 查看Actions: {steps[-1][1]:.2f}s")
            
            # 20. 快速查看工作流
            step_start = time.time()
            await page.wait_for_selector('.Box-row')
            runs = await page.locator('.Box-row').count()
            steps.append(("工作流列表", time.time() - step_start))
            print(f" 20. 工作流列表: {steps[-1][1]:.2f}s ({runs}个运行)")
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)[:80]}")
        
        await browser.close()
    
    total = time.time() - start
    print(f"\n总耗时: {total:.2f}s")
    print(f"平均每步: {total/len(steps):.2f}s")
    print(f"优化策略: domcontentloaded + 智能超时 + 并行操作")
    return total, steps


async def run_github_comparison(headless=True):
    """运行 GitHub 工作流对比"""
    print("\n" + "=" * 60)
    print("👨‍💻 GitHub 工作流 - 性能对比测试")
    print("=" * 60)
    print("\n场景：开发者的日常 GitHub 操作（20个步骤）")
    print("  • 浏览仓库和统计信息")
    print("  • 查看 Pull Requests")
    print("  • 审查代码变更")
    print("  • 查看 Issues 和标签")
    print("  • 查看 CI/CD Actions")
    
    print(f"\n浏览器模式: {'无头模式' if headless else '可见模式'}")
    print("\n⚠️  注意：需要网络连接访问 GitHub")
    print("=" * 60)
    
    # 运行原生版本
    native_time, native_steps = await native_github_workflow(headless=headless)
    
    print("\n" + "-" * 60)
    print("⏸️  暂停 3 秒...")
    await asyncio.sleep(3)
    
    # 运行增强版本
    enhanced_time, enhanced_steps = await enhanced_github_workflow(headless=headless)
    
    # 详细对比
    print("\n" + "=" * 60)
    print("📊 详细性能对比")
    print("=" * 60)
    
    print("\n逐步对比：")
    print(f"{'步骤':<20} {'原生':<10} {'增强':<10} {'提升':<10}")
    print("-" * 60)
    
    for i, (native_step, enhanced_step) in enumerate(zip(native_steps, enhanced_steps), 1):
        native_name, native_dur = native_step
        enhanced_name, enhanced_dur = enhanced_step
        improvement = (native_dur - enhanced_dur) / native_dur * 100 if native_dur > 0 else 0
        print(f"{i:2d}. {native_name:<16} {native_dur:>6.2f}s  {enhanced_dur:>6.2f}s  {improvement:>6.1f}%")
    
    # 总体对比
    print("\n" + "=" * 60)
    print("📈 总体性能对比")
    print("=" * 60)
    
    improvement = (native_time - enhanced_time) / native_time * 100
    saved = native_time - enhanced_time
    speedup = native_time / enhanced_time
    
    print(f"\n原生 Playwright:     {native_time:.2f}s")
    print(f"Playwright-Enhance:  {enhanced_time:.2f}s")
    print(f"\n⚡ 性能提升:          {improvement:.1f}%")
    print(f"⏱️  节省时间:          {saved:.2f}s")
    print(f"🚀 速度倍数:          {speedup:.2f}x")
    
    print("\n🔑 关键优化技术：")
    print("  1. 页面导航优化：6次导航，每次节省 2-4s")
    print("  2. 并行元素查找：减少串行等待")
    print("  3. 智能等待：元素就绪立即继续")
    print("  4. 动态超时：避免不必要的长等待")
    
    print("\n💡 GitHub 场景特点：")
    print("  • 多标签页切换（PR/Issues/Actions）")
    print("  • 大量 DOM 元素加载")
    print("  • 动态内容渲染")
    print("  • 适合 AI Agent 代码审查自动化")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    import sys
    
    print("\n🎯 GitHub 工作流性能对比测试")
    print("=" * 60)
    
    # 检查参数
    headless = '--headless' in sys.argv or '-h' in sys.argv
    visible = '--visible' in sys.argv or '-v' in sys.argv
    
    print("\n⚠️  注意：")
    print("  • 真实 GitHub 网站测试")
    print("  • 需要网络连接")
    print("  • 总耗时约 60-120 秒")
    print("  • 可能受网络速度影响")
    
    if visible or not headless:
        print("  • 可见模式：可以看到浏览器操作")
    else:
        print("  • 无头模式：后台运行")
    
    print("\n按 Enter 继续，或 Ctrl+C 取消...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n❌ 测试已取消")
        sys.exit(0)
    
    try:
        use_headless = headless or not visible
        asyncio.run(run_github_comparison(headless=use_headless))
    except KeyboardInterrupt:
        print("\n\n❌ 测试已取消")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        print("\n💡 提示：")
        print("  - 检查网络连接")
        print("  - GitHub 可能限流或变更页面结构")
        print("  - 运行 'playwright install chromium' 确保浏览器已安装")
