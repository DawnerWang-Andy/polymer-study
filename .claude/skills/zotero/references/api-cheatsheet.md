# Zotero API 速查（本项目常用）

面向 polymer-study 项目里最常见的几件事，只列会真的用到的。
完整文档见 [pyzotero](https://pyzotero.readthedocs.io/) 和
[Zotero Web API v3](https://www.zotero.org/support/dev/web_api/v3/start)。

## 一、pyzotero 起手

```python
from pyzotero import zotero
zot = zotero.Zotero(library_id, library_type, api_key)
```

`library_type` 只有两种：`'user'`（个人库）、`'group'`（群组库）。

## 二、检索

| 目的 | 调用 |
|------|------|
| 关键词全文检索 | `zot.items(q='high entropy MOF', qmode='everything', limit=25)` |
| 只搜标题 | `zot.items(q='...', qmode='titleCreatorYear')` |
| 按 tag | `zot.items(tag='polymer-physics')` |
| 按 collection | `zot.collection_items(coll_key)` |
| 最近添加 | `zot.top(sort='dateAdded', direction='desc', limit=10)` |

Zotero 桌面 Local API 也支持等价的 `items?q=`（免鉴权，只读）：
```
GET http://127.0.0.1:23119/api/users/0/items?q=MOF&qmode=everything&format=json
```

## 三、创建条目（Web API）

```python
tpl = zot.item_template('journalArticle')  # 拿模板
tpl['title'] = 'A high-entropy MOF...'
tpl['creators'] = [{'creatorType': 'author', 'firstName': 'X', 'lastName': 'Wang'}]
tpl['DOI'] = '10.1038/s41563-024-...'
tpl['publicationTitle'] = 'Nature Materials'
tpl['date'] = '2025-03'
zot.create_items([tpl])
```

Zotero 支持的 itemType 全表：`zot.item_types()`。项目常用：
`journalArticle` / `preprint` / `book` / `bookSection` / `thesis` /
`conferencePaper` / `report` / `webpage`。

## 四、附加子笔记（HTML）

```python
note = zot.item_template('note')
note['note'] = '<h2>核心结论</h2><p>...</p>'
zot.create_items([note], parentid='ABCD1234')  # 挂到父条目
```

## 五、Collection

| 目的 | 调用 |
|------|------|
| 列出全部 | `zot.collections()` |
| 按名字查 | 手动 `[c for c in zot.collections() if c['data']['name'] == 'Polymer Physics']` |
| 新建 | `zot.create_collections([{'name': 'HE-MHOF'}])` |
| 把条目移入 | `zot.addto_collection(coll_key, item)` |

## 六、导出 BibTeX / Citation

Pyzotero 侧：
```python
zot.item(item_key, format='bibtex')                 # 单条 BibTeX
zot.items(collection=coll_key, format='bibtex')     # 一整个 collection
zot.item(item_key, format='bib', style='nature')    # 格式化引用（HTML）
```

Local API 侧（桌面开着更快）：
```
GET http://127.0.0.1:23119/api/users/0/items/{key}?format=bibtex
```

## 七、速率与坑

- Web API 有 rate limit，批量写建议每 100 条 `time.sleep(1)`。
- 本地库 items 里 tags 是 `[{'tag': 'foo'}, ...]`，写回也用这个结构。
- `library_id` 传字符串更稳（避免整数溢出）。
- 中文 tag 没问题，但 collection name 里的 `/` 会被 Zotero 当成层级分隔，慎用。
