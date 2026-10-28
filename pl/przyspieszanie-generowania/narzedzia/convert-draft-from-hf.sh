#!/bin/bash
# Convert the DSpark speculative head shipped inside DeepSeek-V4-Flash-0731 into a standalone draft GGUF.
# --remote: only the 3 shards that contain mtp.* (46,47,48 ~ 11 GB) are downloaded, not the full 167 GB checkpoint.
W=$HOME/spec-dspark
. $W/venv/bin/activate
export HF_HOME=$W/hf-cache
cd $HOME/llama.cpp
python convert_hf_to_gguf.py deepseek-ai/DeepSeek-V4-Flash-0731 --remote --dspark \
  --target-model-dir $W/target-hf --outtype bf16 --outfile $W/DeepSeek-V4-Flash-0731-DSpark.gguf
echo "CONVERT_RC=$?"
ls -la $W/*.gguf
