# ops/ima — 腾讯文档《每日 AI 大事件》→ 腾讯 ima 知识库

每天 12:20 的独立 cron 任务用这套脚本，把当日腾讯文档篇目推成 ima 笔记并挂进知识库「每日AI大事件」的**年份目录**。

| 文件 | 作用 |
|---|---|
| `td_read.py` | 用 `smartcanvas.read` 分页读腾讯文档智能文档全文 MDX |
| `mdx2md.py` | 腾讯文档 MDX → 标准 Markdown（Callout→引用块、Table→Markdown 表、Mark→文本；修 tail 丢失 / 无值属性 / BulletedList 结构三个坑） |
| `ima_push.py` | ima OpenAPI 客户端：建笔记 / 挂知识库 / 上传文件 / 按年目录（`--year`） |
| `td2ima.py` | 一条龙：`--file-id <腾讯文档file_id> --date YYYY-MM-DD --kb-id <kb> --year YYYY` |

**cron 会话的工作区不共享**，所以脚本从本目录经 GitHub contents API 拉取后本地执行；凭证走平台注入的 secret 环境变量（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` / `GITHUB_TOKEN`）。

关键事实：ima 写入只支持 Markdown（`content_format=1`）；知识库**没有 move / delete 接口**，条目必须在**首次写入**时就带 `folder_id`；读回校验必须用 `target_content_format=1`（`=0` 的纯文本会吞换行）。
