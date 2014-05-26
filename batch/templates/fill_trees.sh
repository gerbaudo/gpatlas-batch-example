#!/bin/bash

#PBS -q atlas

BASE_DIR="${base_dir}"
DEST_DIR="${dest_dir}"
IN_FILE="${input_filelist}"
OUT_FILE="${out_file}"
SCRATCH_DIR="${scratch_dir}"

echo "Starting on `hostname`, `date`"
mkdir -p ${SCRATCH_DIR}
cd ${SCRATCH_DIR}
${BASE_DIR}/python/check_hft_trees.py -i ${BASE_DIR}/${IN_FILE} -o ${OUT_FILE}
echo "copying output file ${OUT_FILE}"
ls -lh ${OUT_FILE}
cp -p ${OUT_FILE} ${DEST_DIR}
cd ${BASE_DIR}
echo "cleaning up ${SCRATCH_DIR}"
rm -rf ${SCRATCH_DIR}
echo "Done, `date`"
