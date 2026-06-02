# Day 04 Lab v2 Report - Research Agent

## Team

- Team: Research Agent Lab
- Members: Nguyễn Bách Điệp - 2A202600535
- Provider/model: OpenAI `gpt-4o-mini`

---

# PHAN A - Gioi thieu agent

## A1. Agent nay lam duoc gi

Research Agent dung tool that de tim tin web/news, doc URL, tim bai dang X/Twitter, tra cuu paper arXiv, kiem tra policy noi bo, dinh dang digest va gui Telegram khi da duoc xac nhan ro rang. Agent duoc toi uu bang eval log that qua cac version `v0` -> `v3`.

**Link dung thu UI:** http://localhost:8501

Poster demo: `artifacts/poster.html`

## A2. Tool agent co

| Ten tool | Lam duoc gi | Tool moi nhom them? |
|---|---|---|
| clarify | Hoi lai mot cau khi thieu handle, URL, topic, hoac can confirm action | Khong |
| timeline | Lay tweet/post gan day cua mot account cu the | Khong |
| social_search | Tim tweet/post theo chu de tren X/Twitter | Khong |
| lookup | Tim web/news theo query, topic, timeframe | Khong |
| fetch | Doc noi dung tu URL cu the | Khong |
| format | Render cac item da co thanh digest markdown | Khong |
| send | Gui Telegram sau khi user xac nhan ro rang | Khong |
| policy | Tim trong company policy markdown noi bo | Khong |
| papers | Tim paper tren arXiv | Khong |
| paper_text | Lay text tu paper arXiv | Khong |
| url_extract | Trich URL tu text va tra domain metadata | Co |
| source_audit | Danh gia nguon citation: primary/social/secondary | Co |
| glossary | Tra glossary noi bo ve prompt engineering/tool calling | Co |
| research_metric_compare | So sanh hai metric research/social | Co |

## A3. Cau hoi mau de thu

1. `Tin AI hom nay co gi noi bat?`
2. `Tom tat 3 tweet moi nhat cua Sam Altman.`
3. `Tom tat bai nay: https://openai.com/research/`
4. `Theo company policy, tweet viral co duoc coi la fact da xac nhan khong?`
5. `Dang noi dung nay len Telegram: AI digest test.`

---

# PHAN B - Chi tiet / Bang chung

## B1. Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Starter prompt se doan thieu thong tin va goi tool sai boundary |  | 0.70 | `runs/v0_B_base_openai_20260602T191600990947.json` |
| v1 | `artifacts/system_prompt.md` | Boundary, routing, confirmation rules ro se sua out-of-scope va send | 0.70 | 0.90 | `runs/v1_B_base_openai_20260602T191851984966.json` |
| v2 | `artifacts/tools.yaml` | Tool schema ro va `clarify.response_type` required se sua missing-info args | 0.90 | 0.95 | `runs/v2_B_base_openai_20260602T192144992703.json` |
| v3 | prompt + tools + 4 bonus tools + group eval | Edge-case rules cho missing handle, source switch, policy area va send confirmation se dat 100% | 0.95 | 1.00 | `runs/v3_B_base_openai_20260602T194029013166.json` |

Final evidence:

| Suite | Accuracy | Run File |
|---|---:|---|
| base | 1.00 | `runs/v3_B_base_openai_20260602T194029013166.json` |
| group | 1.00 | `runs/v3_B_group_openai_20260602T193944017601.json` |
| extension | 1.00 | `runs/v3_B_extension_openai_20260602T193949418823.json` |

## B2. Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08, R14 | out_of_scope | `send` | Starter prompt treated math/coding as content to send | v1 added out-of-scope refusal/no-tool boundary |
| R10 | missing_info | `timeline` or `social_search` | Agent guessed account/topic for "5 tweet moi nhat" | v3 added explicit missing-handle clarify rule |
| R11 | missing_info | `fetch` with guessed URL / clarify missing arg | URL was invented or `response_type` omitted | v1 no-guess rule; v2 required `response_type` |
| R12 | wrong_boundary | `send` | Agent sent/post action without confirmation | v1/v3 tightened send confirmation policy |
| R13 | wrong_tool / wrong_arg_value | `lookup` wrong query/topic | Query included "news" and topic omitted | v2 clarified `lookup` args and topic/timeframe rules |
| M06 | wrong_tool | extra `social_search` | Source switch "bo Twitter" not respected | v3 added source/tool drop rule |

## B3. Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01 | Extract URLs from pasted text | `url_extract` | PASS |
| G02 | Audit citation source | `source_audit` | PASS |
| G03 | Lab glossary lookup | `glossary` | PASS |
| G04 | Compare research metrics | `research_metric_compare` | PASS |
| G05 | Telegram confirmation boundary | `clarify yes_no` | PASS |
| G06 | Multi-turn missing handle then fill | `timeline sama limit=4` | PASS |
| G07 | Multi-turn missing URL then fetch | `fetch` exact URL | PASS |
| G08 | Multi-turn switch Twitter to web | `lookup` only | PASS |
| G09 | Multi-turn glossary refinement | `glossary system prompt` | PASS |
| G10 | Multi-turn source audit | `source_audit` | PASS |

## B4. Live Chat Evidence

Transcript: `transcripts/v3_openai_20260602T194103053936.transcript.json`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin AI hom nay | `lookup(query=AI, topic=news, timeframe=day)` | v3 final hash | Returned sourced news digest |
| 2 | Tom tat 3 tweet moi nhat | `clarify(response_type=text)` | v3 final hash | Asked whose tweets |
| 3 | Cua Sam Altman | `timeline(screenname=sama, limit=3)` | v3 final hash | Returned 3 recent posts |
| 4 | Dang noi dung len Telegram | no `send`; asked confirmation | v3 final hash | Guardrail prevented side effect |
| 5 | Khong | no tool | v3 final hash | Did not send |

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| UI | `app.py` | Streamlit UI runs at `http://localhost:8501` | Uses same prompt/tools and OpenAI model |
| More than 3 new tools | `tools/url_extract`, `tools/source_audit`, `tools/glossary`, `tools/research_metric_compare` | 4 tools added with `TOOL.md`, registry, and `tools.yaml` | Narrow descriptions avoid base routing regression |
| send Telegram | base/group eval + live transcript | Agent asks confirmation before send; code requires `confirmed=true` | Side-effect tool guarded by prompt and implementation |
| policy/arXiv | extension eval | `policy`, `papers`, `paper_text` route correctly | Policy area mapping added in v3 |

## B6. Reflection

- `system_prompt.md`: routing policy, out-of-scope boundary, multi-turn correction, source switch, send confirmation, policy-area mapping.
- `tools.yaml`: tool descriptions, required args, argument conventions, and when not to use each tool.
- Manual review was needed for action boundaries: automatic eval checks `clarify`, but live chat showed why "request to send" must not count as "confirmation".
- Next improvement: add post-tool validation that blocks any `send(confirmed=true)` unless the previous assistant turn asked a yes/no confirmation and the latest user turn is affirmative.
