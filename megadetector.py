# bsub -Is -n 1 -W 100 -q gpu -R "select[rtx2080||gtx1080||p100]" -gpu "num=2:mode=shared:mps=yes" tcsh

# module load conda cuda tensorflow

# change this line in `CameraTraps/detection/run_tf_detector.py`
"""
        self.tf_session = tf.Session(config=config, graph=detection_graph)
# to: 
from tensorflow.compat.v1 import ConfigProto
        config = ConfigProto()
        config.gpu_options.allow_growth = True
        self.tf_session = tf.Session(config=config, graph=detection_graph)
"""

# set AVAIL_GPUS=`python -c "import GPUtil;print(','.join([str(x) for x in GPUtil.getAvailable(order='load', limit=1, maxLoad=0.5, maxMemory=0.5, includeNan=False, excludeID=[], excludeUUID=[])]))"`

# set AVAIL_GPUS=`python get_avail_gpus.py`

# set IMAGES_DIR="sample"
# set CONFIDENCE="0.01"
# setenv CUDA_VISIBLE_DEVICES "$AVAIL_GPUS"; python megadetector.py --images-dir "/gpfs_common/share03/$GROUP/$USER/megadetector/$IMAGES_DIR" --confidence "$CONFIDENCE"

import json
import os
import shutil
import sys
import time
from datetime import datetime
from glob import glob
from pathlib import Path

import tensorflow as tf
from loguru import logger
from tqdm import tqdm

sys.path.insert(0, f'{os.getcwd()}/ai4eutils')
sys.path.insert(0, f'{os.getcwd()}/CameraTraps')

from CameraTraps.detection import run_tf_detector_batch
from CameraTraps.visualization import visualize_detector_output


def setup_dirs(images_dir):
    images_list = glob(f'{images_dir}/*.JPG')
    logger.debug(f'Images directory: {images_dir}')
    output_folder = f'{images_dir}/output'
    visualization_dir = f'{output_folder}/tmp'
    Path(output_folder).mkdir(exist_ok=True)
    Path(visualization_dir).mkdir(exist_ok=True)
    for subf in ['no_detections', 'with_detections_and_bb', 'with_detections']:
        Path(f'{output_folder}/{subf}').mkdir(exist_ok=True)
    output_file_path = output_folder + f'/data_{ts}.json'
    return images_list, output_folder, visualization_dir, output_file_path


def filter_output(data, output_folder, visualization_dir, images_dir):
    for image in tqdm(data['images']):
        if not image['detections']:
            out_path_nd = f'{output_folder}/no_detections/{Path(image["file"]).name}'
            if not Path(out_path_nd).exists():
                shutil.copy2(image['file'], out_path_nd)
        elif image['detections']:
            img_file = visualization_dir + '/anno_' + images_dir.replace(
                '/', '~') + '~' + Path(image['file']).name
            out_path_with_bb = f'{images_dir}/output/with_detections_and_bb/{Path(img_file).name}'
            if not Path(out_path_with_bb).exists():
                shutil.copy2(img_file, out_path_with_bb)
            out_path_wd = f'{images_dir}/output/with_detections/{Path(image["file"]).name}'
            if not Path(out_path_wd).exists():
                shutil.copy2(image['file'], out_path_wd)
    return f"{output_folder}/no_detections", f"{output_folder}/with_detections"


def main(images_dir, restored_results):
    logger.debug(tf.__version__)
    logger.debug(f'GPU available: {tf.test.is_gpu_available()}')
    images_list, output_folder, visualization_dir, output_file_path = setup_dirs(
        images_dir)
    logger.info(f'Number of images in folder: {len(images_list)}')
    results = run_tf_detector_batch.load_and_run_detector_batch(
        model_file='megadetector_v4_1_0.pb',
        image_file_names=images_list,
        checkpoint_path=ckpt_file,
        confidence_threshold=confidence,
        checkpoint_frequency=100,
        results=restored_results,
        n_cores=0,
        use_image_queue=False)
    logger.debug(
        'Finished running `run_tf_detector_batch.load_and_run_detector_batch`')
    run_tf_detector_batch.write_results_to_file(results,
                                                output_file_path,
                                                relative_path_base=None)
    logger.debug(
        'Finished running `run_tf_detector_batch.write_results_to_file`')
    visualize_detector_output.visualize_detector_output(
        detector_output_path=output_file_path,
        out_dir=f'{output_folder}/tmp',
        confidence=confidence,
        images_dir=images_dir,
        is_azure=False,
        sample=-1,
        output_image_width=700,
        random_seed=None,
        render_detections_only=False)
    logger.debug(
        'Finished running `visualize_detector_output.visualize_detector_output`'
    )
    with open(output_file_path) as j:
        data = json.load(j)
    out_folder_nd, out_folder_wd = filter_output(data, output_folder,
                                                 visualization_dir, images_dir)
    logger.debug('Finished running `filter_output`')
    len_nd = len(glob(f"{output_folder}/no_detections/*"))
    len_wd = len(glob(f"{output_folder}/with_detections/*"))
    logger.info(f'Number of images with no detections: {len_nd}')
    logger.info(f'Number of images with detections: {len_wd}')
    logger.info(f'Data file path: {output_file_path}')


if __name__ == '__main__':
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    logger.add(f'logs/logs_{ts}.log')

    try:
        assert all(True if arg in sys.argv else False
                   for arg in ['--confidence', '--images-dir'])
        for arg in sys.argv:
            try:
                next_arg = sys.argv[sys.argv.index(arg) + 1]
            except IndexError:
                break
            if arg == '--images-dir':
                images_dir = next_arg
                assert Path(images_dir).exists(
                ), 'Specified images path does not exist'
            elif arg == '--confidence':
                assert isinstance(
                    float(next_arg),
                    float), 'Confidence threshold needs to be a decimal number'
                confidence = float(next_arg)
    except AssertionError as err:
        logger.exception(err)
        sys.exit(1)

    ckpt_file = f'{images_dir}/output/checkpoint_{ts}.json'

    if '--resume' in sys.argv:
        try:
            assert Path(ckpt_file).exists(
            ), f'Could not find a checkpoint file {ckpt_file}'
            with open(ckpt_file) as f:
                saved = json.load(f)
            assert 'images' in saved, \
                'The file saved as checkpoint does not have the correct fields; cannot be restored'
            restored_results = saved['images']
            logger.info(
                f'Restored {len(restored_results)} entries from the checkpoint'
            )
        except AssertionError as err:
            logger.exception(err)
            sys.exit(1)
    else:
        restored_results = []

    main(images_dir, restored_results)
