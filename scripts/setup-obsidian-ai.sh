#!/usr/bin/env bash
# Obsidian AI 生态一键配置向导
# 使用方法: bash scripts/setup-obsidian-ai.sh
#
# 前提: Safari 扩展装不上，改用 Obsidian 插件方案。
# 本脚本会：
#   1. 打开 DeepSeek API 注册页（拿免费 Key）
#   2. 提示 Obsidian 里装哪几个插件
#   3. 打开配置文档

set -e

echo "========================================"
echo "  Obsidian AI 一键配置向导"
echo "========================================"
echo ""
echo "本方案：只用 Obsidian，不用 Safari 扩展"
echo ""
echo "需要装的 Obsidian 插件（在 Obsidian 里搜）："
echo "  1. Copilot         — AI 侧边栏对话"
echo "  2. Text Generator  — 用 AI 生成/改写笔记"
echo "  3. Translate       — 选中文本一键翻译"
echo "  4. PDF++           — 增强 PDF 阅读（划词高亮）"
echo "  5. Web Clipper     — 网页 → 笔记（可选）"
echo ""
read -p "按回车开始（Ctrl+C 取消）..." _

echo ""
echo "→ 步骤 1: 打开 DeepSeek 注册页"
open "https://platform.deepseek.com/sign_in"
echo "  - 用手机号注册"
echo "  - 送 500 万 token 免费额度（够用几个月）"
echo "  - 进入 'API keys' → 'Create new API key' → 复制"
echo ""
read -p "拿到 Key 了？按回车继续..." _

echo ""
echo "→ 步骤 2: 打开配置文档"
open "docs/obsidian-ai-setup.md"
echo ""

echo "→ 步骤 3: 打开你的 Obsidian Vault"
open -a Obsidian "/Users/dawnerwang/polymer-study" 2>/dev/null || open -a "Obsidian" 2>/dev/null || echo "  请手动打开 Obsidian"
echo ""

echo "========================================"
echo "  接下来在 Obsidian 里做："
echo "========================================"
echo ""
echo "1. ⚙️  设置 → 第三方插件 → 关闭安全模式（如未关闭）"
echo "2. 🔌 社区插件 → 浏览 → 搜索 'Copilot' → 安装 → 启用"
echo "3. ⚙️  Copilot 设置："
echo "     - Default Model: 选 'Custom Model'"
echo "     - API Base URL: https://api.deepseek.com/v1"
echo "     - Model Name: deepseek-chat"
echo "     - API Key: 粘贴你刚才拿到的 DeepSeek Key"
echo "4. 💬 按 Cmd+P → 输入 'Copilot: Open Chat' → 开聊"
echo ""
echo "完整步骤见: docs/obsidian-ai-setup.md"
