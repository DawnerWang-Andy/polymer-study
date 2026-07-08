---
name: zotero
description: >-
  项目级 Zotero 入口 skill。触发场景：当任务涉及 Zotero 文献库
  检索、导入、加笔记、生成 BibTeX、与 Obsidian 双向同步，或者用户直接
  提到 "Zotero"、"参考文献"、"文献库"、"BibTeX" 时使用。这个 skill
  只做“路由 + 起手代码”，具体重活分派给下方三条链路。
metadata:
  scope: project
  layer: router
---

# Zotero 项目路由 skill

polymer-study 项目里的 Zotero 相关任务统一从这里进入。三条链路各司其职，
不要绕开这份文档自行组装。

## 链路总览

| 场景 | 首选链路 | 备用 |
|------|---------|------|
| Python 里用代码读/写 Zotero（脚本、Jupyter、批量操作） | `scripts/zotero_client.py`（本地封装，见下文） | `sci-pyzotero` skill |
| Zotero → Obsidian（`02-科研地图/文献笔记/`）自动生成/更新文献卡 | `scholar-zotero-obsidian-bridge` skill | 手动 `literature-note` skill |
| 只想查一下某本书/某篇论文在不在库里 | `Zotero 桌面 Local API`（`http://127.0.0.1:23119`）+ curl | wrapper 里的 `search()` |
| 大批量整理、去重、审计 | `zotero-library-curator` skill（只读审计） | wrapper 循环 |

## 起手代码（首选）

```python
from scripts.zotero_client import ZoteroClient

zc = ZoteroClient.from_env()          # 读 .env
zc.search("high entropy MOF")          # 返回 items，字段已展平
zc.get_item("ABCD1234")                # 按 item key
zc.add_note("ABCD1234", "<p>要点：...</p>")
zc.list_collection("Polymer Physics")  # 支持 collection name 或 key
zc.export_bibtex(["ABCD1234", ...])    # 导出 BibTeX 字符串
```

wrapper 内部先探测 Zotero 桌面 Local API（快、免 key），失败再回落 Web API。
用户库 write 操作走 Web API，因此需要 `.env` 里有 key。

## 凭证配置

`.env` 至少要有：

```
ZOTERO_API_KEY=xxxx        # https://www.zotero.org/settings/keys
ZOTERO_LIBRARY_ID=1234567  # 同页面 "Your userID for use in API calls"
ZOTERO_LIBRARY_TYPE=user   # user | group
# 可选：Zotero 桌面 Local API 端口，默认 23119
ZOTERO_LOCAL_API=http://127.0.0.1:23119
```

`.env.example` 已经列出这些字段，克隆后 `cp .env.example .env` 补上真实值即可。

## 何时不用这个 skill

- 只想查一段 ACS/Nature 引用格式 → 用 `nature-citation`
- 只想抓 arXiv 全文 → 用 `nature-reader` / arxiv MCP
- 只想在 Obsidian 里手写一张文献卡 → 用 `literature-note` skill

## references

- `references/api-cheatsheet.md` — pyzotero + Local API 常用调用速查
- `references/mapping.md` — Zotero 字段 → Obsidian frontmatter 映射
