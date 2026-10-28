# Sources and verification status

**As of 19 October 2026.** This file collects where the information in the course [Local LLM Engines](README.md) comes from, what is verified, and what is not.

## 1. Method

- **Desk research + code reading.** I did not run or measure anything; the rig's cards are in production use.
- **The web search engine was unavailable** (the session's query limit was exhausted). Sources are project pages, documentation, blog posts, papers (arXiv), Wikipedia, company pages and the **GitHub API** (`gh api`), fetched directly.
- **Source code** I read in shallow clones (`--depth 1`) on the rig, read-only; the pinned commits are below. For projects whose clone had not finished downloading at the time of reading, the GitHub API and raw files were used (marked in the chapters).
- **Stars, licenses, creation dates, contributor counts:** GitHub API, 2026-10-19.
- **Confidence tags in the text:** none = checked in the code or a primary source · *(project's/company's own claim)* = a statement by the party concerned · *(press report)* / *(third-party source)* = a report not confirmed at the source · *(my calculation)* = arithmetic on numbers from the sources · *(unverified)* = a guess.
- **Checks:** the numbers in the chapters passed a scripted test “does this number appear in the notes or in the source” (discrepancies are mostly derived arithmetic); the disputed points from §4 were checked by hand.

## 2. Pinned source trees (commits)

| Project | Commit |
|---|---|
| llama.cpp (production tree) | `0ce8cd11416c8840498e6701bcbe39ad4b858c2b` (2026-10-19) |

| ds4 | `5379c1c9ac315f1540371b06a3db88491d4059ff` |
| dynamo | `c08fa77fcc66e0608f233ba8049bec4149bad5a2` |
| exo | `bc412e2230f395e652c23426a5eb88dfa515769b` |
| ggml | `a05c9922613c6a2230dbb1d0de679519ecafb4f0` |
| ik_llama.cpp | `35e72560fac6eb4e0bedc99976d3a12040749230` |
| jan | `648e8da55438150ccfab78808fa97a7a8e458c9f` |
| koboldcpp | `76e77f34056c51c42435f03faaf9ea1258a7cd68` |
| ktransformers | `a694e718e8b3ec2e221277d674e369f3be38d2a4` |
| lemonade | `c236963ca9ba3635a3ab75dab75cb69690397b98` |
| llama-swap | `a2796fb0306215c6883454a8707dfb22d25c3068` |
| llamafile | `a3ccf098ed9c7c77687f5430b0143156d3bcc45a` |
| llm-d | `e27c2674d70514841b7aca87280fc165d533ecd0` |
| llmman | `d349e730df315262c66557bf65bcd8b2247dfc83` |
| LMCache | `2ef13a37dcd7f816d2737ebcd21a2eb47613bd7d` |
| LocalAI | `ae8092e1c6932a63f1499d28cf58cf7ab0545628` |
| mistral.rs | `465191d0b0a7e2432d327b0de06204ab3f94d3a2` |
| mlc-llm | `8978ea9aec626d64096aaa92fbc89bda2e3ea802` |
| mlx | `f41bec734ac9fc96723ab7d4e64e385796f15561` |
| mlx-lm | `c39139d70f0798834fc721c28a1aa8e1374ea33c` |
| model-runner | `ea783c4f3eaa5d4c2e1d17aee12ade47cb042fe4` |
| ollama | `678722224b3d8c2a024a4fa5f530d83ce34db120` |
| omlx | `c3595bc65981cb097be66471194f3eb47f5a6d8e` |
| ramalama | `a9080556d91cf8e8775487b690a60008cbe632fb` |
| sglang | `aaa9388c91128156a57f4f7ba6abe7457ad62518` |
| TensorRT-LLM | `7695494b8fce4d75aedfaf9dc34b075abe6b1008` |
| text-generation-inference | `b4adbf2f6e2e721280bd0ea5f91d70f7d033f5ed` |
| vllm | `b7701fc3e4b8616353e06b27c95a33463f1f9aa7` |

The clones are shallow — commit history and tag dates come from the GitHub API, not from the clones.

## 3. Sources by chapter

### Chapter 02-JAK-DZIALA-INFERENCJA


**Sources for chapter 02 (all taken from notes/06-fundamentals.md; as of 2026-10-19)**


**The reader's own measurements (course repository)**

- ../speeding-up-generation/README.md
- ../speeding-up-generation/01-HOW-IT-WORKS.md
- ../speeding-up-generation/02-DEEPSEEK-DEPLOYMENT.md

**Prace (arXiv; fetched abstract pages)**

- 2309.06180 (PagedAttention) · 2312.07104 (SGLang/RadixAttention) · 2308.16369 (SARATHI) · 2403.02310 (Sarathi-Serve)
- 2401.09670 (DistServe) · 2311.18677 (Splitwise) · https://www.usenix.org/conference/osdi22/presentation/yu (Orca)
- 2205.14135, 2307.08691, 2407.08608 (FlashAttention 1/2/3) · 2501.01005 (FlashInfer)
- 2405.04434 (DeepSeek-V2/MLA) · 2412.19437 (DeepSeek-V3) · 2512.02556 (DeepSeek-V3.2/DSA)
- 2305.13245 (GQA) · 1911.02150 (MQA) · 2104.09864 (RoPE) · 2309.00071 (YaRN) · 2002.05202 (GLU) · 1910.07467 (RMSNorm)
- 2401.06066 (DeepSeekMoE) · 2401.04088 (Mixtral) · 1909.08053 (Megatron-LM) · 2211.05102 (Pope et al.)
- 2211.17192, 2302.01318 (speculative decoding/sampling) · 2401.10774 (Medusa) · 2401.15077, 2406.16858, 2503.01840 (EAGLE 1/2/3)
- 2402.02057 (Lookahead) · 2602.06036 (DFlash, via z-lab.ai/projects/dflash) · 2411.15100 (XGrammar) · 2307.09702 (Outlines)
- 1904.09751 (nucleus) · 2407.01082 (min-p) · 2202.00666 (typical) · 2007.14966 (Mirostat) · 2411.07641 (top-n-sigma)
- 2402.02750 (KIVI) · 2510.09665 (LMCache)

**Web pages**

- https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
- https://github.com/oobabooga/text-generation-webui (PR 5677 DRY, PR 6335 XTC)
- https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html
- https://en.wikipedia.org/wiki/Radeon_RX_9000_series
- Hugging Face config.json / model card: deepseek-ai/DeepSeek-V3, deepseek-ai/DeepSeek-V4-Flash, Qwen/Qwen3-30B-A3B, openai/gpt-oss-120b, NousResearch/Meta-Llama-3.1-70B
- GitHub API: ggml-org/llama.cpp PR #22105 (DFlash), #25173 (DSpark)

**llama.cpp (build 0ce8cd1, ~/llama.cpp-0ce8cd1)**

- docs/{speculative,multi-gpu,autoparser,llguidance}.md
- common/{arg.cpp,common.h,sampling.cpp,speculative.cpp,reasoning-budget.h,jinja/README.md,parsers/,chat-diff-analyzer.cpp}
- src/{llama-kv-cache*.{h,cpp},llama-graph.cpp,llama-sampler.cpp,llama-grammar.cpp,llama-context.cpp,llama-arch.cpp,llama-moe-cache.h,llama-vocab.cpp,llama-chat.cpp}
- tools/server/{server.cpp,server-context.cpp,server-common.cpp}; tools/llama-bench/README.md; tools/server/bench/speed-bench
- ggml/src/ggml-cuda/{fattn.cu,allreduce.cu}; ggml/src/ggml-backend-meta.cpp; gguf-py/gguf/constants.py

**vLLM (~/runtimes-src/vllm)**

- vllm/v1/core/** (scheduler.py, kv_cache_manager.py, block_pool.py, kv_cache_utils.py); vllm/config/{cache,scheduler,speculative,structured_outputs}.py
- vllm/platforms/rocm.py; vllm/v1/attention/backends/**; vllm/distributed/**; vllm/tool_parsers/; vllm/reasoning/AGENTS.md
- vllm/benchmarks/serve.py; vllm/entrypoints/openai/chat_completion/protocol.py
- docs/features/{tool_calling,structured_outputs,batch_invariance}.md

**SGLang (~/runtimes-src/sglang)**

- python/sglang/srt/{mem_cache/radix_cache.py,managers/schedule_policy.py,managers/scheduler.py,speculative/spec_info.py,layers/attention/,constrained/,batch_invariant_ops/}

**mlx-lm (~/runtimes-src/mlx-lm)**

- mlx_lm/{models/cache.py,generate.py,server.py}

**ds4 (~/runtimes-src/ds4)**

- README.md, MODEL_CARD.md, docs/{SERVER,SPECULATIVE_DECODING,MODELS}.md

**Machine (read-only readings)**

- /sys/class/drm/card*/device/{mem_info_vram_total,pp_dpm_mclk,current_link_speed,current_link_width}; rocminfo

### Chapter 03-KWANTYZACJA-I-FORMATY


**Sources for chapter 03 — Quantization and model formats**


**(paths relative to the trees on the machine with the notes; URLs from the notes)**


**llama.cpp / ggml (tree ~/llama.cpp-0ce8cd1, build 0ce8cd1)**

- ggml/src/ggml-common.h  (static_assert of block_* sizes; QK_K, lines 89, 185-460)
- ggml/include/ggml.h  (enum ggml_type, 43 types)
- ggml/include/gguf.h  (GGUF_MAGIC, GGUF_VERSION 3, GGUF_DEFAULT_ALIGNMENT 32)
- ggml/src/gguf.cpp
- include/llama.h  (ftype: IQ3_XXS=23; loading modes, line approx. 207)
- src/llama-quant.cpp  (mix recipes, lines approx. 465-735; use_more_bits)
- src/llama-model-loader.cpp  (mmap, alignment, lines approx. 560-691)
- convert_hf_to_gguf.py  (--outtype linia 60, --remote, --dspark, --split-max-size)
- conversion/base.py  (GPTQ dequantize approx. l. 495; AWQ NotImplementedError approx. l. 573; repack MXFP4/NVFP4 approx. l. 984-1131)
- gguf-py/gguf/gguf_reader.py  (ReaderTensor: tensor_type, n_elements, n_bytes)
- tools/quantize/README.md  (llama-quantize examples, --tensor-type, bpw/size/tg table for Llama-3.1-8B)
- tools/imatrix/README.md
- tools/perplexity/README.md  (Llama-3-8B scoreboard, KLD, 11/37 GiB of logits; revision f364eb6f)
- docs/multi-gpu.md  (tensor mode: -fa on, KV not quantized)
- PRs ggml-org/llama.cpp: #1684 (k-quants), #4773 (IQ2), #4861 (imatrix), #4897, #5196 (IQ3_XXS), #6936 (KLD/perplexity README), #23572 (NVFP4 CUDA, open)

**Unsloth**

- https://github.com/unslothai/unsloth (README, studio/INFERENCE_ENGINES.md, API: repo, contributors)
- https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs
- https://www.ycombinator.com/companies/unsloth-ai
- https://huggingface.co/api/models/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF/tree/main  (reading the UD-IQ3_XXS header: 12,848,766,112 B, 30,532,122,624 params)

**Research papers**

- arXiv 2210.17323 (GPTQ), 2306.00978 (AWQ), 2211.10438 (SmoothQuant), 2209.05433 (FP8), 2305.14314 (QLoRA/NF4), 2310.10537 (OCP MX), 2406.11235 (QTIP / EXL3)
- https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/

**vLLM / SGLang / TRT-LLM (clones ~/runtimes-src/)**

- vllm: vllm/platforms/rocm.py (supported_quantization approx. l. 625-649; _ON_RDNA4), vllm/model_executor/layers/quantization/__init__.py, vllm/model_executor/kernels/linear/mixed_precision/rdna_hybrid_w4a16.py, vllm/model_executor/kernels/linear/scaled_mm/rocm.py, docs/features/quantization/README.md
- sglang: python/sglang/srt/layers/quantization/, python/sglang/kernels/aot/setup_rocm.py
- TensorRT-LLM: docs/source/legacy/tensorrt-backend-removal.md

**MLX / mlx-lm / oMLX / ds4**

- mlx: mlx/ops.cpp (quantize, lines approx. 4827-4852)
- mlx-lm: mlx_lm/convert.py (arguments, mixed_* recipes), mlx_lm/quant/, LEARNED_QUANTS.md, SERVER.md, mlx_lm/utils.py, mlx_lm/gguf.py
- omlx: omlx/oq.py, docs/oQ_Quantization.md
- ds4: docs/MODELS.md (quantization layout; approx. 81 GiB), speed-bench/m5_max.csv

**The repository's own documents**

- en/speeding-up-generation/README.md  (quality not measured; benchmark aborted after 11/120 samples; 10 October PL 92 / EN 93)
- en/speeding-up-generation/01-HOW-IT-WORKS.md, 02-DEEPSEEK-DEPLOYMENT.md  (llama-swap config, VRAM free after loading, converter command, 167 GB checkpoint, 10.9 GB draft)
- pl/przyspieszanie-generowania/narzedzia/gguf-inspect.py

**Survey notes**

- notes/05-special-runtimes.md (sections 5 and 6), notes/06-fundamentals.md (sections 1, 10, 11, 12), notes/01-ggml-family.md (§4), notes/04-apple-and-ds4.md, notes/03-serving-engines.md

### Chapter 04-LLAMA-CPP-I-RODZINA-GGML


**llama.cpp / ggml (code: production tree ~/llama.cpp-0ce8cd1, commit 0ce8cd11416c8840498e6701bcbe39ad4b858c2b, 2026-10-19)**

- ggml/include/ggml.h
- ggml/include/gguf.h
- ggml/include/ggml-backend.h
- ggml/src/ggml-impl.h
- ggml/src/ggml-common.h
- ggml/src/ggml-backend.cpp
- ggml/src/ggml-backend-meta.cpp
- ggml/src/ggml-alloc.c
- ggml/src/gguf.cpp
- ggml/src/ggml-cuda/ggml-cuda.cu
- ggml/src/ggml-cuda/common.cuh
- ggml/src/ggml-cuda/vendors/hip.h
- ggml/src/ggml-hip/CMakeLists.txt
- src/llama-context.cpp
- src/llama-graph.cpp
- src/llama-kv-cache*.{h,cpp}
- src/llama-memory*.{h,cpp}
- src/llama-batch.h
- src/llama-model-loader.cpp
- src/llama-model.cpp
- src/llama-sampler.cpp
- src/llama-grammar.cpp
- src/models/llama.cpp
- src/llama-moe-cache.h
- include/llama.h
- common/arg.cpp
- common/common.h
- common/speculative.cpp
- common/fit.h
- tools/server/server.cpp
- tools/server/server-context.cpp
- tools/server/server-models.{h,cpp}
- tools/server/server-tools.{h,cpp}
- tools/server/server-mcp.{h,cpp}
- tools/server/server-decision.h
- tools/imatrix/README.md
- tools/quantize/quantize.cpp
- tools/llama-bench/llama-bench.cpp
- tools/rpc/README.md
- docs/multi-gpu.md
- docs/speculative.md
- docs/llguidance.md
- docs/build.md
- CODEOWNERS
- AGENTS.md
- https://github.com/ggml-org/llama.cpp
- https://api.github.com/repos/ggml-org/llama.cpp (+ /languages, /releases, /contributors, /commits)
- https://api.github.com/orgs/ggml-org
- https://ggml.ai
- https://huggingface.co/blog/ggml-joins-hf
- https://github.com/ggml-org/llama.cpp/discussions/19759
- https://llama.app
- https://github.com/ggml-org/Llama-macOS
- https://raw.githubusercontent.com/ggml-org/ggml/master/README.md
- https://lmstudio.ai/docs/app
- https://github.com/janhq/jan
- ~/runtimes-src/ollama/{LLAMA_CPP_VERSION,llama/README.md,CMakeLists.txt,llm/*}

**ggml / whisper.cpp**

- https://github.com/ggml-org/ggml
- https://github.com/ggml-org/whisper.cpp
- https://github.com/leejet/stable-diffusion.cpp
- https://github.com/PABannier/bark.cpp

**ik_llama.cpp**

- https://github.com/ikawrakow/ik_llama.cpp (README, docs/parameters.md, AUTHORS, LICENSE)
- https://github.com/ikawrakow/ik_llama.cpp/discussions/316
- https://github.com/ikawrakow/ik_llama.cpp/discussions/319
- https://github.com/ikawrakow/ik_llama.cpp/discussions/2417
- https://github.com/ikawrakow/ik_llama.cpp/discussions/590

**llamafile**

- https://github.com/mozilla-ai/llamafile (README, README_0.10.0.md, docs/technical_details.md, docs/quickstart.md, docs/security.md, LICENSE)
- https://docs.mozilla.ai/llamafile
- https://www.mozilla.ai

**KoboldCpp**

- https://github.com/LostRuins/koboldcpp (README, wiki, kcpp_src/README.md)
- https://koboldcpp.net

**textgen (text-generation-webui)**

- https://github.com/oobabooga/textgen

**llama-swap**

- https://github.com/mostlygeek/llama-swap (README, internal/router/design.md, docs/kb/*)

**Source notes**

- scratchpad/runtimes/notes/01-ggml-family.md

### Chapter 05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE


**Sources for chapter 05 (from the notes notes/02-wrappers.md, notes/01-ggml-family.md, notes/07-money-and-people.md)**


**Paths ~/runtimes-src/... are shallow clones on the research machine; API addresses = GitHub REST.**


**Ollama**

- ~/runtimes-src/ollama/LLAMA_CPP_VERSION
- ~/runtimes-src/ollama/llama/README.md
- ~/runtimes-src/ollama/llama/compat/README.md
- ~/runtimes-src/ollama/llama/compat/llama-ollama-compat.cpp
- ~/runtimes-src/ollama/CMakeLists.txt
- ~/runtimes-src/ollama/llm/llama_server.go
- ~/runtimes-src/ollama/llm/llama_binary.go
- ~/runtimes-src/ollama/server/sched.go
- ~/runtimes-src/ollama/server/routes.go
- ~/runtimes-src/ollama/envconfig/config.go
- ~/runtimes-src/ollama/manifest/manifest.go
- ~/runtimes-src/ollama/manifest/layer.go
- ~/runtimes-src/ollama/mlxrunner/ (including embed.go, model/architectures/architectures.go)
- ~/runtimes-src/ollama/app/updater/updater.go
- ~/runtimes-src/ollama/discover/
- ~/runtimes-src/ollama/docs/faq.mdx
- ~/runtimes-src/ollama/docs/gpu.mdx
- ~/runtimes-src/ollama/docs/context-length.mdx
- ~/runtimes-src/ollama/docs/cloud.mdx
- ~/runtimes-src/ollama/docs/modelfile.mdx
- https://api.github.com/repos/ollama/ollama
- https://api.github.com/repos/ollama/ollama/pulls/16031
- https://api.github.com/repos/ollama/ollama/issues/3185
- https://api.github.com/repos/ollama/ollama/issues/8557
- https://api.github.com/repos/ollama/ollama/issues/14259
- https://api.github.com/repos/ollama/ollama/issues/17878
- https://api.github.com/repos/ollama/ollama/releases
- https://ollama.com/pricing
- https://ollama.com/blog/all-aboard-open-models
- https://ollama.com/blog/improved-performance-and-model-support-with-gguf
- https://ollama.com/blog/transparent-pricing
- https://en.wikipedia.org/wiki/Ollama   (third-party)

**LM Studio**

- https://lmstudio.ai/terms
- https://lmstudio.ai/app-privacy
- https://lmstudio.ai/enterprise
- https://lmstudio.ai/blog/introducing-lm-studio-bionic
- https://lmstudio.ai/blog/0.4.0
- https://lmstudio.ai/blog/free-for-work
- https://lmstudio.ai/blog/locally-ai-joins-lm-studio
- https://lmstudio.ai/blog/locally-lm-link
- https://lmstudio.ai/blog/splash-engine
- https://lmstudio.ai/docs/developer
- https://lmstudio.ai/docs/developer/core/headless
- https://lmstudio.ai/docs/developer/anthropic-compat
- https://lmstudio.ai/docs/app
- https://lmstudio.ai/docs/app/mcp
- https://api.github.com/orgs/lmstudio-ai
- https://github.com/lmstudio-ai/lms (README)
- https://github.com/lmstudio-ai/mlx-engine (README)
- https://github.com/lmstudio-ai/docs (lmstudio-vs-llmster-vs-lms.md, system-requirements.md, 3_cli/4_runtime/runtime.md)
- https://en.wikipedia.org/wiki/LM_Studio   (third-party)

**llmman**

- ~/runtimes-src/llmman/README.md
- ~/runtimes-src/llmman/Cargo.toml
- ~/runtimes-src/llmman/AGENTS.md
- ~/runtimes-src/llmman/LLAMA_CPP_RELEASE
- ~/runtimes-src/llmman/MLX_LM_RELEASE
- ~/runtimes-src/llmman/docs/backends.md
- ~/runtimes-src/llmman/docs/api.md
- ~/runtimes-src/llmman/src/modelpack.rs
- ~/runtimes-src/llmman/src/storage/oci.rs
- ~/runtimes-src/llmman/src/cmd/serve/sched.rs
- ~/runtimes-src/llmman/src/cmd/serve/backend.rs
- ~/runtimes-src/llmman/src/llama_release.rs
- https://llmmanorg.github.io (+ /blog)
- https://api.github.com/repos/llmmanorg/llmman
- https://api.github.com/users/ericcurtin
- https://api.github.com/repos/ericcurtin/agenticlinux
- (commit metadata: containers/ramalama, docker/model-runner)

**Jan**

- https://api.github.com/repos/janhq/jan (LICENSE, README, tree, Cargo.toml, engine/mod.rs, jan-llama-worker.rs, mlx-server/README, extensions/llamacpp-extension/settings.json)
- https://jan.ai ; https://jan.ai/changelog ; https://docs.jan.ai/desktop/privacy
- https://menlo.ai
- https://huggingface.co/janhq

**GPT4All**

- https://api.github.com/repos/nomic-ai/gpt4all (releases, commits, tree, .gitmodules, issues)
- https://nomic.ai ; https://nomic.ai/about

**LocalAI**

- https://api.github.com/repos/mudler/LocalAI (README, backend/backend.proto, pkg/model/process.go, tree, ADOPTERS)
- https://api.github.com/users/mudler
- https://localai.io

**Lemonade**

- https://api.github.com/repos/lemonade-sdk/lemonade (README, docs/dev/philosophy.md, docs/dev/backends-reference.md, docs/guide/configuration/llamacpp.md, docs/guide/telemetry.md)
- https://api.github.com/orgs/lemonade-sdk
- https://api.github.com/repos/ROCm/FastFlowLM (LICENSE_BINARY.txt)
- https://api.github.com/users/jeremyfowers ; users/danielholanda ; users/ramkrishna2910 ; users/superm1
- https://lemonade-server.ai

**Docker Model Runner**

- https://api.github.com/repos/docker/model-runner (README, .versions, .gitmodules, tree)
- https://docs.docker.com/ai/model-runner

**RamaLama**

- https://api.github.com/repos/containers/ramalama (README, MAINTAINERS.md, Roadmap.md, tree)

**Open WebUI, AnythingLLM**

- https://github.com/open-webui/open-webui (LICENSE, LICENSE_HISTORY)
- https://docs.openwebui.com/license
- https://github.com/Mintplex-Labs/anything-llm (README)
- https://anythingllm.com/pricing

**llama.cpp router and llama-swap (comparison in section 8)**

- ~/llama.cpp-0ce8cd1/tools/server/server-models.{h,cpp}, common/common.h, common/arg.cpp
- https://github.com/mostlygeek/llama-swap (README, docs/kb/, internal/router/design.md)

### Chapter 06-SILNIKI-SERWEROWE-VLLM-SGLANG


**vLLM**

- https://arxiv.org/abs/2309.06180 (PagedAttention; PDF pp. 1-2, 8-9)
- https://pytorch.org/blog/pytorch-foundation-welcomes-vllm/
- https://en.wikipedia.org/wiki/VLLM
- https://vllm.ai/blog/v1-alpha-release
- https://vllm.ai/blog (lista)
- https://docs.vllm.ai (installation)
- https://inferact.ai (home, /blog)
- https://github.com/Inferact
- GitHub API: repos/vllm-project/vllm (repo, releases, contributors, languages), users/*, orgs/vllm-project
- repo vllm @ b7701fc: docs/governance/process.md
- repo vllm: docs/design/arch_overview.md, model_runner_v2.md, cuda_graphs.md, torch_compile.md, prefix_caching.md, plugin_system.md, custom_op.md, dbo.md, hybrid_kv_cache_manager.md
- repo vllm: docs/features/disagg_prefill.md, docs/features/quantization/gguf.md, docs/features/quantization/README.md
- repo vllm: docs/getting_started/installation/gpu.rocm.inc.md, docs/getting_started/installation/README.md
- repo vllm: vllm/v1/core/sched/scheduler.py, async_scheduler.py; vllm/v1/core/{kv_cache_manager,block_pool,kv_cache_utils,kv_cache_coordinator,single_type_kv_cache_manager,kv_cache_planning}.py
- repo vllm: vllm/v1/engine/core.py; vllm/v1/worker/gpu_model_runner.py, vllm/v1/worker/gpu/; vllm/v1/attention/; vllm/v1/spec_decode/; vllm/v1/structured_output/
- repo vllm: vllm/config/{scheduler,vllm,cache,structured_outputs}.py; vllm/platforms/rocm.py; vllm/model_executor/kernels/linear/**; vllm/_aiter_ops.py
- repo vllm: vllm/usage/usage_lib.py; vllm/envs.py; CMakeLists.txt; docker/Dockerfile.rocm_base; rust/README.md; csrc/rocm/
- https://github.com/vllm-project/vllm-gguf-plugin (via GitHub API)

**SGLang**

- https://arxiv.org/abs/2312.07104
- https://en.wikipedia.org/wiki/SGLang
- https://lmsys.org/about
- https://lmsys.org/blog/2024-12-04-sglang-v0-4/
- https://pytorch.org/blog/sglang-joins-pytorch/
- https://radixark.com
- GitHub API: repos/sgl-project/sglang (repo, releases, contributors, languages)
- repo sglang @ aaa9388: python/sglang/srt/managers/{scheduler,schedule_policy,schedule_batch}.py
- repo sglang: python/sglang/srt/mem_cache/{radix_cache.py,README.md}
- repo sglang: python/sglang/srt/entrypoints/engine.py
- repo sglang: docs/docs/hardware-platforms/amd_gpu.mdx; docs/docs/advanced_features/{attention_backend,quantization,radix_eviction_policy}.mdx
- repo sglang: python/sglang/kernels/aot/setup_rocm.py; docker/rocm.Dockerfile, docker/rocm-gfx1151.Dockerfile
- repo sglang: sgl-model-gateway/README.md; python/pyproject.toml

**TensorRT-LLM**

- GitHub API: repos/NVIDIA/TensorRT-LLM (repo, license, releases, contributors, languages)
- repo TensorRT-LLM @ 7695494: README.md; LICENSE
- repo TensorRT-LLM: docs/source/{overview.md,supported-hardware.md,legacy/tensorrt-backend-removal.md,features/paged-attention-ifb-scheduler.md}
- repo TensorRT-LLM: tensorrt_llm/usage/*; tensorrt_llm/_torch/pyexecutor/*; cpp/tensorrt_llm/batch_manager/*
- https://nvidia.github.io/TensorRT-LLM

**TGI**

- GitHub API: repos/huggingface/text-generation-inference (repo, readme, commits, license history)
- https://huggingface.co/docs/text-generation-inference (index)
- repo TGI docs/source: installation_amd.md, multi_backend_support.md, usage_statistics.md

**LMDeploy**

- GitHub API: repos/InternLM/lmdeploy
- https://arxiv.org/abs/2508.15601
- repo lmdeploy docs/en/get_started/installation.md (README)

**Cluster layers**

- https://github.com/ai-dynamo/dynamo (README, API)
- https://github.com/llm-d/llm-d (README, API)
- https://github.com/LMCache/LMCache (README, API, blog 2025-10-31)
- https://github.com/flashinfer-ai/flashinfer (README, API); https://arxiv.org/abs/2501.01005
- https://github.com/Dao-AILab/flash-attention (README "AMD ROCm Support", API); https://arxiv.org/abs/2205.14135; https://tridao.me
- https://github.com/modular/modular (README, API); modular.com/about; modular.com/blog (lista); MAX packages page

**llama.cpp (comparison column)**

- notes/01-ggml-family.md (drzewo 0ce8cd1: docs/multi-gpu.md, tools/server/*, common/common.h; GitHub API 2026-10-19)

### Chapter 07-APPLE-MLX-OMLX-I-DS4


**ds4 / DwarfStar**

- https://github.com/antirez/ds4
- ds4: README.md, AGENT.md, CONTRIBUTING.md, LICENSE, MODEL_CARD.md, Makefile, download_model.sh
- ds4: docs/{MODELS,SERVER,CLIENTS,SSD_STREAMING,DISTRIBUTED,SPECULATIVE_DECODING,PERFORMANCE,STRIX_HALO,DGX_SPARK,CUDA_MULTI_GPU,METAL}.md
- ds4: dir-steering/README.md, speed-bench/*.csv, speed-bench/gfx1151-prefill-results.md, QA_BEFORE_RELEASES.md
- ds4: ds4.c, ds4_kvstore.h, ds4_ssd.h, ds4_engram.h, ds4_deepseek41_dspark.h, ds4_gpu_mgpu.h, ds4_rocm_compat.cu, rocm/ds4_rocm_common.cuh
- GitHub API 2026-10-19: repos/antirez/ds4 (+ contributors, forks, issues #16 #521, PRs #558 #599 #602 #744 #1233), users/antirez
- https://github.com/notatestuser/ds4-control
- https://en.wikipedia.org/wiki/Salvatore_Sanfilippo
- https://antirez.com/

**MLX**

- https://github.com/ml-explore/mlx
- mlx: README.md, docs/src/usage/distributed.rst, docs/src/python/{fast,cuda}.rst, mlx/backend/metal/device.cpp, directory line counts
- GitHub API 2026-10-19: ml-explore/{mlx,mlx-swift,mlx-swift-lm,mlx-c}, users/awni, users/zcbenz, users/angeloskath
- https://machinelearning.apple.com/research/mlx-distributed-inference (2026-10-15; only a summarizer's output was read)

**mlx-lm**

- https://github.com/ml-explore/mlx-lm
- mlx-lm: mlx_lm/{server,generate,convert}.py, mlx_lm/models/cache.py, SERVER.md, LEARNED_QUANTS.md, mlx_lm/quant/
- https://huggingface.co/api/organizations/mlx-community/overview

**oMLX**

- https://github.com/jundot/omlx
- omlx: README.md, docs/oQ_Quantization.md, docs/experimental/{dflash_mlx_integration,qwen35_ane_prefill,MoE_Expert_Offload}.md
- omlx: omlx/scheduler.py, omlx/oq.py, omlx/cache/paged_ssd_cache.py
- https://omlx.ai
- GitHub API 2026-10-19: jundot/omlx, users/jundot, waybarrios/vllm-mlx, vllm-project/vllm-metal, lmstudio-ai/mlx-engine, ddalcu/mlx-serve, Blaizzy/mlx-vlm, youssofal/mtplx, bstnxbt/dflash-mlx, incoai/splash
- ollama: mlxrunner/ (clone)

**Apple stack**

- https://developer.apple.com/documentation/foundationmodels and subpages (incl. TN3193)
- https://developer.apple.com/documentation/coreai
- https://github.com/apple/coreai-models
- https://machinelearning.apple.com/research/{apple-foundation-models-2025-updates, introducing-third-generation-of-apple-foundation-models, core-ml-on-device-llama}
- https://www.apple.com/mac-studio/specs/
- https://www.apple.com/macbook-pro/specs/
- https://en.wikipedia.org/wiki/{Apple_M3, Apple_M4, Apple_M5}

**exo**

- https://github.com/exo-explore/exo
- exo: README.md, PLATFORMS.md, src/exo/master/placement.py, src/exo/shared/election.py, src/exo/worker/engines/mlx/auto_parallel.py
- https://exolabs.net

**llama.cpp (for section 8 mapping)**

- notes/01-ggml-family.md (llama.cpp prompt cache, context checkpoints, speculative types, llama-moe-cache)

**Local guide**

- ../speeding-up-generation/README.md (reader's measured 23.5 -> ~50 tok/s result; not re-read by the chapter author, figures given by the course lead)

**Evidence base**

- notes/04-apple-and-ds4.md

### Chapter 08-SPECJALISCI-KTRANSFORMERS-I-INNE


**KTransformers**

- https://github.com/kvcache-ai/ktransformers (README.md, MAINTAINERS.md, kt-kernel/README.md, kt-kernel/CMakeLists.txt, kt-kernel/python/experts.py, kt-kernel/python/experts_base.py, kt-kernel/cpu_backend/worker_pool.{h,cpp}, kt-kernel/operators/moe-tp.hpp, kt-kernel/operators/amx/la/amx_kernels.hpp, doc/en/AMX.md, doc/en/ROCm.md, doc/en/kt-kernel/kt-kernel_intro.md, doc/en/kt-kernel/experts-sched-Tutorial.md) @a694e718
- https://kvcache-ai.github.io/ktransformers/
- https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/
- https://madsys.cs.tsinghua.edu.cn/
- https://lmsys.org/blog/2025-10-22-KTransformers/
- https://raw.githubusercontent.com/hiyouga/LLaMA-Factory/main/README.md
- sglang: python/sglang/srt/layers/moe/kt_ep_wrapper.py (rig clone ~/runtimes-src/sglang)
- GitHub API: repos/kvcache-ai/ktransformers (+contributors, releases), orgs/kvcache-ai

**Hybrid MoE comparison**

- llama.cpp tree 0ce8cd1: common/arg.cpp (lines 2758-2793), src/llama-moe-cache.h, ggml/src/ggml-backend.cpp, ggml/src/ggml-cuda/ggml-cuda.cu (180-183, 6011-6015)
- https://github.com/ikawrakow/ik_llama.cpp (README, docs/parameters.md, discussions #316, #319, #590)
- ds4: docs/SSD_STREAMING.md, ds4_ssd.c, AGENT.md, MODEL_CARD.md, PR #558 (rig clone ~/runtimes-src/ds4)
- notes/01-ggml-family.md, notes/04-apple-and-ds4.md, notes/05-special-runtimes.md

**mistral.rs / Candle**

- https://github.com/EricLBuehler/mistral.rs (README.md, Cargo.toml, mistralrs-core/Cargo.toml, mistralrs-core/src/{scheduler,engine,paged_attention,pipeline}, mistralrs-quant/src/{lib.rs,uqff}, mistralrs-mcp/src/lib.rs, mistralrs-paged-attn/src/cuda) @465191d0
- https://docs.mistralrs.dev/
- https://github.com/huggingface/candle (tag 0.11.0)
- GitHub API: repos/EricLBuehler/mistral.rs, users/EricLBuehler, orgs/huggingface/members/EricLBuehler, users/LaurentMazare

**MLC LLM / WebLLM**

- https://github.com/mlc-ai/mlc-llm (README.md, .gitmodules, cpp/serve, python/mlc_llm/{model,quantization,cli}, docs/) @8978ea9a
- https://llm.mlc.ai/docs/compilation/compile_models.html
- https://github.com/mlc-ai/web-llm (README)
- https://arxiv.org/abs/2412.15803
- https://tqchen.com/

**NPU / vendor stacks**

- https://github.com/microsoft/onnxruntime-genai (README, DESIGN.md, docs/Privacy.md, cmake/options.cmake, src/engine, src/ep, src/python/py/models/builder.py)
- https://github.com/openvinotoolkit/openvino.genai (README)
- https://github.com/qualcomm/GenieX (README, CONTRIBUTING.md, .gitmodules); redirect from NexaAI/nexa-sdk (API)
- https://ryzenai.docs.amd.com/en/latest/hybrid_oga.html
- llama.cpp tree 0ce8cd1: docs/backend/OPENVINO.md, docs/backend/snapdragon
- Apple Foundation Models (developer.apple.com, thin fetch)

### Chapter 10-PIENIADZE-I-LUDZIE


**Sources for chapter 10 (from the notes notes/07-money-and-people.md and the “Money and people” sections in notes/01-05), grouped**


**llama.cpp / ggml / Hugging Face**

- https://ggml.ai
- https://huggingface.co/blog/ggml-joins-hf
- https://github.com/ggml-org/llama.cpp/discussions/19759
- https://github.com/ggml-org
- https://huggingface.co/blog/omlx
- https://huggingface.co/pricing
- https://github.com/huggingface/text-generation-inference
- GitHub API 2026-10-19: repos/ggml-org/llama.cpp, contributors, users/*, orgs/ggml-org
- file: ~/llama.cpp-0ce8cd1/LICENSE, AUTHORS, CODEOWNERS, ggml/src/ggml-hip/CMakeLists.txt, ggml/src/ggml-cuda/vendors/hip.h

**NVIDIA–Hugging Face (press report; no statement from the companies)**

- https://en.wikipedia.org/wiki/Hugging_Face
- https://en.wikipedia.org/wiki/Nvidia
- TechCrunch "Nvidia confirms it will buy Hugging Face for $12.9 billion" (2026-09-03)

**ik_llama.cpp, llama-swap, llamafile, KoboldCpp, textgen**

- https://github.com/ikawrakow/ik_llama.cpp/discussions/316
- https://github.com/mostlygeek/llama-swap
- https://blog.mozilla.org/en/mozilla/introducing-mozilla-ai-investing-in-trustworthy-ai/
- https://www.mozilla.ai

**Ollama**

- https://ollama.com/blog/all-aboard-open-models
- https://ollama.com/pricing
- https://ollama.com/blog/transparent-pricing
- https://github.com/ollama/ollama/issues/3185
- https://en.wikipedia.org/wiki/Ollama

**LM Studio, Jan, LocalAI, Lemonade, Open WebUI, AnythingLLM, GPT4All**

- https://lmstudio.ai/terms
- https://lmstudio.ai/blog
- https://lmstudio.ai/enterprise
- https://menlo.ai
- https://localai.io
- https://www.lemonade-server.ai
- https://docs.openwebui.com/license/
- open-webui LICENSE, LICENSE_HISTORY
- https://anythingllm.com
- https://www.nomic.ai/about

**vLLM, Inferact, Red Hat, SGLang, RadixArk, LMSYS**

- https://inferact.ai/news/introducing-inferact-building-the-future-of-ai-inference
- https://pytorch.org/blog/pytorch-foundation-welcomes-vllm/
- https://vllm.ai/#sponsors
- https://arxiv.org/abs/2309.06180
- https://www.redhat.com/en/products/ai/inference-server
- Red Hat press releases: Neural Magic (2024-11-12, 2025-01-13)
- https://www.radixark.com
- https://lmsys.org/about/
- https://techcrunch.com/2026/01/21/sources-project-sglang-spins-out-as-radixark-with-400m-valuation-as-inference-market-explodes/
- vLLM docs/governance/process.md

**NVIDIA, Modular, Qualcomm**

- https://docs.nvidia.com/ai-enterprise/planning-resource/licensing-guide/latest/pricing.html
- https://developer.nvidia.com/nim
- TensorRT-LLM README/LICENSE; ai-dynamo/dynamo README/LICENSE
- https://www.modular.com/about
- https://www.modular.com/blog/qualcomm-to-acquire-modular
- https://www.modular.com/blog/qualcomm-completes-acquisition-of-modular
- https://www.modular.com/blog/modular-raises-250m-to-scale-ais-unified-compute-layer
- https://www.modular.com/legal/community

**Apple / MLX / oMLX / ds4 / mistral.rs / Docker / RamaLama / llmman**

- GitHub API: ml-explore/mlx, mlx-lm, users/awni
- https://huggingface.co/blog/omlx
- https://antirez.com/news/144
- https://redis.io/blog/agplv3/
- https://github.com/sponsors/antirez
- https://www.docker.com/blog/introducing-docker-model-runner/
- containers/ramalama, docker/model-runner, llmmanorg/llmman (GitHub API, README)
- https://llmmanorg.github.io

**Unsloth**

- unslothai/unsloth README, COPYING, studio/LICENSE.AGPL-3.0
- https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs
- https://www.ycombinator.com/companies/unsloth-ai

**Hosted inference**

- https://www.together.ai/blog/announcing-our-series-c
- https://modal.com/blog/1-billion-annualized-run-rate-series-d
- https://en.wikipedia.org/wiki/Fireworks_AI
- https://www.baseten.co

## 4. Weakest-verified points (read with caution)

| Point | Status |
|---|---|
| **NVIDIA's acquisition of Hugging Face (12.93 billion USD)** | only Wikipedia and one TechCrunch article *(press report)*; I did not find a statement from NVIDIA or HF; closing of the deal planned for the first half of 2027 |
| **Ollama funding** | 88 million USD “in total” according to the company *(company's own claim, blog post 2026-07-09)* vs 65 million USD according to Wikipedia — not reconciled |
| **Inferact (the creators of vLLM)** | 150 million USD seed at an 800 million USD valuation, January 2026 *(company's own claim)*; the amount is confirmed by the press; I could not establish the exact day; the company's home page does not give the funding, the information comes from the launch post |
| **Valuations of Fireworks (17.5 billion USD), RadixArk (400 million USD), Tensormesh (20 million USD)** | single sources |
| **Funding of LM Studio, Jan/Menlo, Unsloth, exo, Approaching.AI, Baseten, Open WebUI, AnythingLLM** | I did not find it |
| **Why Apple funds MLX** | my guess; no statement from Apple |
| **Apple's 2026 posts (AFM 3, MLX + RDMA, M5 Ultra 1.2 TB/s)** | reached me through a summarizing tool, not as raw text |
| **R9700 bandwidth (~640 GB/s), peak TFLOPS** | the AMD page was unreachable; VRAM verified via sysfs (34,208,743,424 B per card); bandwidth from external/calculated data |
| **Type composition of the DeepSeek-V4-Flash UD-IQ3_XXS file** | size measured (104,207,848,508 B), composition not; reading the header settles it (the box in chapter 03) |
| **`-sm tensor` support for DeepSeek-V4 in llama.cpp** | the code has neither an exclusion-list entry nor explicit confirmation; in practice it worked on the rig (measurements in the generation-speedup guide) |
| **vLLM on gfx1201** | the documentation (AWQ/GPTQ unsupported on AMD) contradicts the code (INT4 kernels for RDNA); zero measurements |
| **Performance of any engines on gfx1201 other than llama.cpp** | no measurements |

## 5. Discrepancies between sources and how I resolved them

- **Ollama vs llama.cpp:** the llmman README describes Ollama as a “fork of llama.cpp + its own engine”; Ollama's code (PR #16031, 2026-05-29; `LLAMA_CPP_VERSION` b11669) shows that GGUF runs on the upstream `llama-server`. I went with the code.
- **KTransformers:** one note speaks of archiving the old framework (`archive/`), the other of “API churn”; I went with the archiving.
- **ds4:** `AGENT.md` says “DeepSeek V4 Flash specific”, the README lists several models; I went with the README (the project is now called DwarfStar).
- **Apple:** the context window of the on-device model — 4096 tokens (developer documentation) vs 65 thousand (a 2025 post); I went with the documentation.
- **vLLM:** `max_num_seqs` 128 in the config vs 1024 in the Model Runner V2 document; Model Runner V2 is the default in the code, “experimental” in the documentation — both values are given.
- **llama-swap:** approx. 653 vs approx. 553 commits in the two notes; I went with 653 (consistent with the main author's share of approx. 82%).
- **Mozilla.ai (30 million USD), Red Hat–Neural Magic (closing 2025-01-13), ggml.ai in HF (2026-02-20):** confirmed in primary sources during the final check (Red Hat, Hugging Face) or in the notes with a page citation.
- **GB vs GiB:** the numbers in the course are decimal GB unless GiB is indicated; the DeepSeek file is 104,207,848,508 B = 104.2 GB = 97.05 GiB.
- **Jan:** Apache-2.0 license in the README, GitHub shows NOASSERTION.

## 6. What I could not establish

The detailed “what I could not establish” lists are at the end of chapters 05–08 and 10. The most important: funding rounds and founders of LM Studio and Jan; telemetry of most wrappers; gfx1201 support in LM Studio, Docker Model Runner, RamaLama, Jan, MLC; the license of the DeepSeek weights and the terms of Unsloth's GGUF repositories; NUMA in llama.cpp and ik_llama.cpp; market data for Polish users (I did not search).
