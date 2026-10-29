#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读腾讯文档智能文档的完整 MDX（分页），落到本地文件。
用法: python3 td_read.py <file_id> <out.mdx>
"""
import sys, json, subprocess

TOOL = "connector__tencentdocs__smartcanvas.read"


def call(args, timeout=120):
    p = subprocess.run(
        ["mcode-tools", "connector", "call", TOOL, "--args", json.dumps(args, ensure_ascii=False)],
        capture_output=True, text=True, timeout=timeout)
    out = p.stdout.strip()
    if not out:
        raise RuntimeError("empty stdout: " + (p.stderr or "")[:200])
    o = json.loads(out)
    if isinstance(o, list) and o and isinstance(o[0], dict) and o[0].get("type") == "text":
        o = json.loads(o[0]["text"])
    if not isinstance(o, dict):
        raise RuntimeError("unexpected: " + str(o)[:200])
    if o.get("error"):
        raise RuntimeError("api error: " + str(o["error"])[:200])
    return o


def read_all(file_id, page_id=""):
    parts, token, pages = [], "", 0
    while True:
        a = {"file_id": file_id, "size": 20}
        if page_id:
            a["page_id"] = page_id
        if token:
            a["next_token"] = token
        o = call(a)
        c = o.get("content") or ""
        parts.append(c)
        pages += 1
        token = o.get("next_token") or ""
        if not token or pages > 60:
            break
    return "\n".join(parts), pages


if __name__ == "__main__":
    fid, out = sys.argv[1], sys.argv[2]
    mdx, pages = read_all(fid)
    with open(out, "w", encoding="utf-8") as f:
        f.write(mdx)
    print("pages=%d chars=%d -> %s" % (pages, len(mdx), out))
