#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""腾讯文档《每日 AI 大事件》当日篇 → ima 笔记 → ima 知识库（按年目录）一条龙。

用法:
  python3 td2ima.py --file-id <腾讯文档file_id> --date 2026-10-28 \
      --kb-id ima_kb_mgx6wDbn --year 2026 [--title "2026-10-28 AI 大事件"] [--dry]

链路:
  1) smartcanvas.read 分页读全文 MDX          → /tmp/td_<date>.mdx
  2) mdx2md.py 降级成标准 Markdown              → /tmp/td_<date>.md
  3) ima import_doc 建笔记（content_format=1）
  4) ima add_knowledge(media_type=11) 挂进年份目录（folder_id 由 --year 解析）
  5) 读回校验（target_content_format=1，ima 的纯文本模式会吞换行，不能用于校验）
"""
import os, sys, json, re, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def sh(cmd, timeout=200):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file-id", required=True)
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--kb-id", required=True)
    ap.add_argument("--year", required=True)
    ap.add_argument("--title", default=None)
    ap.add_argument("--dry", action="store_true", help="只转换不写 ima")
    a = ap.parse_args()

    title = a.title or ("%s AI 大事件" % a.date)
    mdx_p = "/tmp/td_%s.mdx" % a.date
    md_p = "/tmp/td_%s.md" % a.date

    # 1) 读腾讯文档 MDX
    rc, out, err = sh(["python3", os.path.join(HERE, "td_read.py"), a.file_id, mdx_p])
    if rc != 0:
        sys.exit("[FATAL] 读腾讯文档失败: %s %s" % (out[-300:], err[-300:]))
    print(out.strip())

    # 2) 转 Markdown
    rc, out, err = sh(["python3", os.path.join(HERE, "mdx2md.py"), mdx_p, md_p])
    if rc != 0:
        sys.exit("[FATAL] MDX→MD 失败: %s %s" % (out[-300:], err[-300:]))
    print(out.strip())

    md = open(md_p, encoding="utf-8").read()
    content = ("# %s\n\n> 来源：腾讯文档《每日 AI 大事件》· %s 汇总\n\n" % (title, title)) + md
    print("待写入 %d 字符" % len(content))
    if a.dry:
        print("[dry] 未写入 ima")
        return

    # 3) 建笔记 + 4) 挂年份目录
    rc, out, err = sh(["python3", os.path.join(HERE, "ima_push.py"), "push",
                        "--file", md_p, "--title", title, "--kb-id", a.kb_id, "--year", a.year])
    print(out.strip() or err.strip())
    if rc != 0:
        sys.exit("[FATAL] 推送 ima 失败")
    m = re.search(r"note_id:\s*(\S+)", out)
    print("note_id:", m.group(1) if m else "?")


if __name__ == "__main__":
    main()
