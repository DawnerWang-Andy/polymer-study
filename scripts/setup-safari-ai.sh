#!/usr/bin/env bash
# Safari AI 插件一键安装脚本（国内直连版）
# 使用方法: bash scripts/setup-safari-ai.sh
#
# 注意: 原版的 DeepL / Perplexity / Glasp / Wiseone / 沉浸式翻译
#       在中国大陆访问不稳定，本版本全部替换为国产方案。
# 装完后请阅读 docs/safari-ai-setup.md 完成配置。

set -e

echo "========================================"
echo "  Safari AI 插件安装向导（国内直连版）"
echo "========================================"
echo ""
echo "本脚本会依次打开以下国产插件的 App Store 页面："
echo "  1. Kimi 智能助手 — AI 侧边栏，长文阅读"
echo "  2. 秘塔 AI 搜索 — Perplexity 国内替代，带引用"
echo "  3. 有道翻译 — 划词翻译，专业词典"
echo "  4. 豆包 — 字节 AI，全文翻译 + 对话"
echo "  5. Obsidian Web Clipper — 网页剪藏到本地 Vault"
echo ""
read -p "按回车键开始，或 Ctrl+C 取消... " _

open_appstore() {
  local name="$1"
  local url="$2"
  echo ""
  echo "→ 正在打开: $name"
  echo "   $url"
  open "$url"
  read -p "   [回车继续 / s 跳过] " choice
  if [[ "$choice" == "s" ]]; then
    echo "   已跳过 $name"
  fi
}

# 1. Kimi 智能助手（Moonshot 官方 Safari 扩展）
open_appstore "Kimi 智能助手" \
  "https://apps.apple.com/cn/app/kimi-%E6%99%BA%E8%83%BD%E5%8A%A9%E6%89%8B/id6474420776"

# 2. 秘塔 AI 搜索
# 秘塔在 macOS App Store 没有独立扩展，通过 Safari 收藏 metaso.cn 或用其 iOS App
# 备选: 用 Safari 书签 + 侧边栏方式
echo ""
echo "→ 秘塔 AI 搜索没有 Safari 扩展"
echo "   → 直接打开网页并加书签："
open "https://metaso.cn"
read -p "   [回车继续] " _

# 3. 有道翻译（网易官方）
open_appstore "有道翻译" \
  "https://apps.apple.com/cn/app/%E7%BD%91%E6%98%93%E6%9C%89%E9%81%93%E8%AF%8D%E5%85%B8/id491854842"

# 4. 豆包（字节跳动）
open_appstore "豆包 (Doubao)" \
  "https://apps.apple.com/cn/app/%E8%B1%86%E5%8C%85-%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8%E5%87%BA%E5%93%81%E7%9A%84-ai-%E6%99%BA%E8%83%BD%E5%8A%A9%E6%89%8B/id6449125253"

# 5. Obsidian Web Clipper（不在 App Store，走官方安装页）
echo ""
echo "→ Obsidian Web Clipper（Safari 扩展）"
open "https://obsidian.md/clipper"
read -p "   [回车继续] " _

echo ""
echo "========================================"
echo "  所有插件页面已打开完毕"
echo "========================================"
echo ""
echo "下一步："
echo "  1. Safari → 设置 → 扩展 → 逐个勾选启用"
echo "  2. 阅读配置文档: open docs/safari-ai-setup.md"
echo "  3. Kimi / 豆包 用手机号登录即可，无需 API Key"
echo "  4. Obsidian Web Clipper 需要在设置里选择 Vault 路径"
echo ""
