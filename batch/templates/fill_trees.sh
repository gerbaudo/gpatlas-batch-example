#!/bin/bash

#PBS -q atlas

BASE_DIR="${base_dir}"
DEST_DIR="${dest_dir}"
OUT_FILE="${out_file}"
SCRATCH_DIR="${scratch_dir}"

echo "Starting on `hostname`, `date`"
mkdir -p ${SCRATCH_DIR}
cd ${SCRATCH_DIR}
${BASE_DIR}/python/check_hft_trees.py -o ${OUT_FILE}
cp -p ${OUT_FILE} ${DEST_DIR}
echo "Done, `date`"
