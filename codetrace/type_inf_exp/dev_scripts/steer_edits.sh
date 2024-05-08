#!/bin/bash

edits=()
edits+=("rename_types" "rename_vars" "all_renames" "all_mutations" "delete_annotation" "types_and_delete" "vars_and_delete")

SOURCE_DATASET="franlucc/ts_<EDIT>_may3_seed0_starcoderbase-1b_typechecked"
DATADIR="/mnt/ssd/franlucc/projects/codetrace/data/starcoderbase-1b/typescript/may3_seed0_typechecked"
EXPDIR="/mnt/ssd/franlucc/projects/codetrace/results/starcoderbase-1b/typescript/may3_seed0_typechecked"
MODEL="/mnt/ssd/arjun/models/starcoderbase-1b"

LANG=""
if [[ $SOURCE_DATASET == *"/ts_"* ]]; then
    LANG="ts"
fi
if [[ $SOURCE_DATASET == *"/py_"* ]]; then
    LANG="py"
fi

for edit in "${edits[@]}"; do
    echo "Running steering pipeline for $edit"
    SOURCE_DATASET_TEMP=${SOURCE_DATASET//<EDIT>/$edit}
    python ~/projects/codetrace/codetrace/type_inf_exp/scripts/pipeline_steering.py \
    --datadir $DATADIR/$edit \
    --source_dataset $SOURCE_DATASET_TEMP \
    --model $MODEL \
    --tensor_name steering_tensor-2000.pt \
    --expdir $EXPDIR/$edit  \
    --max_size 2000 \
    --batchsize 10 \
    --rand_steering_tensor \
    --seed 42 >> steering_pipeline_${LANG}_${edit}.out 2>&1
done