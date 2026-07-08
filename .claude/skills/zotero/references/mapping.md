# Zotero → Obsidian 文献卡字段映射

polymer-study 使用 EverOS 工作流，文献卡统一落在
`02-科研地图/文献笔记/{citekey}.md`。这份映射决定 `zotero_client.py`
的 `to_obsidian_frontmatter()` 怎么输出。

## Frontmatter 字段

| Obsidian frontmatter | Zotero 字段 | 说明 |
|----------------------|-------------|------|
| `title` | `title` | 原文标题 |
| `authors` | `creators`（author 型） | 数组，格式 `Last, First` |
| `year` | `date` 前 4 位 | 无 date 时留空 |
| `journal` | `publicationTitle` / `bookTitle` / `conferenceName` | 取第一个非空 |
| `doi` | `DOI` | |
| `zotero_key` | `key` | 后续 wrapper 反查用 |
| `citekey` | Better BibTeX citation key（若装了 BBT） | 无 BBT 时 fallback：`firstAuthorLastName + year + firstWordOfTitle` |
| `tags` | `tags[].tag` | 数组，中文 tag 保留 |
| `type` | `itemType` | e.g. journalArticle |
| `added` | `dateAdded` | 保留 ISO 时间 |
| `abstract` | `abstractNote` | 塞进 `> [!abstract]` callout 而不是 frontmatter，避免超长 |
| `collections` | 反查 `zot.collections()` | 数组，用中文名 |

## 正文骨架

```markdown
---
（上面那些字段）
---

> [!abstract]
> {{abstractNote}}

## 核心贡献
- 
- 

## 方法要点
- 

## 我的评述
- 

## 参考
- Zotero: [[zotero://select/library/items/{{zotero_key}}]]
- DOI: https://doi.org/{{doi}}
```

## 命名与去重

- 文件名用 `citekey`（BBT 优先，否则 wrapper 兜底算法），不要用中文标题。
- 已存在同名文件时：如果 `zotero_key` 相同 → 增量更新 frontmatter，正文不动；不同 → 加 `-2`、`-3` 后缀，不覆盖。

## 反向同步

从 Obsidian 里给条目加 tag / 移入 collection 的做法：修改 frontmatter 里的
`tags` / `collections` 后运行 `python scripts/zotero_client.py sync-back <file>`，
wrapper 会把差分写回 Zotero。摘要 (`abstract`)、正文不做反向写回，
避免 Zotero 那边被 Obsidian 覆盖。
