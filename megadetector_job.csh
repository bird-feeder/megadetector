#!/bin/tcsh
#BSUB -n 1
#BSUB -W 60 # <<<<<<<<<<<<<< EDIT TIME! (in minutes)
#BSUB -J megadetector_%J
#BSUB -o logs/megadetector_%J.out
#BSUB -e logs/megadetector_%J.err
#BSUB -q gpu
#BSUB -R "select[rtx2080||gtx1080||p100]"
#BSUB -gpu "num=2:mode=shared:mps=yes"


# EDIT THESE LINES: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
set IMAGES_DIR="$1"
set CONFIDENCE="$2"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# ----------------------- DO NOT EDIT BELOW THIS LINE! -----------------------

nvidia-smi
module load conda cuda tensorflow
set AVAIL_GPUS=`python get_avail_gpus.py`

setenv CUDA_VISIBLE_DEVICES "$AVAIL_GPUS"; python megadetector.py --images-dir "/gpfs_common/share03/$GROUP/$USER/megadetector/$IMAGES_DIR" --confidence "$CONFIDENCE"
