"""zotero_client.py — polymer-study 项目 Zotero 薄封装。

设计原则：
    - 读优先走 Zotero 桌面 Local API（免鉴权、快），失败回落 Web API。
    - 写强制走 Web API（Local API 不支持写）。
    - 只包最常用的 5 个动作：search / get_item / list_collection / add_note / export_bibtex。
    - 不做重业务，重业务留给上层 skill / 脚本。

使用：
    from scripts.zotero_client import ZoteroClient
    zc = ZoteroClient.from_env()
    zc.search("high entropy MOF")

依赖：
    pip install pyzotero python-dotenv requests
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import requests

try:
    from dotenv import load_dotenv
except ImportError:  # 允许不装 dotenv，直接读 os.environ
    def load_dotenv(*_args, **_kwargs):  # noqa: D401
        """dotenv 缺失时的空实现。"""
        return False

try:
    from pyzotero import zotero
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "缺少 pyzotero。请运行: pip install pyzotero"
    ) from exc


DEFAULT_LOCAL_API = "http://127.0.0.1:23119"


@dataclass
class ZoteroClient:
    """Zotero 客户端，Local + Web 双通道。

    Attributes:
        library_id: Zotero 用户或群组 ID（字符串更稳）。
        library_type: 'user' 或 'group'。
        api_key: Web API 密钥；只做本地读时可以为空。
        local_api: 桌面 Local API URL，未启用时会被跳过。
    """

    library_id: str
    library_type: str = "user"
    api_key: Optional[str] = None
    local_api: str = DEFAULT_LOCAL_API

    def __post_init__(self) -> None:
        # Web 客户端只在有 key 时才建，避免误用
        self._web = (
            zotero.Zotero(self.library_id, self.library_type, self.api_key)
            if self.api_key
            else None
        )
        self._local_alive: Optional[bool] = None  # 懒探测

    # ------------------------------------------------------------------ 构造

    @classmethod
    def from_env(cls, env_path: str | Path | None = None) -> "ZoteroClient":
        """从 .env 装载凭证。

        Args:
            env_path: 指定 .env 路径；默认查找项目根目录。

        Returns:
            初始化好的 ZoteroClient。

        Raises:
            RuntimeError: 缺 ZOTERO_LIBRARY_ID。
        """
        if env_path is None:
            # 默认 .env 在 scripts/ 上一级
            env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(env_path)

        lib_id = os.getenv("ZOTERO_LIBRARY_ID")
        if not lib_id:
            raise RuntimeError(
                "缺少 ZOTERO_LIBRARY_ID。请在 .env 中配置，参考 .env.example。"
            )
        return cls(
            library_id=lib_id,
            library_type=os.getenv("ZOTERO_LIBRARY_TYPE", "user"),
            api_key=os.getenv("ZOTERO_API_KEY"),
            local_api=os.getenv("ZOTERO_LOCAL_API", DEFAULT_LOCAL_API),
        )

    # ------------------------------------------------------------------ 通道

    def _local_ok(self) -> bool:
        """探测 Zotero 桌面 Local API 是否可用。"""
        if self._local_alive is not None:
            return self._local_alive
        try:
            r = requests.get(f"{self.local_api}/api/", timeout=1.5)
            self._local_alive = r.status_code < 500
        except requests.RequestException:
            self._local_alive = False
        return self._local_alive

    def _local_get(self, path: str, **params) -> requests.Response:
        """构造 Local API 请求。"""
        # Local API 用 0 代替 library_id
        url = f"{self.local_api}/api/{self.library_type}s/0/{path}"
        return requests.get(url, params=params, timeout=10)

    def _require_web(self) -> zotero.Zotero:
        if self._web is None:
            raise RuntimeError(
                "此操作需要 Web API。请在 .env 中配置 ZOTERO_API_KEY。"
            )
        return self._web

    # ------------------------------------------------------------------ 读

    def search(
        self,
        query: str,
        *,
        limit: int = 25,
        qmode: str = "everything",
    ) -> list[dict]:
        """全文/元数据检索，返回条目 dict 列表。

        Local 优先，Web 兜底。返回值字段与 Zotero API 原生一致，
        取常用信息看 ``item["data"]``。
        """
        params = {"q": query, "qmode": qmode, "limit": limit, "format": "json"}
        if self._local_ok():
            r = self._local_get("items", **params)
            if r.ok:
                return r.json()
        return self._require_web().items(**params)

    def get_item(self, item_key: str) -> dict:
        """按 item key 取单条。"""
        if self._local_ok():
            r = self._local_get(f"items/{item_key}", format="json")
            if r.ok:
                return r.json()
        return self._require_web().item(item_key)

    def list_collection(self, name_or_key: str) -> list[dict]:
        """按 collection 名字或 key 列出条目。"""
        web = self._require_web()
        # 名字要先反查
        if len(name_or_key) != 8 or not name_or_key.isalnum():
            hits = [
                c for c in web.collections()
                if c["data"]["name"] == name_or_key
            ]
            if not hits:
                raise ValueError(f"未找到 collection: {name_or_key}")
            coll_key = hits[0]["key"]
        else:
            coll_key = name_or_key
        return web.collection_items(coll_key)

    # ------------------------------------------------------------------ 写

    def add_note(self, parent_key: str, html: str) -> dict:
        """给条目挂一条 HTML 子笔记。"""
        web = self._require_web()
        tpl = web.item_template("note")
        tpl["note"] = html
        result = web.create_items([tpl], parentid=parent_key)
        # Zotero 返回 {'successful': {'0': {...}}, 'failed': {...}, ...}
        if result.get("failed"):
            raise RuntimeError(f"add_note 失败: {result['failed']}")
        return result["successful"]["0"]

    def batch_create(
        self,
        items: Iterable[dict],
        *,
        chunk: int = 50,
        sleep: float = 1.0,
    ) -> list[dict]:
        """批量创建条目，自带 rate limit 保护。"""
        web = self._require_web()
        buf: list[dict] = []
        results: list[dict] = []
        for i, it in enumerate(items, 1):
            buf.append(it)
            if i % chunk == 0:
                results.extend(web.create_items(buf).get("successful", {}).values())
                buf.clear()
                time.sleep(sleep)
        if buf:
            results.extend(web.create_items(buf).get("successful", {}).values())
        return results

    # ------------------------------------------------------------------ 导出

    def export_bibtex(self, item_keys: Iterable[str]) -> str:
        """把一组条目导出为 BibTeX 字符串。

        单条走 Local API 更快，多条批量走 Web API 的 collection format。
        """
        chunks: list[str] = []
        for key in item_keys:
            if self._local_ok():
                r = self._local_get(f"items/{key}", format="bibtex")
                if r.ok:
                    chunks.append(r.text)
                    continue
            chunks.append(self._require_web().item(key, format="bibtex"))
        return "\n\n".join(chunks)


# ---------------------------------------------------------------------- CLI

def _cli() -> None:  # pragma: no cover
    """轻量 CLI：``python scripts/zotero_client.py search "MOF"``。"""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Zotero 项目薄封装 CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="全文检索")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=10)

    p_get = sub.add_parser("get", help="按 key 取单条")
    p_get.add_argument("key")

    p_bib = sub.add_parser("bibtex", help="导出 BibTeX")
    p_bib.add_argument("keys", nargs="+")

    p_ping = sub.add_parser("ping", help="探测 Local / Web 连通性")

    args = ap.parse_args()
    zc = ZoteroClient.from_env()

    if args.cmd == "search":
        items = zc.search(args.query, limit=args.limit)
        for it in items:
            data = it.get("data", it)
            print(f"[{data.get('key','?')}] {data.get('title','(no title)')}")
    elif args.cmd == "get":
        print(json.dumps(zc.get_item(args.key), ensure_ascii=False, indent=2))
    elif args.cmd == "bibtex":
        print(zc.export_bibtex(args.keys))
    elif args.cmd == "ping":
        print(f"Local API 可用: {zc._local_ok()}")
        print(f"Web API 可用:   {zc._web is not None}")


if __name__ == "__main__":  # pragma: no cover
    _cli()
