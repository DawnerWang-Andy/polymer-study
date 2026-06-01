#!/usr/bin/env python3
"""通用记忆系统 — 全 Agent 共享的文件级记忆 CLI。

任何 Agent（Claude Code / Codex / Pi / Aider / Hermes / Copaw 等）
只需通过 shell 调用本脚本即可读写记忆，无需 MCP 或专用插件。

用法:
  python scripts/memory.py add <name> <description>  添加记忆
  python scripts/memory.py search <query>             搜索记忆
  python scripts/memory.py recall <name>              回忆特定记忆
  python scripts/memory.py list                       列出所有记忆
  python scripts/memory.py forget <name>              删除记忆
  python scripts/memory.py context [query]            获取上下文（供 Agent 注入）
  python scripts/memory.py sync                       同步 claude-mem 记忆

输出格式: 默认 Markdown；加 --json 输出 JSON。
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---- 配置 ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = PROJECT_ROOT / ".memory"
CLAUDE_MEM_DIR = Path.home() / ".claude" / "projects" / "-Users-dawnerwang-polymer-study" / "memory"
MEMORY_INDEX_FILE = MEMORY_DIR / "MEMORY.md"

VALID_TYPES = {"user", "feedback", "project", "reference"}


# ---- 核心函数 ----

def _frontmatter_parse(content: str) -> tuple[dict, str]:
    """解析 YAML frontmatter，返回 (metadata, body)。"""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    meta = {}
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            meta[key] = val
    return meta, parts[2].strip()


def _frontmatter_dump(metadata: dict, body: str) -> str:
    """生成带 YAML frontmatter 的 Markdown。"""
    lines = ["---"]
    for k, v in metadata.items():
        if isinstance(v, dict):
            lines.append(f"{k}:")
            for sk, sv in v.items():
                lines.append(f"  {sk}: {sv}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(body)
    return "\n".join(lines) + "\n"


def _slugify(name: str) -> str:
    """生成 kebab-case slug。"""
    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")


def _read_memory(path: Path) -> Optional[dict]:
    """读取单个记忆文件，返回 {name, description, type, content, path, mtime}。"""
    if not path.exists() or not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8")
    meta, body = _frontmatter_parse(raw)
    return {
        "name": meta.get("name", path.stem),
        "description": meta.get("description", ""),
        "type": _extract_type(meta),
        "content": body,
        "path": str(path),
        "mtime": path.stat().st_mtime,
    }


def _extract_type(meta: dict) -> str:
    """从 metadata 提取 type 字段。"""
    if "metadata" in meta and isinstance(meta["metadata"], dict):
        return meta["metadata"].get("type", "reference")
    return meta.get("type", "reference")


def _all_memories() -> list[dict]:
    """读取所有记忆文件。"""
    memories = []
    if not MEMORY_DIR.exists():
        return memories
    for f in sorted(MEMORY_DIR.iterdir()):
        if f.suffix == ".md" and f.name != "MEMORY.md":
            mem = _read_memory(f)
            if mem:
                memories.append(mem)
    return memories


def _write_memory(name: str, description: str, mem_type: str, content: str) -> Path:
    """写入记忆文件。"""
    slug = _slugify(name)
    metadata = {
        "name": slug,
        "description": description,
        "metadata": {
            "node_type": "memory",
            "type": mem_type,
            "origin": "universal-memory-cli",
        },
    }
    full = _frontmatter_dump(metadata, content)
    filepath = MEMORY_DIR / f"{slug}.md"
    filepath.write_text(full, encoding="utf-8")
    return filepath


def _update_index():
    """重建 MEMORY.md 索引。"""
    memories = _all_memories()
    lines = ["# Memory Index", ""]
    for m in sorted(memories, key=lambda x: x["name"]):
        lines.append(f"- [{m['name']}]({m['name']}.md) — {m['description']}")
    if not memories:
        lines.append("（暂无记忆）")
    lines.append("")
    MEMORY_INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")


# ---- 命令实现 ----

def cmd_add(args):
    """添加记忆。"""
    if args.type not in VALID_TYPES:
        print(f"错误: type 必须是 {VALID_TYPES} 之一", file=sys.stderr)
        sys.exit(1)

    content = args.content
    if args.stdin:
        content = sys.stdin.read().strip()

    if not content:
        print("错误: 需要提供内容（--content 或管道输入）", file=sys.stderr)
        sys.exit(1)

    filepath = _write_memory(args.name, args.description, args.type, content)
    _update_index()

    if args.json:
        print(json.dumps({"status": "added", "name": args.name, "path": str(filepath)}))
    else:
        print(f"已添加记忆: {args.name} → {filepath}")


def cmd_search(args):
    """搜索记忆。"""
    query = args.query.lower()
    memories = _all_memories()
    results = []
    for m in memories:
        score = 0
        if query in m["name"].lower():
            score += 10
        if query in m["description"].lower():
            score += 5
        if query in m["content"].lower():
            score += 3
        if score > 0:
            m["score"] = score
            results.append(m)

    results.sort(key=lambda x: x["score"], reverse=True)
    limit = args.limit or len(results)

    if args.json:
        output = [{"name": r["name"], "description": r["description"],
                    "type": r["type"], "score": r["score"]} for r in results[:limit]]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("未找到相关记忆。")
            return
        for r in results[:limit]:
            print(f"## {r['name']} ({r['type']}) — 相关度: {r['score']}")
            print(f"  {r['description']}")
            print()


def cmd_recall(args):
    """回忆特定记忆。"""
    slug = _slugify(args.name)
    filepath = MEMORY_DIR / f"{slug}.md"
    mem = _read_memory(filepath)
    if not mem:
        # 模糊搜索
        memories = _all_memories()
        for m in memories:
            if args.name.lower() in m["name"].lower():
                mem = m
                break
    if not mem:
        print(f"未找到记忆: {args.name}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(mem, ensure_ascii=False, indent=2))
    else:
        print(Path(mem["path"]).read_text(encoding="utf-8"))


def cmd_list(args):
    """列出所有记忆。"""
    memories = _all_memories()
    if args.type:
        memories = [m for m in memories if m["type"] == args.type]

    if args.json:
        print(json.dumps([{"name": m["name"], "description": m["description"],
                            "type": m["type"]} for m in memories],
                         ensure_ascii=False, indent=2))
    else:
        if not memories:
            print("（暂无记忆）")
            return
        for m in memories:
            print(f"- [{m['type']}] {m['name']} — {m['description']}")


def cmd_forget(args):
    """删除记忆。"""
    slug = _slugify(args.name)
    filepath = MEMORY_DIR / f"{slug}.md"
    if not filepath.exists():
        print(f"未找到记忆: {args.name}", file=sys.stderr)
        sys.exit(1)
    filepath.unlink()
    _update_index()
    print(f"已删除记忆: {args.name}")


def cmd_context(args):
    """输出上下文文本，供 Agent 注入 system prompt。"""
    memories = _all_memories()
    query = args.query.lower() if args.query else None

    if query:
        # 按相关性排序
        scored = []
        for m in memories:
            score = 0
            if query in m["name"].lower():
                score += 10
            if query in m["description"].lower():
                score += 5
            if query in m["content"].lower():
                score += 3
            if score > 0:
                scored.append((score, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        memories = [m for _, m in scored]

    limit = args.limit or len(memories)

    if args.json:
        print(json.dumps([{"name": m["name"], "description": m["description"],
                            "type": m["type"], "content": m["content"][:500]}
                          for m in memories[:limit]], ensure_ascii=False, indent=2))
    else:
        lines = ["## 相关记忆", ""]
        for m in memories[:limit]:
            lines.append(f"### [{m['type']}] {m['name']}")
            lines.append(f"_{m['description']}_")
            lines.append("")
            lines.append(m["content"][:800])
            lines.append("")
        print("\n".join(lines))


def cmd_sync(args):
    """从 claude-mem 同步记忆到通用记忆系统。"""
    if not CLAUDE_MEM_DIR.exists():
        print("claude-mem 目录不存在，跳过同步。")
        return

    count = 0
    for f in CLAUDE_MEM_DIR.iterdir():
        if f.suffix == ".md" and f.name != "MEMORY.md":
            dest = MEMORY_DIR / f.name
            if not dest.exists():
                dest.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
                count += 1

    _update_index()
    print(f"同步完成: {count} 条新记忆已导入。")


def cmd_prompt(args):
    """输出 Agent 接入提示词 — 复制到任意 Agent 的 system prompt 即可使用记忆系统。"""
    prompt_file = MEMORY_DIR / "AGENT_PROMPT.md"
    if prompt_file.exists():
        print(prompt_file.read_text(encoding="utf-8"))
    else:
        print("提示词文件不存在: .memory/AGENT_PROMPT.md", file=sys.stderr)
        sys.exit(1)


# ---- CLI 入口 ----

def main():
    parser = argparse.ArgumentParser(
        description="通用记忆系统 — 全 Agent 共享的记忆 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/memory.py add "论文方向" "大创项目使用GNN预测聚合物性质" --type project
  python scripts/memory.py search "GNN"
  python scripts/memory.py recall "论文方向"
  python scripts/memory.py list --type project
  python scripts/memory.py forget "旧想法"
  python scripts/memory.py context "聚合物 机器学习"
  python scripts/memory.py sync
  echo "内容来自管道" | python scripts/memory.py add "新记忆" "描述" --stdin
        """,
    )
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    sub = parser.add_subparsers(dest="command", help="命令")

    # add
    p_add = sub.add_parser("add", help="添加记忆")
    p_add.add_argument("name", help="记忆名称（会转成 slug）")
    p_add.add_argument("description", help="简短描述")
    p_add.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_add.add_argument("--type", default="reference", choices=VALID_TYPES,
                       help="记忆类型 (默认: reference)")
    p_add.add_argument("--content", help="记忆内容（或使用 --stdin 从管道读取）")
    p_add.add_argument("--stdin", action="store_true", help="从标准输入读取内容")

    # search
    p_search = sub.add_parser("search", help="搜索记忆")
    p_search.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_search.add_argument("query", help="搜索关键词")
    p_search.add_argument("--limit", type=int, help="最大返回数")

    # recall
    p_recall = sub.add_parser("recall", help="回忆特定记忆")
    p_recall.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_recall.add_argument("name", help="记忆名称")

    # list
    p_list = sub.add_parser("list", help="列出所有记忆")
    p_list.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_list.add_argument("--type", choices=VALID_TYPES, help="按类型过滤")

    # forget
    p_forget = sub.add_parser("forget", help="删除记忆")
    p_forget.add_argument("name", help="要删除的记忆名称")

    # context
    p_ctx = sub.add_parser("context", help="获取上下文（供 Agent 注入）")
    p_ctx.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_ctx.add_argument("query", nargs="?", help="可选过滤关键词")
    p_ctx.add_argument("--limit", type=int, help="最大返回数")

    # sync
    p_sync = sub.add_parser("sync", help="从 claude-mem 同步记忆")

    # prompt
    p_prompt = sub.add_parser("prompt", help="输出 Agent 接入提示词")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    commands = {
        "add": cmd_add,
        "search": cmd_search,
        "recall": cmd_recall,
        "list": cmd_list,
        "forget": cmd_forget,
        "context": cmd_context,
        "sync": cmd_sync,
        "prompt": cmd_prompt,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
