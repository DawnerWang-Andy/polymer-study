# Safari AI 插件配置指南

**目标**：为高分子专业本科生（读英文文献 + 写报告 + 大创项目）配置 Safari AI 生态。

**执行顺序**：
1. `bash scripts/setup-safari-ai.sh` 一键打开所有插件的 App Store 页面
2. 在每个页面点"获取"完成安装
3. 打开 Safari → 设置 → 扩展 → 逐个勾选启用
4. 按本文档逐个配置

---

## 一、沉浸式翻译 (Immersive Translate)

**用途**：读 Nature / JACS 等英文文献时中英对照显示

### 配置步骤
1. 点击 Safari 工具栏的沉浸式翻译图标 → 设置
2. **翻译服务** 添加三个引擎（对应你选的"全部配上"方案）：

| 引擎 | 用途 | 需要 API Key |
|------|------|--------------|
| **谷歌翻译** | 日常浏览（默认） | 否，免费无限 |
| **DeepL** | 高质量翻译 | 是，见下方 |
| **Claude / OpenAI** | 专业论文，可指定学术风格 | 是，读取 `.env` |

### DeepL Key 申请
1. 访问 https://www.deepl.com/pro-api（选免费版 DeepL API Free）
2. 用邮箱注册（需要绑定信用卡，但免费额度 50万字符/月不扣费）
3. 拿到 Auth Key 后填入沉浸式翻译 → DeepL → 认证密钥

### Claude 配置（推荐用于文献）
在沉浸式翻译中选"自定义 AI 翻译服务"：
- API 地址：`https://api.anthropic.com/v1/messages`
- 模型：`claude-sonnet-5`（性价比最高）或 `claude-opus-4-8`
- API Key：从 `.env` 里的 `ANTHROPIC_API_KEY` 复制
- 自定义 Prompt（学术风格）：
  ```
  你是一名高分子材料专业的学术翻译。请将以下英文翻译成中文，
  保持专业术语准确（如 monomer→单体、glass transition→玻璃化转变），
  英文缩写和公式保留原文，语言流畅、符合中文学术论文风格。
  ```

### 快捷键
- `Option + A` 翻译整个页面
- `Option + W` 切换鼠标悬停翻译

---

## 二、Wiseone（SciSpace 的 Safari 替代品）

**注意**：SciSpace Copilot 官方目前只有 Chrome 扩展，Safari 上用 **Wiseone** 作为替代。

**用途**：读英文网页 / PDF 时划词自动解释术语、公式、缩写。

### 配置
1. 首次打开注册（免费版够用）
2. 设置 → Language → 输出语言选"中文"
3. Reading Mode → 开启"Auto-explain complex terms"（自动解释复杂词）

### 使用
- 在 Nature / arXiv HTML 页面上划词 → 弹窗显示定义 + 相关文献
- PDF 需要用 Safari 打开在线 PDF（本地 PDF 建议直接用 Zotero）

---

## 三、Perplexity - Ask AI

**用途**：查资料、找文献时的智能搜索，结果带引用来源。

### 配置
1. 首次打开注册（免费版每天 5 次 Pro Search，日常够用）
2. 设置 → Default AI Model → 选 `Claude 3.5 Sonnet` 或 `GPT-4o`
3. Focus Mode → 默认设为 `Academic`（自动限定学术源）

### 使用场景
- 查"高熵金属配位聚合物 电催化甘油氧化 最新进展" → 得到带引用的综述
- 需要孤证时对照 DocsGPT 本地知识库使用

---

## 四、Glasp（网页高亮 + Obsidian 联动）

**用途**：读网页/YouTube 时高亮 → 自动同步到 Obsidian。

### 配置
1. 首次打开用 Google 账号登录
2. 设置 → Integrations → **Obsidian**：
   - 选择 Vault：`polymer-study`
   - 文件夹路径：`02-科研地图/文献笔记/glasp/`
   - 文件模板选 "Individual notes"（每条高亮一个文件）
3. AI Summary：开启"Auto-generate summary"（每篇网页自动 AI 摘要）

### Obsidian 联动细节
Glasp 会在 `02-科研地图/文献笔记/glasp/` 下生成 Markdown 文件，格式：
```yaml
---
title: <网页标题>
url: <原网址>
tags: [glasp, highlight]
date: 2026-07-08
---

## AI Summary
...

## Highlights
- 高亮1
- 高亮2
```

配合你 Vault 里的 Dataview 查询，可以在文献笔记主页统一浏览所有高亮。

---

## 五、`.env` 文件配置

复制模板并填入 Key：
```bash
cp .env.example .env
vim .env  # 或用 VS Code 打开
```

需要填的字段（已在 `.env.example` 里预留）：
- `DEEPL_API_KEY` — 沉浸式翻译用
- `ANTHROPIC_API_KEY` — 沉浸式翻译 Claude 模式 + 你其他项目通用
- `OPENAI_API_KEY` — 沉浸式翻译 GPT 模式（可选）

**注意**：Safari 插件是独立 App，无法直接读 `.env`。`.env` 只是你记录 Key 的中转站，最后要**手动复制到各个插件的设置面板里**。

---

## 六、装完后的自检清单

打开 Safari 一个 Nature 论文页面（比如 https://www.nature.com/articles/s41586-023-06600-9），验证：

- [ ] 沉浸式翻译：按 `Option + A` 出现中英对照
- [ ] Wiseone：划词 "polymerization" 弹窗出现定义
- [ ] Perplexity：工具栏图标可打开侧边栏搜索
- [ ] Glasp：选中一段文字出现"Highlight"按钮，点击后同步到 Obsidian

全部通过 = 配置成功 ✅

---

## 七、日常使用建议

| 场景 | 用哪个 |
|------|--------|
| 读一篇 Nature 论文 | 沉浸式翻译（Claude 引擎）+ Wiseone 划词 |
| 查"XX 是什么" | Perplexity（带引用） |
| 想把网页内容存进 Obsidian | Glasp 高亮 |
| 查本地已上传的论文 | `python scripts/ask-docsgpt.py "问题"`（不用 Safari 插件） |
| 翻译日常英文网页 | 沉浸式翻译（谷歌引擎，快） |

---

## 常见问题

**Q: 沉浸式翻译按了 Option+A 没反应？**
A: 检查 Safari → 设置 → 扩展 → 沉浸式翻译 → 权限，改为"在所有网站上允许"。

**Q: SciSpace 的 Chrome 版能不能装到 Safari？**
A: 不能。Safari 的扩展格式和 Chrome 不兼容，必须用 Wiseone 替代。如果你非常需要 SciSpace，可以装个 Chrome 只用来读论文。

**Q: Glasp 同步到 Obsidian 是双向的吗？**
A: 单向。Glasp → Obsidian，不会反过来。如果你在 Obsidian 里改了笔记不会影响 Glasp 云端。
