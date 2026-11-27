# ops/lane_log

两条 AI 大事件日报 lane 的**每日运行台账**落点。

**唯一权威落点 = 本目录下的 `YYYY-MM_台账实录归档.md`（按月份一个文件，只追加）**。
台账进版本控制，可 diff、可追溯，跟仓库一起走；**不再依赖 memory topic**（cron lane 的运行环境没有 `memory_topic_append` 工具，2026-11-26/27 实测确认）。

| 文件 | 内容 |
|:--|:--|
| `2026-10_台账实录归档.md` | 2026 年 10 月各次 lane 运行实录 |
| `2026-11_台账实录归档.md` | 2026 年 11 月各次 lane 运行实录 |

## 写入规范

### 路径
- 文件名：`ops/lane_log/YYYY-MM_台账实录归档.md`，月份取 `date` 输出的月份（跨月则新建该月文件）。

### 通道
GitHub Connector 整片不可用（`invalid_provider`），**一律走 REST**，必须带 token 头：
```
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/lqyzc18/lly_ai_news/contents/ops/lane_log/YYYY-MM_%E5%8F%B0%E8%B4%A6%E5%AE%9E%E5%BD%95%E5%BD%92%E6%A1%A3.md"
```
- 返回体里 `content` 是 **base64**，用 `base64 -d` 解码得正文；`sha` 是写入时必须带的版本号。
- **404 = 本月文件尚不存在**，按新建处理（不带 sha 即可）。

### 写入
```
PUT https://api.github.com/repos/lqyzc18/lly_ai_news/contents/ops/lane_log/YYYY-MM_台账实录归档.md
body: {"message":"Append the YYYY-MM-DD run record to the <Month> lane log.",
       "content":"<base64(utf-8 全量正文)>","branch":"main","sha":"<GET 到的 sha>"}
```
- **一次 PUT = 一个 commit**。已有文件必须带 `sha`，否则 422。
- **只追加**：新条目追加到文件末尾，**绝不改写、删除、压缩、重排已有条目**。
- 写完 `GET` 同一路径回读，确认新条目在、且历史条目仍在。

### 条目格式
沿用既有样式：
```
## YYYY-MM-DD（星期X）· 标题

- **产出**：…
- **可复用**：…
- **新踩的坑**：…
```
三类要点各 1~3 行，**正文控制 3~5 行，不复述当天日报全文**。

## 两条 lane 的差异

| lane | 标题前缀 | 产出条目应写什么 |
|:--|:--|:--|
| GitHub 版（12:15） | 仓库 lane | 当天篇路径、节数、来源数、commit 数与 SHA |
| 腾讯文档版（18:00） | 腾讯文档 lane | 文档标题、file_id、目标目录归位结果、是否新建 |

## 硬规则

1. **最多 1 轮、只追加不压缩**。
2. **写失败不重试**：网络/403/422 时如实写一句「本次运行台账未写入仓库（原因：…）」，**绝不重试、绝不压缩历史台账**。台账缺失不影响当天日报与文档的交付。
3. **台账缺失不等于任务失败** —— 判成败看产出物（仓库 commit / 腾讯文档是否建出并归位）。
