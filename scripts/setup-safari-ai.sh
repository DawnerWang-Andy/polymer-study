#!/usr/bin/env bash
# Safari AI 插件一键安装脚本
# 使用方法: bash scripts/setup-safari-ai.sh
#
# 本脚本会依次打开 Mac App Store 上的插件页面，
# 你只需要在每个页面点"获取 / Get"即可。
# 装完后请阅读 docs/safari-ai-setup.md 完成配置。

set -e

echo "========================================"
echo "  Safari AI 插件安装向导"
echo "========================================"
echo ""
echo "本脚本会依次打开以下插件的 App Store 页面："
echo "  1. 沉浸式翻译 (Immersive Translate)"
echo "  2. SciSpace Copilot (论文阅读助手)"
echo "  3. Perplexity - Ask AI"
echo "  4. Glasp (网页高亮 + AI 摘要)"
echo "  5. DeepL Translate (翻译引擎，可选)"
echo ""
read -p "按回车键开始，或 Ctrl+C 取消... " _

# 依次打开 App Store 页面
# macappstores:// 协议直接调起 App Store 应用

open_appstore() {
  local name="$1"
  local url="$2"
  echo ""
  echo "→ 正在打开: $name"
  echo "   $url"
  open "$url"
  echo "   请在 App Store 点击 '获取 / Get'，装完按回车继续..."
  read -p "   [回车继续 / s 跳过] " choice
  if [[ "$choice" == "s" ]]; then
    echo "   已跳过 $name"
  fi
}

# 1. 沉浸式翻译
open_appstore "沉浸式翻译 (Immersive Translate)" \
  "https://apps.apple.com/app/immersive-translate/id6447957425"

# 2. SciSpace Copilot
# 注意: SciSpace 目前主要通过 Chrome 商店提供，Safari 版可能需要用网页版
# 备选: Wiseone
open_appstore "Wiseone (论文/网页阅读辅助，SciSpace 替代品)" \
  "https://apps.apple.com/app/wiseone-your-reading-copilot/id6444373719"

# 3. Perplexity
open_appstore "Perplexity - Ask AI" \
  "https://apps.apple.com/app/perplexity-ask-anything/id6714467315"

# 4. Glasp
open_appstore "Glasp - Social Web Highlighter" \
  "https://apps.apple.com/app/glasp-social-web-highlighter/id1605690124"

# 5. DeepL (可选)
open_appstore "DeepL Translate (可选，用于沉浸式翻译)" \
  "https://apps.apple.com/app/deepl-translate/id1552407475"

echo ""
echo "========================================"
echo "  所有插件页面已打开完毕"
echo "========================================"
echo ""
echo "下一步："
echo "  1. 在 Safari 中打开: 设置 → 扩展 → 逐个勾选启用"
echo "  2. 阅读配置文档: open docs/safari-ai-setup.md"
echo "  3. 填写 API Keys: cp .env.example .env && vim .env"
echo ""
