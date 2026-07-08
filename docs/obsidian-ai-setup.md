# Obsidian AI 生态配置指南（只用 Obsidian）

**背景**：Safari 扩展在你机器上装不上，改用 **只在 Obsidian 里跑** 的方案。所有 AI 功能都做进 Obsidian，你不用切来切去，笔记也直接落在你自己的 Vault 里。

**AI 模型**：**DeepSeek**（¥1/百万 token，学术翻译质量强，性价比最高）

---

## 一、五分钟快速开始

### Step 1：申请 DeepSeek API Key（3 分钟）
1. 打开 https://platform.deepseek.com/sign_in
2. 手机号注册（新账号送 500 万 token 免费额度，够用几个月）
3. 进入 API Keys 页面 → "Create new API key"
4. **立刻复制**（关闭页面后看不到了），存到 `.env` 里的 `DEEPSEEK_API_KEY=`

### Step 2：Obsidian 装 Copilot 插件（2 分钟）
1. 打开 Obsidian → 设置 (⌘,)
2. **第三方插件** → 关闭"安全模式"（如已关闭，跳过）
3. **社区插件** → 浏览 → 搜索 **Copilot**（作者 logancyang）
4. 点安装 → 启用

### Step 3：配置 Copilot 接入 DeepSeek（1 分钟）
在 Obsidian 里进 Copilot 设置：
- **Default Model**: 选 `Custom Model`（或叫 `Third-party OpenAI-format`）
- **API Base URL**: `https://api.deepseek.com/v1`
- **Model Name**: `deepseek-chat`（日常）或 `deepseek-reasoner`（推理，读论文推荐）
- **API Key**: 粘贴 DeepSeek Key
- **Temperature**: 0.3（学术翻译建议低温度）

### Step 4：验证
- ⌘P → 输入 "Copilot: Open Chat" → 回车
- 侧边栏出现对话框 → 问"你好，请介绍一下你自己"
- 有回复 = 成功 ✅

---

## 二、推荐的 Obsidian 插件全景

| 插件 | 作者 | 用途 | 必装 |
|------|------|------|------|
| **Copilot** | logancyang | AI 侧边栏对话，接入 DeepSeek/Kimi/GLM | ⭐⭐⭐ |
| **Text Generator** | nhaouari | 选中文本让 AI 生成/改写（比 Copilot 更适合写作） | ⭐⭐ |
| **Translate** | Fevol | 划词翻译，接谷歌/百度/DeepL/自定义 API | ⭐⭐ |
| **PDF++** | RyotaUshio | 增强 PDF 阅读，划词高亮直接生成笔记 | ⭐⭐⭐ |
| **Smart Connections** | Brian Petro | 语义搜索你自己的笔记，AI 会引用你的 Vault | ⭐⭐ |
| **Local GPT** | pfrankov | 本地 Ollama 模型（离线用） | 可选 |

**核心组合**：Copilot + PDF++ + Text Generator = 覆盖你 95% 的场景。

---

## 三、Copilot 详细配置（重点）

### 3.1 学术模式 System Prompt
在 Copilot 设置 → **User System Prompt** 里填入：

```
你是一名高分子材料专业的学术助手。回答时遵守：
1. 专业术语中英对照：单体(monomer)、玻璃化转变(Tg)、聚合反应(polymerization)、
   交联(crosslinking)、电催化(electrocatalysis)、金属有机框架(MOF)、
   高熵配位聚合物(HE-MHOF)、甘油氧化反应(GOR) 等
2. 化学式、公式、单位保留原文（PMMA、Fe₂O₃、mol/L）
3. 引用论文数据时注明章节、图表编号（如 Fig.2、Section 3.1）
4. 用中文回答，学术风格，简洁准确
5. 用户是高分子专业本科生，讲清核心概念的同时可以适当补充背景
6. 涉及数据时明确来源，避免脱离原文自行发挥
```

### 3.2 常用命令（⌘P 呼出命令面板）

| 命令 | 用途 |
|------|------|
| `Copilot: Open Chat` | 打开侧边栏对话 |
| `Copilot: Chat with Note` | 让 AI 读当前笔记全文并回答 |
| `Copilot: Summarize` | 一键总结当前笔记 |
| `Copilot: Translate` | 翻译选中文本 |
| `Copilot: Explain` | 解释选中文本（超好用！） |
| `Copilot: Rewrite` | 改写选中文本（学术润色） |

### 3.3 自定义命令（Custom Prompt）
Copilot 支持你写自己的 Prompt 模板。推荐加两个：

**Prompt 1：翻译学术段落**
```
名称: 翻译论文段落
Prompt: 请将以下英文段落翻译成中文，专业术语保留英文括注，
       化学式和公式保留原文，语言符合中文学术风格：
       {}
```

**Prompt 2：读论文提取关键信息**
```
名称: 论文速读
Prompt: 请从以下论文段落中提取：
       1. 核心研究问题
       2. 采用的方法/材料体系
       3. 关键结论
       4. 需要重点记忆的数据
       用中文回答，简洁分点。
       段落: {}
```

---

## 四、PDF++ 配置（读文献必装）

在 Obsidian 装 **PDF++**（社区插件搜索）：
1. 把 Nature/JACS 论文 PDF 拖进 Vault（放到 `research/papers/` 目录）
2. 打开 PDF → 划词 → 右键 "Add Highlight & Add to..."
3. 高亮会自动生成一条 Markdown 引用到你选的文献笔记
4. 结合 Copilot：选中 PDF 里的英文段 → 复制 → Chat 里粘贴 → 让 DeepSeek 讲解

### PDF++ 推荐配置
- **Backlinks**: 开启（显示这段被哪些笔记引用）
- **Highlight color**: 黄色=重点、绿色=已理解、红色=待深究
- **Auto-focus**: 开启（点笔记引用直接跳到 PDF 对应位置）

---

## 五、"读一篇 Nature 论文" 完整工作流

假设你今天要读 `Nature 626, 123 (2024)`：

### Step 1：进 Vault
把 PDF 拖到 `research/papers/Nature-2024-高熵配位.pdf`

### Step 2：新建文献笔记
在 `02-科研地图/文献笔记/` 新建 `高熵配位-Nature-2024.md`，用 Templater 生成模板（Frontmatter 含 DOI/作者/年份）

### Step 3：读 PDF（用 PDF++）
- 划取重要段落 → 高亮 + 生成引用到笔记
- 划取不懂的英文段 → 复制

### Step 4：调 Copilot 讲解
- ⌘P → `Copilot: Open Chat` → 粘贴段落 → 用你保存的"论文速读" Prompt
- DeepSeek 返回中文讲解 + 关键数据
- 复制回笔记

### Step 5：让 Copilot 帮你写总结
- 笔记写完 → `Copilot: Chat with Note` → "帮我总结这篇论文核心创新点"
- 生成的总结放到笔记末尾"我的理解"部分

### Step 6：链接到概念卡
用 `[[高熵合金]]` `[[电催化甘油氧化]]` 关联到已有笔记

**耗时对比**：原来读一篇 Nature 全英文论文可能要 2-3 小时；用这个流程约 45-60 分钟。

---

## 六、翻译方案（不用沉浸式翻译）

### 方案 A：Copilot 直接翻译（推荐）
- 选中文本 → ⌘P → `Copilot: Translate` → 侧边栏出译文
- 学术准确度最高（DeepSeek 中文强）

### 方案 B：Translate 插件（免费，无需 Key）
- 装 **Translate** 插件（社区插件搜索）
- 引擎选"Google Translate"（网页版免费镜像）或"Bing"
- 选中文本 → 快捷键 `Ctrl+Shift+T` → 出译文

### 方案 C：网页翻译
如果非要翻译整个网页而不是 Obsidian 里的文本：
- 用 macOS 自带 Safari 翻译（右键 → 翻译成中文）
- 或用系统级翻译工具 **Bob**（Mac App Store 免费版）

---

## 七、`.env` 该放什么

```bash
# === Obsidian AI 生态（只需要 DeepSeek 一个 Key）===
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx  # 从 platform.deepseek.com 获取

# 备用（可选，都免费）：
ZHIPU_API_KEY=       # https://open.bigmodel.cn/usercenter/apikeys (完全免费)
KIMI_API_KEY=        # https://platform.moonshot.cn/console/api-keys (免费额度)
```

**注意**：Obsidian 插件不会自动读 `.env`，Key 需要**手动复制到 Copilot 设置面板**。`.env` 只作为你自己记录的中转站。

---

## 八、验证清单

装完后确认这些都能跑通：

- [ ] Copilot: 侧边栏能对话
- [ ] Copilot: 选中文本 → 命令 "Explain" → 有回复
- [ ] PDF++: PDF 划词能生成高亮
- [ ] Templater: 新建文献笔记能套模板（这个你已经装了）
- [ ] Smart Connections（如装）: 侧边栏出现相关笔记推荐

---

## 九、常见问题

**Q: DeepSeek 免费额度用完了怎么办？**
A: 直接充值，¥10 能用 1-2 个月。或者切换到智谱 GLM-4-Flash（Copilot 里换 Base URL 到 `https://open.bigmodel.cn/api/paas/v4`，模型选 `glm-4-flash`，完全免费）。

**Q: Copilot 报错 "Invalid API Key"？**
A: 检查三点：
1. Key 有没有前后空格
2. Base URL 末尾**不要**加 `/chat/completions`（只到 `/v1`）
3. Model Name 拼写：DeepSeek 是 `deepseek-chat`，不是 `DeepSeek-Chat`

**Q: 想让 Copilot 引用我 Vault 里的其他笔记？**
A: 装 **Smart Connections** 插件，Copilot 会自动检索相关笔记作为上下文。或者手动在对话里 @文件名。

**Q: 手机上能用吗？**
A: 能。装 Obsidian 移动版 → 同步 Vault → 手机上装同款 Copilot 插件即可（Key 需要重新填一次）。

**Q: 想用本地免费模型（不联网）？**
A: 装 Ollama + `local-gpt` 插件，模型选 `qwen2.5:7b`（中文强）。速度慢但完全免费、离线可用。

---

## 十、和之前项目工具的关系

| 工具 | 用途 | 是否还用 |
|------|------|---------|
| Obsidian + Copilot | 日常读文献、笔记、AI 对话 | ✅ 主力 |
| DocsGPT (`ask-docsgpt.py`) | 查本地已上传的论文库 | ✅ 补充 |
| Claude Code / Codex | 写代码、跑实验、改仓库 | ✅ 编程用 |
| Zotero | 管理 PDF 和引用 | ✅ 文献管理 |
| Safari 扩展 | ❌ 已放弃 | 装不上就不用 |

**分工**：Obsidian 里读写 + Copilot 讲解 → DocsGPT 查本地库交叉验证 → Zotero 存 PDF 和 BibTeX → Claude Code 写代码。
