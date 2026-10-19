# 2026 年 1—10 月日报体检报告（跨档重复 + 来源可达性）

- 范围：`202601/` ~ `202607/`、`202609/`、`202610/`，**共 261 篇**（`202608/` 正在由另一路 worker 写入，本次排除）。
- 性质：**只查不改**。本报告只列证据与建议动作，所有改动需 PM 确认后执行。
- 扫描方法与阈值：标题 token 交集 ≥3 且正文 5-gram Jaccard ≥0.15 判为跨档疑似重复；来源可达性用浏览器 UA 实抓 1982 个唯一 URL，区分真 404 与反爬（403/429/5xx）与超时。

## 0. 结论速览

| 检查项 | 结果 |
|:--|:--|
| 跨档疑似重复（同一事件写两遍） | **0 对**（标题 token + 5-gram Jaccard 0.15 阈值，261 篇两两比对） |
| 同一来源被 **≥5 篇** 引用 | **0 个**（无「一个来源盖多篇」的重灾） |
| 同一来源被 **相邻 2~3 天连续** 引用 | **35 处** ← 最强灌水/占位信号，见 §1 |
| 栏目页/早报/榜单页当来源 | **17 个 URL** 被 ≥2 篇引用，见 §2 |
| 来源 404（真死链） | **82 条** |
| 来源 403/429/5xx（反爬，未判定死活） | 196 条 |
| 来源超时/连接失败（未判定） | 149 条 |

**总体判断：2026 年的稿子在「重复」这一项上明显好于 2025 年**——2025-04~06 我用同一套方法查出的 6 组「同一事件写两遍」，在 2026 年 261 篇里没有复现。**真正的问题集中在来源侧**：35 处「同一 URL 连续两天以上被引用」，以及 82 条 404 死链。

## 1. 同一来源被相邻多天连续引用（35 处）——占位/灌水稿的外部信号

判定：同一 URL 出现在**日期相邻（±2 天）**的两篇及以上里。正常情况下一个来源只应支撑一天的事件；连续三天引用同一页，通常意味着其中几天是把那一页当兜底在用。

| # | 涉及日期 | 引用篇数 | URL | 来源性质 | 建议动作 |
|:--|:--|--:|:--|:--|:--|
| 1 | 2026-04-28, 2026-04-29, 2026-04-30 | 3 | `https://aibars.net/zh-Hant/news/837985384569901056` | 聚合站（繁体、纯数字 id） | 换官方一手页 |
| 2 | 2026-06-20, 2026-06-22, 2026-06-23 | 3 | `https://c.m.163.com/news/a/L03NVC5L05118BEE.html` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 3 | 2026-02-14, 2026-02-15, 2026-02-16 | 3 | `https://m.163.com/dy/article/KLQ4UCBM05118BEE.html` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 4 | 2026-02-14, 2026-02-15, 2026-02-16 | 3 | `https://m.toutiao.com/a1857151048801675/` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 5 | 2026-02-11, 2026-02-12, 2026-02-13 | 3 | `https://news.sina.cn/2026-02-12/detail-inhmpyyf6844807.d.html?vt=4` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 6 | 2026-04-04, 2026-04-05, 2026-04-06 | 3 | `https://txtmix.com/posts/news/ai-news-morning-2026-04-04` | 每日早报页 | **换事件级一手页** |
| 7 | 2026-04-04, 2026-04-05, 2026-04-06 | 3 | `https://www.duoke360.com/post/46133` | 聚合站文章页 | 换官方博客/newsroom |
| 8 | 2026-04-05, 2026-04-06, 2026-04-07 | 3 | `https://www.kunaledge.com/news` | **栏目页**（无文章 id） | 换成具体文章页；栏目页不可作为来源 |
| 9 | 2026-04-04, 2026-04-05, 2026-04-06 | 3 | `https://www.theneuron.ai/explainer-articles/-around-the-horn-digest-everything-that-happened-in-` | 周末汇总 digest（标题含 weekend/around the horn） | **改为对应事件的一手页**；周末稿本身只应归 1 天 |
| 10 | 2026-03-01, 2026-03-03 | 2 | `http://quitgpt.org/press-openai-protest` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 11 | 2026-04-07, 2026-04-08 | 2 | `https://ai-news-daily--ms-workspace-b3c.camelai.app/articles/49` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 12 | 2026-09-04, 2026-09-05 | 2 | `https://aiproducthub.cn/newsflash/2026-09-05/` | **栏目页**（newsflash 列表） | 换成具体快讯页 |
| 13 | 2026-02-17, 2026-02-19 | 2 | `https://article-factory.ai/news/waymo-teams-with-lyft-to-launch-robotaxi-service-in-nashville-by` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 14 | 2026-02-13, 2026-02-15 | 2 | `https://c.m.163.com/news/a/KLLU3A6905118BEE.html` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 15 | 2026-02-09, 2026-02-10 | 2 | `https://datapipe.app?p=435/` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 16 | 2026-05-02, 2026-05-03 | 2 | `https://gagadget.com/en/707937-meta-acquires-robotics-ai-startup-ari-to-build-the-android-of-hum` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 17 | 2026-04-22, 2026-04-24 | 2 | `https://gcp.infoq.cn/Details/2168.html` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 18 | 2026-07-01, 2026-07-02 | 2 | `https://h5.ifeng.com/c/vivo/v002KJI6-_y--ENpVRj9ij2uPwlfHRFkKPdXpod-_plXciK8mI__` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 19 | 2026-02-06, 2026-02-07 | 2 | `https://i.ifeng.com/c/8qW5G0yPptW` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 20 | 2026-01-26, 2026-01-27 | 2 | `https://jnzstatic.cs.com.cn/zzb/htmlInfo/114562.html` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 21 | 2026-01-26, 2026-01-27 | 2 | `https://m.cnfin.com/gs-lb/zixun/20260126/4371193_1.html` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 22 | 2026-05-22, 2026-05-23 | 2 | `https://m.cnyes.com/news/id/6466773` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 23 | 2026-05-12, 2026-05-13 | 2 | `https://m.tmtpost.com/7984060.html` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 24 | 2026-07-26, 2026-07-27 | 2 | `https://new.qq.com/rain/a/20260727A02PVP00` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 25 | 2026-06-26, 2026-06-27 | 2 | `https://saassentinel.com/2026/06/27/openai-releases-gpt-5-6-sol-terra-and-luna-to-limited-partne` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 26 | 2026-01-25, 2026-01-26 | 2 | `https://stcn.com/article/detail/3615760.html` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 27 | 2026-04-22, 2026-04-24 | 2 | `https://stcn.com/article/detail/3789568.html` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 28 | 2026-05-30, 2026-05-31 | 2 | `https://thenextweb.com/news/anthropic-mythos-eu-enisa-cybersecurity-access` | 权威媒体文章页（本身可用） | **仅需确认引用那天的事件确实发生** |
| 29 | 2026-03-17, 2026-03-18 | 2 | `https://www.axios.com/2026/03/16/tech-industry-rallies-anthropic-pentagon-fight` | 权威媒体文章页（本身可用） | **仅需确认引用那天的事件确实发生** |
| 30 | 2026-06-12, 2026-06-14 | 2 | `https://www.nfnews.com/content/VoQVOmQLy5.html` | 文章页 | 确认该事件是否重复出现在多篇；若否，保留一次即可 |
| 31 | 2026-07-26, 2026-07-27 | 2 | `https://www.toutiao.com/a7666977837706707496` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 32 | 2026-02-17, 2026-02-18 | 2 | `https://www.toutiao.com/article/7607633963154227722/` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 33 | 2026-02-24, 2026-02-25 | 2 | `https://www.toutiao.com/article/7610936442461618739` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 34 | 2026-02-18, 2026-02-19 | 2 | `https://www.toutiao.com/w/1857507518132362/` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |
| 35 | 2026-02-20, 2026-02-21 | 2 | `https://www.toutiao.com/w/1857689384533003/` | 聚合转载页（网易/头条/凤凰/腾讯/新浪/钛媒体） | 换原始报道或一手页 |

### 1.1 优先处理（同一来源连续 3 天 + 属汇总/栏目/聚合页）

以下 5 处是「连续三天 + 汇总/栏目页」叠加，最可能是兜底式引用：

- **https://aibars.net/zh-Hant/news/837985384569901056** —— 被 2026-04-28、2026-04-29、2026-04-30 连续引用。该页是汇总/栏目页，按规范应替换为该事件的一手页。
- **https://txtmix.com/posts/news/ai-news-morning-2026-04-04** —— 被 2026-04-04、2026-04-05、2026-04-06 连续引用。该页是汇总/栏目页，按规范应替换为该事件的一手页。
- **https://www.duoke360.com/post/46133** —— 被 2026-04-04、2026-04-05、2026-04-06 连续引用。该页是汇总/栏目页，按规范应替换为该事件的一手页。
- **https://www.kunaledge.com/news** —— 被 2026-04-05、2026-04-06、2026-04-07 连续引用。该页是汇总/栏目页，按规范应替换为该事件的一手页。
- **https://www.theneuron.ai/explainer-articles/-around-the-horn-digest-everything-that-happened-in-ai-t** —— 被 2026-04-04、2026-04-05、2026-04-06 连续引用。该页是汇总/栏目页，按规范应替换为该事件的一手页。

## 2. 栏目页 / 早报页 / 榜单页当来源（17 个 URL）

这类 URL 指向的是「一个栏目」而不是「一篇文章」，无法核验它支撑了哪条具体事实。

| URL | 涉及篇数 | 涉及文件 |
|:--|--:|:--|
| `https://www.theneuron.ai/explainer-articles/-around-the-horn-digest-everything-that-happened` | 3 | 2026-04-04.md, 2026-04-05.md, 2026-04-06.md |
| `https://txtmix.com/posts/news/ai-news-morning-2026-04-04` | 3 | 2026-04-04.md, 2026-04-05.md, 2026-04-06.md |
| `https://www.kunaledge.com/news` | 3 | 2026-04-05.md, 2026-04-06.md, 2026-04-07.md |
| `https://aibars.net/zh-Hant/news/837985384569901056` | 3 | 2026-04-28.md, 2026-04-29.md, 2026-04-30.md |
| `https://arena.ai/leaderboard/code/webdev` | 2 | 2026-05-27.md, 2026-10-19.md |
| `https://aiproducthub.cn/newsflash/2026-09-05/` | 2 | 2026-09-04.md, 2026-09-05.md |
| `https://alignment.openai.com/misalignment-reports/` | 2 | 2026-10-11.md, 2026-10-17.md |
| `https://aibars.net/zh-Hant/news/800312808272171008` | 1 | 2026-01-19.md |
| `https://unwire.pro/2026/01/28/eu-launches-proceedings-google-android-ai-data/news/` | 1 | 2026-01-28.md |
| `https://unwire.pro/2026/01/30/apple-acquires-qai-2-billion-ai-wearables-silent-speech/news` | 1 | 2026-01-30.md |
| `https://leaderboard.mteb.org/models/codefuse-ai/F2LLM-v2-80M` | 1 | 2026-03-26.md |
| `https://aibars.net/en/news/844515027498176512` | 1 | 2026-05-20.md |
| `https://www.odaily.news/zh-TW/newsflash/495706` | 1 | 2026-06-30.md |
| `https://aibars.net/zh-Hant/news/868159513935613952` | 1 | 2026-07-16.md |
| `https://arena.ai/leaderboard/code/webdev?license=open-source` | 1 | 2026-10-19.md |
| `https://arena.ai/company/leaderboard-changelog` | 1 | 2026-10-19.md |
| `https://artificialanalysis.ai/leaderboards/models/` | 1 | 2026-10-19.md |

## 3. 来源 404 死链（82 条）

按域名聚合（`zglg.work` 一族 20 余条为同一站批量失效，优先整站替换）：

| 域名 | 死链条数 | 样例 |
|:--|--:|:--|
| `zglg.work` | 75 | `https://zglg.work/ai/news/zh/2026-08-31-forbes-report-details-openai-agents-` |
| `article-factory.ai` | 1 | `https://article-factory.ai/news/waymo-teams-with-lyft-to-launch-robotaxi-ser` |
| `finance.sina.cn` | 1 | `https://finance.sina.cn/headline/2026-04-11/detail-inhuauvh7666520.d.html` |
| `m.163.com` | 1 | `https://m.163.com/dy/article/KL0ILPQF05118BWE.html` |
| `stcn.com` | 1 | `https://stcn.com/article/detail/3661050.html` |
| `wallstreetobserver.com` | 1 | `https://wallstreetobserver.com/nvidias-plan-to-invest/` |
| `www.afp.com` | 1 | `https://www.afp.com/en/openai-says-three-staffers-fired-mishandling-sensitiv` |
| `www.kut.org` | 1 | `https://www.kut.org/business/2026-03-22/austin-tx-elon-musk-ai-chip-terrafab` |

全部 404 明细：

```
https://article-factory.ai/news/waymo-teams-with-lyft-to-launch-robotaxi-service-in-nashville-by-2026-2
https://finance.sina.cn/headline/2026-04-11/detail-inhuauvh7666520.d.html
https://m.163.com/dy/article/KL0ILPQF05118BWE.html
https://stcn.com/article/detail/3661050.html
https://wallstreetobserver.com/nvidias-plan-to-invest/
https://www.afp.com/en/openai-says-three-staffers-fired-mishandling-sensitive-info-0
https://www.kut.org/business/2026-03-22/austin-tx-elon-musk-ai-chip-terrafab-tesla-spacex
https://zglg.work/ai/news/zh/2026-08-31-forbes-report-details-openai-agents-hugging-face-attack-70-000-agent-messages
https://zglg.work/ai/news/zh/2026-08-31-the-pentagon-is-adding-its-own-versions-of-chatgpt-and-grok-to-its-central-ai
https://zglg.work/ai/news/zh/2026-09-01-anthropic-paused-some-ai-training-after-claude-took-unauthorized-actions
https://zglg.work/ai/news/zh/2026-09-01-openai-to-limit-astra-model-release-over-hacking-concerns-report-says
https://zglg.work/ai/news/zh/2026-09-02-anthropic-admits-security-failures-behind-ai-hacking-incidents-says-models-no
https://zglg.work/ai/news/zh/2026-09-02-meta-releases-muse-spark-1-3-its-most-powerful-ai-model-yet-as-chief-ai-offic
https://zglg.work/ai/news/zh/2026-09-03-nvidia-agrees-to-acquire-hugging-face-for-12-9-billion
https://zglg.work/ai/news/zh/2026-09-03-openai-launches-astra-its-powerful-and-controversial-new-model
https://zglg.work/ai/news/zh/2026-09-03-tencent-open-sources-hunyuan-hy4-preview-in-an-open-source-ai-push
https://zglg.work/ai/news/zh/2026-09-05-deepseek-orders-160-000-huawei-ascend-950dt-chips-moving-inference-under-chin
https://zglg.work/ai/news/zh/2026-09-05-hikers-rescued-after-using-google-gemini-for-planning
https://zglg.work/ai/news/zh/2026-09-05-lg-unveils-thinq-claw-a-chat-based-ai-agent-for-the-smart-home-at-ifa-2026
https://zglg.work/ai/news/zh/2026-09-07
https://zglg.work/ai/news/zh/2026-09-07-gpt-6-astra-sol-6
https://zglg.work/ai/news/zh/2026-09-08-deepseek-v4-1-flash-oschina-ai-oschina
https://zglg.work/ai/news/zh/2026-09-08-meta-debuts-its-muse-ai-agent-will-consumers-trust-it
https://zglg.work/ai/news/zh/2026-09-08-the-work-now-within-reach
https://zglg.work/ai/news/zh/2026-09-09-suno-replaces-its-ai-models-with-a-new-one-trained-on-licensed-music-as-copyr
https://zglg.work/ai/news/zh/2026-09-10-ai-research-startup-listen-labs-scrubbed-a-1-5b-funding-round-for-salesforce
https://zglg.work/ai/news/zh/2026-09-10-meta-s-ai-agent-muse-is-now-the-no-2-app-in-the-us
https://zglg.work/ai/news/zh/2026-09-10-official-model-update-deepseek-ai-deepseek-v4-1-flash
https://zglg.work/ai/news/zh/2026-09-10-openai-pauses-pro-subscriptions-as-astra-demand-strains-capacity
https://zglg.work/ai/news/zh/2026-09-11-twenty-five-fields-medalists-sign-an-open-letter-warning-ai-labs-are-threaten
https://zglg.work/ai/news/zh/2026-09-11-zhipu-s-glm-ocr-model-update-tops-omnidocbench-v1-5-at-0-9b-parameters
https://zglg.work/ai/news/zh/2026-09-12-anthropic-ceo-dario-amodei-we-must-slow-the-pace-of-improving-ai-models
https://zglg.work/ai/news/zh/2026-09-13-house-speaker-johnson-rejects-an-ai-moratorium-china-will-overlap-us
https://zglg.work/ai/news/zh/2026-09-13-nasa-and-ibm-release-open-source-lunar-foundation-model-trained-on-30-data-la
https://zglg.work/ai/news/zh/2026-09-13-zhipu-raises-about-5-billion-to-fund-next-gen-glm-self-training-and-compute
https://zglg.work/ai/news/zh/2026-09-14-deepseek-routes-all-v4-pro-api-traffic-to-v4-1-flash-at-flash-rates
https://zglg.work/ai/news/zh/2026-09-14-deepseek-v4-1-flash-552b-parameter-moe-built-for-efficient-inference
https://zglg.work/ai/news/zh/2026-09-14-huang-takes-a-live-trump-call-onstage-we-re-not-going-to-let-an-ai-slowdown-h
https://zglg.work/ai/news/zh/2026-09-14-microsoft-s-new-ai-code-of-conduct-tells-models-not-to-hack-systems-or-trick
https://zglg.work/ai/news/zh/2026-09-15-aws-puts-openai-s-gpt-6-astra-on-bedrock-for-business-customers
https://zglg.work/ai/news/zh/2026-09-15-google-s-new-speech-model-gemini-3-8-live-supports-real-time-reasoning
https://zglg.work/ai/news/zh/2026-09-16-bytedance-ships-feishu-8-0-and-doubao-work-partner-as-office-collaboration-en
https://zglg.work/ai/news/zh/2026-09-16-openai-releases-model-misalignment-reporting-framework-discloses-six-incident
https://zglg.work/ai/news/zh/2026-09-16-openai-unveils-sponsored-agents-and-new-ad-tools-with-hubspot-and-shopify-int
https://zglg.work/ai/news/zh/2026-09-17-crusoe-raises-3-9b-at-a-30-9b-valuation-to-build-mega-data-centers-and-modula
https://zglg.work/ai/news/zh/2026-09-17-tang-jie-releases-zhipu-s-first-rsi-result-as-glm-takes-part-in-building-glm
https://zglg.work/ai/news/zh/2026-09-17-watchdog-alleges-openai-violated-california-s-sb-53-in-three-model-releases
https://zglg.work/ai/news/zh/2026-09-18-anthropic-confirms-it-runs-a-wet-biology-lab-to-test-its-ai-models-for-real
https://zglg.work/ai/news/zh/2026-09-18-anthropic-rebuilds-claude-code-projects-around-parallel-cloud-agents
https://zglg.work/ai/news/zh/2026-09-18-gemini-hacked-three-companies-in-first-known-breakout-by-google-s-ai-wsj-repo
https://zglg.work/ai/news/zh/2026-09-18-researchers-used-anthropic-s-claude-to-hack-into-openai
https://zglg.work/ai/news/zh/2026-09-19-google-s-gemini-is-the-latest-ai-model-reported-to-have-hacked-other-companie
https://zglg.work/ai/news/zh/2026-09-19-terence-tao-launches-sair-foundation-s-open-math-model-initiative
https://zglg.work/ai/news/zh/2026-09-19-trump-suggests-rebranding-ai-with-a-new-name-says-he-s-also-creating-an-ai-fo
https://zglg.work/ai/news/zh/2026-09-20-anthropic-builds-a-san-francisco-biology-lab-and-puts-claude-on-the-robots
https://zglg.work/ai/news/zh/2026-09-21-amazon-blocks-meta-s-muse-ai-agent-from-shopping-on-its-site-as-agentic-comme
https://zglg.work/ai/news/zh/2026-09-21-google-confirms-gemini-models-hacked-three-companies-pushing-ai-security-into
https://zglg.work/ai/news/zh/2026-09-21-openai-forms-math-advisory-group-as-its-ai-resolves-more-than-100-open-proble
https://zglg.work/ai/news/zh/2026-09-21-qwen-open-sources-qwen-image-2-1-a-7b-visual-generator-that-unifies-text-to-i
https://zglg.work/ai/news/zh/2026-09-21-roboharm-robot-safety-benchmark-gpt-6-astra-tried-dangerous-actions-in-97-of
https://zglg.work/ai/news/zh/2026-09-22-anthropic-releases-opus-5-5-with-lower-prices-and-fable-level-performance
https://zglg.work/ai/news/zh/2026-09-22-meta-admits-muse-s-likeness-to-openclaw-isn-t-a-coincidence
https://zglg.work/ai/news/zh/2026-09-22-openai-launches-gpt-6-sol-and-luna-pitching-lower-cost-and-fewer-mistakes
https://zglg.work/ai/news/zh/2026-09-22-reuters-alibaba-plans-a-5t-to-10t-parameter-ai-model-and-unveils-a-new-chip
https://zglg.work/ai/news/zh/2026-09-23-anthropic-says-its-biology-lab-found-a-crispr-like-enzyme-system
https://zglg.work/ai/news/zh/2026-09-24-australia-to-investigate-whether-openai-linked-hack-of-a-government-health-we
https://zglg.work/ai/news/zh/2026-09-24-meta-goes-all-in-on-its-ai-agent-muse-at-connect
https://zglg.work/ai/news/zh/2026-09-24-okta-led-alliance-urges-a-kill-switch-for-ai-agents
https://zglg.work/ai/news/zh/2026-09-24-report-openai-agent-hacked-an-australian-health-website-in-unprecedented-inci
https://zglg.work/ai/news/zh/2026-09-24-un-security-council-confronts-ai-risks-as-u-s-rejects-a-global-regulator
https://zglg.work/ai/news/zh/2026-09-25-anthropic-commits-11-6-billion-to-akamai-in-seven-year-cloud-deal
https://zglg.work/ai/news/zh/2026-09-25-astra-and-claude-opus-5-crack-two-long-unsolved-enigma-messages
https://zglg.work/ai/news/zh/2026-09-25-openai-admits-unsecured-agents-posted-53-user-images-on-public-image-hosts
https://zglg.work/ai/news/zh/2026-09-26-openai-confirms-self-replicating-prompt-injections-exist
https://zglg.work/ai/news/zh/2026-09-27-australia-summons-altman-and-amodei-after-ai-agents-breach-controls-and-leak
https://zglg.work/ai/news/zh/2026-09-27-maxine-waters-demands-openai-investigation-and-a-halt-to-new-ai-model-release
https://zglg.work/ai/news/zh/2026-09-27-openai-pauses-training-of-latest-models-after-agents-searched-u-s-government
https://zglg.work/ai/news/zh/2026-09-28-alibaba-unveils-zhenwu-v900-data-center-gpu-claiming-triple-the-performance-o
https://zglg.work/ai/news/zh/2026-09-28-anthropic-releases-claude-sonnet-5-5-calling-it-a-cheaper-faster-work-partner
https://zglg.work/ai/news/zh/2026-09-28-meta-s-muse-agent-reportedly-closed-a-marketplace-sale-and-shared-a-seller-s
https://zglg.work/ai/news/zh/2026-09-28-openai-reportedly-withholds-a-new-model-over-safety-concerns
https://zglg.work/ai/news/zh/2026-09-29-openai-apologizes-over-incidents-involving-australian-government-websites
```

## 4. 反爬 / 超时（196 + 149 条，未判定死活）

这些 URL 用浏览器 UA 抓取返回 403/429/5xx 或直接超时，**不能据此判定是死链**；其中不少是海外站点的正常反爬（如 nvidia.com、openai.com、techcrunch.com 的部分路径）。本报告只列分布，不建议据此改动来源。

| 分类 | 条数 | 主要域名（前 8） |
|:--|--:|:--|
| 403/429/5xx | 196 | baike.baidu.com(25)、openai.com(22)、www.cnii.com.cn(7)、chen-blog-sigma.vercel.app(5)、caip.org.cn(4)、ai.ettoday.net(3)、aiwiki.ai(3)、arena.ai(3) |
| 超时/连接失败 | 149 | — |

## 5. 跨档重复扫描：未发现（0 对）

用与 2025-04~06 相同的两把尺子：

1. **标题 token 级**：把每节标题按「与/和/的/及/在」切词，跨月两篇交集 ≥3 词 → 疑似；
2. **正文 5-gram Jaccard**：去空白后取 5-gram 集合，两两算 Jaccard，阈值 0.15。

结果：**0 对**。2025-04~06 用同一套方法查出了 6 组「同一事件写两遍」（io 收购、Builder.ai、Anthropic 70% 代码、Elephant 基准、o3/Operator/BAGEL、xAI Grok/CoreWeave/RM-Bench），2026 年这 261 篇没有复现该问题。

补充：实体级复现统计里，OpenAI（193 篇）、Anthropic（174 篇）、Claude（95 篇）等高频词属于正常的主题分布，**不构成重复证据**；真正的重复信号已集中在 §1 的同源连续引用上。

## 6. 建议动作清单（按优先级）

| 优先级 | 动作 | 涉及处数 | 说明 |
|:--|:--|--:|:--|
| P0 | 把 §1 中「连续 3 天 + 汇总/栏目/聚合页」的来源替换为事件级一手页 | 5 | 这些是 2026 年稿子里最像「兜底占位」的引用 |
| P0 | 整站替换 `zglg.work` 的来源 | 75 | 同一站批量 404 |
| P1 | 其余 §1 的相邻日同源引用逐条核：该事件是否真的在多篇里各写一遍 | 35 | 若同事件重复，删除后写的一篇 |
| P1 | §2 的栏目页/榜单页换成具体文章页 | 17 | 无法核验支撑关系 |
| P2 | §3 其余 404 逐条换源 | 7 | 含聚合站文章页 |
| P3 | §4 的反爬/超时项**保持不动** | 345 | 浏览器 UA 抓不到不等于死链 |

> 本报告只出清单、不改稿。2026 年是用户验收过的定版稿，任何改动需 PM 确认后执行。

> 扫描脚本：`/workspace/audit2026.py`；中间数据：`/workspace/legacy/audit2026.json`。