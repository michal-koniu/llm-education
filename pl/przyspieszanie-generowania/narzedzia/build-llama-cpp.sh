#!/bin/bash
# Build llama.cpp 0ce8cd1 (19 X 2026) into a SEPARATE directory; the production build in ~/llama.cpp/build is not touched.
set -e
SRC=/home/USER/llama.cpp-0ce8cd1
if ! git -C $SRC rev-parse --verify -q HEAD >/dev/null 2>&1; then
  rm -rf $SRC; mkdir -p $SRC; cd $SRC
  git init -q; git remote add origin https://github.com/ggml-org/llama.cpp
  git fetch -q --depth 1 origin 0ce8cd11416c8840498e6701bcbe39ad4b858c2b; git checkout -q FETCH_HEAD
fi
cd $SRC && git log -1 --format="HEAD: %h %ad %s" | cut -c1-120
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DGGML_HIP=ON -DGPU_TARGETS=gfx1201 -DGGML_HIP_GRAPHS=ON -DGGML_HIP_NO_VMM=ON \
  -DCMAKE_HIP_COMPILER=/opt/rocm-7.2.4/lib/llvm/bin/clang++ -DGGML_CCACHE=ON 2>&1 | tail -8
date; nice -n 12 cmake --build build -j 14 --target llama-server llama-bench llama-cli 2>&1 | tail -5
date; ls -la build/bin/llama-server && build/bin/llama-server --version 2>&1 | head -3
echo BUILD_DONE
