#!/bin/bash

#PBS -q atlas


SCRATCH_DIR="/scratch/asoffa/${JOB_NUMBER}"
BASE_DIR="${BASE_DIR}"
DEST_DIR="${DEST_DIR}"

echo "Starting on `hostname`, `date`"
cd ${SCRATCH_DIR}
${SCRATCH_DIR}/python/check_hft_trees.py -o ${OUT_FILE} ${opt}
cp -p ${OUT_FILE} ${DEST_DIR}
echo "Done, `date`"
