#!/bin/bash
#SBATCH --job-name=typesteering_completions
#SBATCH --partition=gpuA40x4
#SBATCH --account=bcbj-delta-gpu
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem=60G
#SBATCH --gres=gpu:1
#SBATCH --time=12:00:00

set -x
set -e

# You must run this script in the codetrace directory and in an environment
# in which it works.

MODEL=$1
LANG=$2

if [ "$LANG" = "py" ]; then
    SOURCE_DATASET="nuprl-staging/py_typeinf_fim"
else
    SOURCE_DATASET="nuprl-staging/ts_typeinf_fim"
fi

NUM_GPUS=$(nvidia-smi --list-gpus | wc -l)
DEVICES=$(seq -s "," 0 $((NUM_GPUS - 1)))
export CUDA_VISIBLE_DEVICES="$DEVICES"

VLLM_LOGGING_LEVEL=ERROR python3 -m codetrace.scripts.completions \
    --model /work/nvme/bcbj/franlucc/models/$MODEL \
    --prompt-ds $SOURCE_DATASET \
    --new-ds-name results/completions-$LANG-$MODEL
