#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送日报到腾讯 ima（官方 OpenAPI，Base URL https://ima.qq.com）
鉴权头：ima-openapi-clientid / ima-openapi-apikey

子命令：
  api <path> '<json_body>'      通用调用（任何 endpoint，body 可为空 '{}'）
  note --file X.md --title "T"   新建/写入一篇笔记（content_format=1，Markdown 原样）
  append --note-id ID --file X.md  向已有笔记追加内容
  kb-list                       列出可写入的知识库
  kb-url --kb-id ID --url U     把网页/链接加入知识库
  kb-file --kb-id ID --file F   把本地文件上传进知识库（原始二进制，不转码）
  dry <path> '<json>'           只打印将要发出的请求，不真正发送

凭证来源（优先级）：环境变量 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY
                     → ~/.config/ima/client_id / api_key
所有请求体强制 UTF-8 字节发送，避免中文乱码。
"""
import os, sys, json, base64, uuid, mimetypes, argparse, urllib.request, urllib.error

BASE = "https://ima.qq.com"

# ima OpenAPI 媒体类型枚举（按扩展名，官方 knowledge-base skill 规范）
MEDIA_TYPE = {"pdf": 1, "doc": 3, "docx": 3, "ppt": 4, "pptx": 4, "xls": 5, "xlsx": 5,
              "csv": 5, "md": 7, "markdown": 7, "png": 9, "jpg": 9, "jpeg": 9, "webp": 9,
              "txt": 13, "xmind": 14, "mp3": 15, "m4a": 15, "wav": 15, "aac": 15}
CONTENT_TYPE = {"pdf": "application/pdf", "doc": "application/msword",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "ppt": "application/vnd.ms-powerpoint",
                "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "xls": "application/vnd.ms-excel",
                "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "csv": "text/csv", "md": "text/markdown", "markdown": "text/markdown",
                "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp",
                "txt": "text/plain", "xmind": "application/x-xmind", "mp3": "audio/mpeg",
                "m4a": "audio/x-m4a", "wav": "audio/wav", "aac": "audio/aac"}
# 大小上限（官方规范）
MAX_SIZE = {7: 10 * 1024 * 1024, 13: 10 * 1024 * 1024, 14: 10 * 1024 * 1024, 5: 10 * 1024 * 1024,
             9: 30 * 1024 * 1024}


def creds():
    cid = os.environ.get("IMA_OPENAPI_CLIENTID") or os.environ.get("IMA_CLIENT_ID")
    key = os.environ.get("IMA_OPENAPI_APIKEY") or os.environ.get("IMA_API_KEY")
    if not cid or not key:
        home = os.path.expanduser("~/.config/ima")
        try:
            cid = cid or open(os.path.join(home, "client_id"), encoding="utf-8").read().strip()
        except Exception:
            pass
        try:
            key = key or open(os.path.join(home, "api_key"), encoding="utf-8").read().strip()
        except Exception:
            pass
    if not cid or not key:
        sys.exit("[FATAL] 缺少凭证：需要 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY")
    return cid.strip(), key.strip()


def api(path, body=None, method="POST", raw=False):
    cid, key = creds()
    data = json.dumps(body if body is not None else {}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        BASE + "/" + path.lstrip("/"),
        data=data, method=method,
        headers={
            "ima-openapi-clientid": cid,
            "ima-openapi-apikey": key,
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read()
    except urllib.error.HTTPError as e:
        b = e.read()
        print("[HTTP %s]" % e.code, file=sys.stderr)
    except Exception as e:
        sys.exit("[FATAL] 请求失败: %r" % e)
    if raw:
        return b
    try:
        return json.loads(b.decode("utf-8", "replace"))
    except Exception:
        return {"_raw": b.decode("utf-8", "replace")[:1500]}


def report(tag, r):
    code = r.get("code") if isinstance(r, dict) else None
    ok = code in (0, 200, None) or (isinstance(r, dict) and r.get("data"))
    print("[%s] code=%s msg=%s %s" % (tag, code, r.get("msg"), "OK" if ok else "FAIL"))
    d = r.get("data") if isinstance(r, dict) else None
    if d:
        s = json.dumps(d, ensure_ascii=False)
        print("   data:", s[:600] + ("…" if len(s) > 600 else ""))
    return r


def resolve_year_folder(kb_id, year):
    """按年定位/创建文件夹：先在根目录找 media_type=99 且标题=year 的条目，
    找不到就 create_folder（重名时服务端报 220001，再列一次即可拿到已有 folder_id）。"""
    y = str(year)
    def scan():
        d = (api("openapi/wiki/v1/get_knowledge_list",
                 {"knowledge_base_id": kb_id, "cursor": "", "limit": 50}).get("data") or {})
        for it in d.get("knowledge_list") or []:
            if it.get("media_type") == 99 and str(it.get("title")) == y:
                return it.get("media_id")
        return None
    fid = scan()
    if fid:
        return fid
    r = api("openapi/wiki/v1/create_folder", {"knowledge_base_id": kb_id, "name": y})
    fid = (r.get("data") or {}).get("media_id")
    if not fid:
        fid = scan()
        if not fid:
            sys.exit("[FATAL] 无法创建/定位年份目录 %s（create_folder: %s）" % (y, r.get("msg")))
    print("[folder] %s → %s" % (y, fid))
    return fid


def read_text(p):
    with open(p, "rb") as f:
        b = f.read()
    return b.decode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("api"); p.add_argument("path"); p.add_argument("body", nargs="?", default="{}")
    p = sub.add_parser("note"); p.add_argument("--file", required=True); p.add_argument("--title", required=True)
    p = sub.add_parser("append"); p.add_argument("--note-id", required=True); p.add_argument("--file", required=True)
    p = sub.add_parser("kb-list")
    p = sub.add_parser("kb-url"); p.add_argument("--kb-id", required=True); p.add_argument("--url", required=True)
    p.add_argument("--folder-id", default=None); p.add_argument("--year", default=None)
    p = sub.add_parser("kb-note"); p.add_argument("--kb-id", required=True); p.add_argument("--note-id", required=True)
    p.add_argument("--title", required=True); p.add_argument("--folder-id", default=None); p.add_argument("--year", default=None)
    p = sub.add_parser("push"); p.add_argument("--file", required=True); p.add_argument("--title", required=True)
    p.add_argument("--kb-id", required=True); p.add_argument("--folder-id", default=None); p.add_argument("--year", default=None)
    p = sub.add_parser("kb-file"); p.add_argument("--kb-id", required=True); p.add_argument("--file", required=True)
    p.add_argument("--folder-id", default=None); p.add_argument("--year", default=None)
    p = sub.add_parser("dry"); p.add_argument("path"); p.add_argument("body", nargs="?", default="{}")
    a = ap.parse_args()
    if getattr(a, "year", None) and not getattr(a, "folder_id", None):
        a.folder_id = resolve_year_folder(a.kb_id, a.year)

    if a.cmd == "dry":
        print(json.dumps({"path": a.path, "body": json.loads(a.body)}, ensure_ascii=False, indent=2))
        return
    if a.cmd == "api":
        report("api " + a.path, api(a.path, json.loads(a.body)))
        return
    if a.cmd == "note":
        body = read_text(a.file)
        content = body if body.lstrip().startswith("#") else "# %s\n\n%s" % (a.title, body)
        report("note", api("openapi/note/v1/import_doc", {"content_format": 1, "content": content}))
        return
    if a.cmd == "append":
        report("append", api("openapi/note/v1/append_doc",
                             {"note_id": a.note_id, "content_format": 1, "content": read_text(a.file)}))
        return
    if a.cmd == "kb-list":
        # 实测：limit 取值范围 (0,50]（可写库列表）/ (0,20]（搜索库列表），用 start/end 会报 code=51
        for path, lim in (("openapi/wiki/v1/get_addable_knowledge_base_list", 50),
                          ("openapi/wiki/v1/search_knowledge_base", 20)):
            r = api(path, {"limit": lim, "cursor": ""})
            report("kb-list " + path, r)
            if isinstance(r, dict) and r.get("data"):
                break
        return
    if a.cmd == "kb-url":
        b = {"knowledge_base_id": a.kb_id, "urls": [a.url]}
        if a.folder_id: b["folder_id"] = a.folder_id
        report("kb-url", api("openapi/wiki/v1/import_urls", b))
        return
    if a.cmd == "kb-note":
        b = {"media_type": 11, "note_info": {"content_id": a.note_id},
             "title": a.title, "knowledge_base_id": a.kb_id}
        if a.folder_id: b["folder_id"] = a.folder_id
        report("kb-note", api("openapi/wiki/v1/add_knowledge", b))
        return
    if a.cmd == "push":
        # 一天一条日报的完整链路：import_doc 写笔记 → add_knowledge(media_type=11) 挂进知识库
        body = read_text(a.file)
        content = body if body.lstrip().startswith("#") else "# %s\n\n%s" % (a.title, body)
        r1 = report("import_doc", api("openapi/note/v1/import_doc",
                                      {"content_format": 1, "content": content}))
        note_id = (r1.get("data") or {}).get("note_id")
        if not note_id:
            sys.exit("[FATAL] 未拿到 note_id，停止（不挂知识库）")
        print("   note_id:", note_id)
        b2 = {"media_type": 11, "note_info": {"content_id": note_id},
              "title": a.title, "knowledge_base_id": a.kb_id}
        if a.folder_id: b2["folder_id"] = a.folder_id
        r2 = report("add_knowledge", api("openapi/wiki/v1/add_knowledge", b2))
        print("   media_id:", (r2.get("data") or {}).get("media_id"))
        return
    if a.cmd == "kb-file":
        # 文件型媒体链路（.md/.pdf/.docx/...）：查重名 → create_media → COS 上传 → add_knowledge
        name = os.path.basename(a.file)
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        mt = MEDIA_TYPE.get(ext)
        if mt is None:
            sys.exit("[FATAL] 不支持的文件类型 .%s（视频/B站/YouTube/file:// 只能用 ima 客户端添加）" % ext)
        ctype = CONTENT_TYPE.get(ext, "application/octet-stream")
        chk = {"params": [{"name": name, "media_type": mt}], "knowledge_base_id": a.kb_id}
        if a.folder_id: chk["folder_id"] = a.folder_id
        r1 = report("check_repeated_names", api("openapi/wiki/v1/check_repeated_names", chk))
        for res in ((r1.get("data") or {}).get("results") or []):
            if res.get("is_repeated"):
                print("[WARN] 知识库已有同名文件，ima 不支持覆盖：", name,
                      "→ 需改名（{base}_{ts}.{ext}）或取消")
                sys.exit(2)
        r2 = report("create_media", api("openapi/wiki/v1/create_media",
                                        {"file_name": name,
                                         "file_size": os.path.getsize(a.file),
                                         "content_type": ctype,
                                         "knowledge_base_id": a.kb_id,
                                         "file_ext": ext}))
        d2 = r2.get("data") or {}
        cc = d2.get("cos_credential") or {}
        media_id = d2.get("media_id")
        if not cc or not media_id:
            print("[FATAL] create_media 返回不完整：", json.dumps(d2, ensure_ascii=False)[:400])
            sys.exit(3)
        cos_ok = cos_upload(a.file, cc, ctype)
        if not cos_ok:
            print("[FATAL] COS 上传失败 → 不调用 add_knowledge（按规范必须中止）")
            sys.exit(4)
        ak = {"media_type": mt, "media_id": media_id, "title": name,
              "knowledge_base_id": a.kb_id,
              "file_info": {"cos_key": cc.get("cos_key"),
                            "file_size": os.path.getsize(a.file),
                            "file_name": name}}
        if a.folder_id: ak["folder_id"] = a.folder_id
        report("add_knowledge", api("openapi/wiki/v1/add_knowledge", ak))
        return


def _md5(p):
    import hashlib
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _hmac_sha1(key, msg):
    import hmac, hashlib
    return hmac.new(key.encode(), msg.encode(), hashlib.sha1).digest()


def cos_upload(path, cc, ctype):
    """COS 带临时密钥签名 PUT（q-sign-algorithm=sha1）。
    算法依据腾讯云 COS 文档 + 官方 ima skill 的 cos-upload.cjs：
      SignKey     = HMAC-SHA1(SecretKey, KeyTime)
      HttpString  = method\npathname\n\n<k=v&k=v>\n     (header key 小写、value URL 编码、按 key 排序)
      StringToSign= sha1\nKeyTime\nSHA1(HttpString)\n
      Signature   = HMAC-SHA1(SignKey, StringToSign)
    签名放在 **Authorization 请求头**里（不是 URL query）。
    失败必须中止，不允许继续调 add_knowledge。"""
    import hashlib, hmac, urllib.parse
    bucket = cc.get("bucket_name"); region = cc.get("region"); cos_key = cc.get("cos_key")
    sid = cc.get("secret_id"); skey = cc.get("secret_key"); token = cc.get("token")
    st = str(cc.get("start_time")); et = str(cc.get("expired_time"))
    if not all([bucket, region, cos_key, sid, skey, st, et]):
        print("[FATAL] cos_credential 字段不全：", json.dumps(cc, ensure_ascii=False)[:300])
        return False
    host = "%s.cos.%s.myqcloud.com" % (bucket, region)
    pathname = "/" + str(cos_key).lstrip("/")
    data = open(path, "rb").read()
    key_time = st + ";" + et
    sign_key = hmac.new(skey.encode(), key_time.encode(), hashlib.sha1).hexdigest()
    signed = {"content-length": str(len(data)), "host": host}
    http_headers = "&".join("%s=%s" % (k, urllib.parse.quote(signed[k], safe="")) for k in sorted(signed))
    http_string = "put\n%s\n\n%s\n" % (pathname, http_headers)
    string_to_sign = "sha1\n%s\n%s\n" % (key_time, hashlib.sha1(http_string.encode()).hexdigest())
    signature = hmac.new(sign_key.encode(), string_to_sign.encode(), hashlib.sha1).hexdigest()
    authorization = "&".join([
        "q-sign-algorithm=sha1", "q-ak=%s" % sid, "q-sign-time=%s" % key_time,
        "q-key-time=%s" % key_time, "q-header-list=%s" % ";".join(sorted(signed)),
        "q-url-param-list=", "q-signature=%s" % signature,
    ])
    req = urllib.request.Request("https://%s%s" % (host, pathname), data=data, method="PUT", headers={
        "Content-Type": ctype, "Content-Length": str(len(data)),
        "Authorization": authorization, "x-cos-security-token": token or "",
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            print("[COS upload] HTTP", r.status)
            return r.status in (200, 204)
    except urllib.error.HTTPError as e:
        print("[COS upload] HTTP %s %s" % (e.code, e.read().decode("utf-8", "replace")[:400]), file=sys.stderr)
        return False
    except Exception as e:
        print("[COS upload] 失败:", repr(e)[:200], file=sys.stderr)
        return False


if __name__ == "__main__":
    main()
