#!/bin/tcsh
#BSUB -n 1
#BSUB -W 01:00
#BSUB -J megadetector_%J
#BSUB -o logs/megadetector_%J.out
#BSUB -e logs/megadetector_%J.err
#BSUB -q gpu
#BSUB -R "select[rtx2080||gtx1080||p100]"
#BSUB -gpu "num=2:mode=shared:mps=yes"

module load conda cuda tensorflow
nvidia-smi

set AVAIL_GPUS=`python helpers.py --gpus`
echo "AVAIL_GPUS: $AVAIL_GPUS"
if ( $AVAIL_GPUS == "" ) set AVAIL_GPUS="1"

set NEW_FOLDER_NAME="downloaded_`date +%m-%d-%Y`"
set IMAGES_DIR="/gpfs_common/share03/$GROUP/$USER/megadetector_picam/picam/$NEW_FOLDER_NAME"

setenv CUDA_VISIBLE_DEVICES "$AVAIL_GPUS"; python megadetector.py --images-dir "$IMAGES_DIR" --jobid "$LSB_JOBID" --confidence "0.8" --animal-only
