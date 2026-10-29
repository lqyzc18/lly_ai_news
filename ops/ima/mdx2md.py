#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""腾讯文档 MDX → 标准 Markdown（供 ima 笔记 / 知识库使用）

降级映射：
  Heading(level=N)      → #×N
  Paragraph             → 纯文本段
  Callout(icon/color)   → 引用块（>），icon 保留为前缀
  BulletedList          → "- item"（★ 腾讯文档里 BulletedList 本身就是「一项」，
                          文本直接挂在标签里、没有 BulletedListItem 子标签；
                          但也兼容「包着 ListItem」的常规结构）
  NumberedList          → "1. item"
  Table/Row/Cell        → Markdown 表格
  BlockQuote            → "> "
  Mark(color/bold)      → 去掉颜色标签保留文本；bold → **文本**
  frontmatter           → 丢弃（标题写在正文 H1）
  所有 id="..." 属性     → 丢弃；无值属性（readonly/bold…）→ 补 "true"

★ 关键坑：XML 元素的 **tail**（闭合标签后的紧邻文本）必须拼回去，否则
  `<Mark>x</Mark>：后半句` 会只剩「x」，`归档口径：<Mark>…</Mark>——…` 会丢开头。
用法: python3 mdx2md.py <in.mdx> <out.md>
"""
import sys, re
import xml.etree.ElementTree as ET

BOOL_ATTRS = ("readonly", "disabled", "checked", "selected", "bold", "italic",
              "underline", "strike", "hidden", "open", "loop", "autoplay",
              "muted", "controls", "default", "multiple", "required")


def fix_attrs(s):
    s = re.sub(r'\s+id="[^"]*"', "", s)
    pat = re.compile(r'\s(' + "|".join(BOOL_ATTRS) + r')(?=[\s/>])')
    s = pat.sub(r' \1="true"', s)
    return s


def node_text(el):
    """元素内联文本：el.text + 各子元素文本 + 各子元素的 tail（不含 el 自己的 tail）"""
    parts = []
    if el.text:
        parts.append(el.text)
    for c in el:
        if c.tag == "Mark":
            t = c.text or ""
            if c.get("bold") is not None:
                t = "**%s**" % t
            parts.append(t)
        else:
            parts.append(node_text(c))
        if c.tail:
            parts.append(c.tail)
    return "".join(parts)


def para_text(el):
    """块内文本。★ 只有块级子元素（Paragraph）才分段；内联标签（Mark/Link）
    及其 tail 属于同一段连续文本，必须拼在一起，否则一句话会被切成两行。"""
    segs, cur = [], []
    if el.text:
        cur.append(el.text)
    for c in el:
        if c.tag == "Paragraph":
            if cur:
                segs.append(one_line("".join(cur))); cur = []
            segs.append(one_line(node_text(c)))
        else:
            cur.append(node_text(c))
            if c.tail:
                cur.append(c.tail)
    if cur:
        segs.append(one_line("".join(cur)))
    return "\n\n".join(x for x in segs if x)


def one_line(s):
    return re.sub(r"\s*\n\s*", " ", (s or "")).strip()


def node_md(el):
    tag = el.tag
    if tag == "Heading":
        lvl = int(el.get("level", "1") or 1)
        return "\n" + "#" * lvl + " " + one_line(node_text(el)) + "\n"
    if tag == "Paragraph":
        return one_line(node_text(el)) + "\n"
    if tag == "Callout":
        icon = el.get("icon") or ""
        inner = para_text(el)
        head = (icon + " ") if icon else ""
        lines = (head + inner).split("\n")
        return "\n" + "\n".join(("> " + l) if l.strip() else ">" for l in lines) + "\n"
    if tag == "BlockQuote":
        inner = para_text(el)
        return "\n" + "\n".join(("> " + l) if l.strip() else ">" for l in inner.split("\n")) + "\n"
    if tag in ("BulletedList", "NumberedList"):
        items = [c for c in el if c.tag in ("BulletedListItem", "NumberedListItem")]
        lines = []
        if items:
            for i, it in enumerate(items, 1):
                lines.append(("- " if tag == "BulletedList" else "%d. " % i) + one_line(node_text(it)))
        else:
            t = one_line(node_text(el))
            if t:
                lines.append(("- " if tag == "BulletedList" else "1. ") + t)
        return "\n" + "\n".join(lines) + "\n"
    if tag == "Table":
        rows = []
        for tr in el:
            if tr.tag != "TableRow":
                continue
            cells = [one_line(node_text(tc)).replace("|", "\\|")
                     for tc in tr if tc.tag == "TableCell"]
            if cells:
                rows.append(cells)
        if not rows:
            return ""
        n = max(len(r) for r in rows)
        rows = [r + [""] * (n - len(r)) for r in rows]
        out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * n]
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
        return "\n" + "\n".join(out) + "\n"
    if tag in ("ColumnList", "Column"):
        return "".join(node_md(c) for c in el)
    if tag in ("Divider", "Image"):
        return ""
    # 其它：按子块拼
    if len(el):
        return "".join(node_md(c) for c in el)
    return one_line(el.text or "")


def convert(mdx):
    s = mdx
    # ★ smartcanvas.read 分页返回时每页都带一份 frontmatter ⇒ 全部删掉（不只第一份）
    s = re.sub(r"(?m)^---\s*\n.*?\n---\s*\n", "", s, flags=re.S)
    s = fix_attrs(s)
    s = re.sub(r"&nbsp;", " ", s)
    body = "<root>" + s + "</root>"
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        s = re.sub(r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", s)
        root = ET.fromstring("<root>" + s + "</root>")
    md = "".join(node_md(c) for c in root)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md.strip() + "\n"


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    t = open(src, encoding="utf-8").read()
    md = convert(t)
    open(dst, "w", encoding="utf-8").write(md)
    print("mdx=%d chars -> md=%d chars -> %s" % (len(t), len(md), dst))
