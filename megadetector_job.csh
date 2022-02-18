#!/bin/tcsh
#BSUB -n 1
#BSUB -W 01:00
#BSUB -J megadetector_%J
#BSUB -o logs/megadetector_%J.out
#BSUB -e logs/megadetector_%J.err
#BSUB -q gpu
#BSUB -R "select[rtx2080||gtx1080||p100]"
#BSUB -gpu "num=2:mode=shared:mps=yes"

nvidia-smi
module load conda cuda tensorflow
set AVAIL_GPUS=`python helpers.py --gpus`
echo "AVAIL_GPUS: $AVAIL_GPUS"
setenv CUDA_VISIBLE_DEVICES "$AVAIL_GPUS"; python megadetector.py --images-dir "/gpfs_common/share03/$GROUP/$USER/megadetector/$IMAGES_DIR" --confidence "$CONFIDENCE"
