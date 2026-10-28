# rig-env.sh — środowisko obu kursów (szablon). Użycie (z katalogu głównego repozytorium):
#     source rig-env.sh
# albo z dowolnego miejsca:  source <ścieżka-do-llm-education>/rig-env.sh
# Utworzony 22 września 2026 (kurs 1, 00-KURS-INDEKS.md); od 11 października 2026 w repozytorium llm-education.
#
# To jest SZABLON. Wartości domyślne pochodzą z maszyny referencyjnej kursu. Każdą zmienną
# ze ścieżką możesz nadpisać, ustawiając ją w powłoce PRZED `source rig-env.sh`, np.:
#     M=/data/models LB=~/src/llama.cpp/build/bin source rig-env.sh
# albo po prostu zmień wartości domyślne poniżej.

# --- Repozytorium i katalogi robocze --------------------------------
# Wszystko, co tworzą kursy (skrypty, bazy, wyniki, środowiska Pythona, narzędzia),
# powstaje WEWNĄTRZ repozytorium, w katalogach ignorowanych przez git.
export LLMEDU="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "$LLMEDU" in *" "*) echo "⚠️  Ścieżka repozytorium zawiera spację - polecenia kursu jej nie obsłużą: $LLMEDU" ;; esac
export KURS=$LLMEDU/pl/kurs_lokalne_modele/praca         # kurs 1: skrypty, bazy, eval, gramatyki
export AGENT=$KURS/agent                              # kurs 1, część 6+: agent zbudowany od zera
export OSA=$LLMEDU/pl/kurs_aplikacje_agentowe/praca/os-agenta   # kurs 2: system "OS agenta"
export VENVS=$LLMEDU/.venvs                           # środowiska Pythona kursów (hf, kurs, dok, ...)
export NARZEDZIA=$LLMEDU/narzedzia                    # narzędzia budowane w kursie (whisper.cpp, piper)
mkdir -p "$KURS" "$(dirname "$OSA")" "$VENVS" "$NARZEDZIA"

# --- Binarki ---------------------------------------------------------
export LB=${LB:-~/llama.cpp/build/bin}                # llama.cpp jest wspólne z resztą maszyny
export WB=${WB:-$NARZEDZIA/whisper.cpp/build/bin}     # po części 5

# --- Modele ----------------------------------------------------------
# Modele leżą we wspólnym katalogu maszyny (używają ich też llama-swap i benchmarki).
export M=${M:-~/models}
export BIELIK=${BIELIK:-$M/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf}
export OSS20=${OSS20:-$M/gpt-oss-20b/gpt-oss-20b-MXFP4.gguf}
export QWEN32=${QWEN32:-$M/qwen3-32b/Qwen_Qwen3-32B-Q4_K_M.gguf}
export QWEN80=${QWEN80:-$M/qwen3-next-80b/Q4_1/Qwen3-Next-80B-A3B-Instruct-Q4_1-00001-of-00002.gguf}
export DRAFT=${DRAFT:-$M/gpt-oss-120b/eagle3-gpt-oss-120b-Q8_0.gguf}

# Powstaną w trakcie kursu:
export EMB=${EMB:-$M/embed/bge-m3-f16.gguf}                            # część 4
export VL=${VL:-$M/vl/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf}              # część 5
export VLMM=${VLMM:-$M/vl/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf}      # część 5
export WMODEL=${WMODEL:-$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin}   # część 5

# --- Karty graficzne -------------------------------------------------
# Które karty widzi ROCm. Na maszynie referencyjnej zintegrowana grafika (iGPU) zgłasza się
# jako osobne urządzenie z 2 GB; małe modele potrafią tam wylądować i działać ~50x wolniej,
# więc lista "0,1" ją wyklucza. USTAW WŁASNE KARTY: sprawdź numerację przez
#     amd-smi list      (albo: rocm-smi --showid)
# i pamiętaj, że po dołożeniu kart numeracja może się zmienić.
export HIP_VISIBLE_DEVICES=${HIP_VISIBLE_DEVICES:-0,1}

# Tylko ROCm z wieloma kartami: na maszynie referencyjnej (4x R9700) transfery P2P między
# kartami zawieszały cały host (ROCm #11348), dlatego P2P jest wyłączone. Przy jednej karcie
# te zmienne niczego nie zmieniają. GGML_CUDA_P2P: NIE USTAWIAĆ.
export NCCL_P2P_DISABLE=1
export NCCL_PROTO=Simple

# --- Sprawdzenie ------------------------------------------------------
# echo $LLMEDU $KURS           -> katalogi w repozytorium
# $LB/llama-cli --version      -> wersja llama.cpp
# rocm-smi --showid            -> widoczne karty
