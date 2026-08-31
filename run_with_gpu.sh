#!/usr/bin/env bash
set -e

# Change directory to the script's root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect virtual environment:
# 1. Use currently active VIRTUAL_ENV if set
# 2. Or prefer whichever folder has site-packages/tensorflow installed
# 3. Or fallback to lvenv / venv
if [ -n "$VIRTUAL_ENV" ] && [ -d "$VIRTUAL_ENV" ]; then
    VENV_PATH="$VIRTUAL_ENV"
elif [ -d "$SCRIPT_DIR/lvenv/lib/python3.12/site-packages/tensorflow" ]; then
    VENV_PATH="$SCRIPT_DIR/lvenv"
elif [ -d "$SCRIPT_DIR/venv/lib/python3.12/site-packages/tensorflow" ]; then
    VENV_PATH="$SCRIPT_DIR/venv"
elif [ -d "$SCRIPT_DIR/lvenv" ]; then
    VENV_PATH="$SCRIPT_DIR/lvenv"
elif [ -d "$SCRIPT_DIR/venv" ]; then
    VENV_PATH="$SCRIPT_DIR/venv"
else
    VENV_PATH=""
fi

# Locate nvidia CUDA libraries if virtual environment exists
NV_LIBS=""
if [ -n "$VENV_PATH" ]; then
    NV_SITE="$VENV_PATH/lib/python3.12/site-packages/nvidia"
    if [ -d "$NV_SITE" ]; then
        for dir in "$NV_SITE"/*/lib; do
            if [ -d "$dir" ]; then
                NV_LIBS="${NV_LIBS}:${dir}"
            fi
        done
        if [ -d "$NV_SITE/cuda_nvcc/nvvm/lib64" ]; then
            NV_LIBS="${NV_LIBS}:$NV_SITE/cuda_nvcc/nvvm/lib64"
        fi
    fi
fi

# Set library path including WSL CUDA driver library and nvidia packages
export LD_LIBRARY_PATH="/usr/lib/wsl/lib${NV_LIBS}:${LD_LIBRARY_PATH:-}"

# GPU / CUDA Settings for RTX 50-series (Blackwell)
export CUDA_VISIBLE_DEVICES=0
export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility
export CUDA_CACHE_DISABLE=0
export CUDA_CACHE_MAXSIZE=4294967296
export TF_FORCE_GPU_ALLOW_GROWTH=true

PYTHON_BIN="python3"
if [ -n "$VENV_PATH" ] && [ -x "$VENV_PATH/bin/python" ]; then
    PYTHON_BIN="$VENV_PATH/bin/python"
fi

if [ "$#" -eq 0 ]; then
    exec "$PYTHON_BIN"
fi

exec "$PYTHON_BIN" "$@"

