from info import *
import os
from subprocess import call
import argparse


parser = argparse.ArgumentParser('Detetion, tracking, and submission creation!')
parser.add_argument('--experiment_name', type=str, default='yolox_l', help='Optional name of experiment')
parser.add_argument('--video_id', type=str, default=None, required=True, help='Absolute path file with video id and paths')
parser.add_argument('--cuda_path', default='/usr/local/cuda-11.3/lib64', type=str, help='CUDA library path')
parser.add_argument('--submission_name', default='submission.txt', type=str, help='Output submission file')
parser.add_argument('--tracker', default='BYTE', type=str, choices=['BYTE', 'SORT'], help='Tracker used')
parser.add_argument('--img_size', default=640, type=int, help='Detector input image size')
args = parser.parse_args()

vids = load_ids_and_paths(args.video_id)

################################################################################
os.chdir('/content/PersonGONE/detector_and_tracker')
os.environ['LD_LIBRARY_PATH'] = args.cuda_path
os.environ['PYTHONPATH'] = os.getcwd()
for vid in vids:
    call(['python', '/content/PersonGONE/detector_and_tracker/tools/detector_with_tracker.py',
           '-expn', args.experiment_name,
           '--path', os.path.join(inpainting_path, vid['name'], vid['name']+'.mp4'),
           '--roi_path', os.path.join(rois_path, vid['name']+'.json'),
           '--tracker', args.tracker,
           '--tsize', str(args.img_size),
           '-f', 'exps/aic_yolox_l.py',
           '-c', 'checkpoints/{:s}/best_ckpt.pth'.format(args.experiment_name)
           ])
################################################################################

################################################################################
os.chdir('..')
call(['python', '/content/PersonGONE/utils/tracks_processing.py',
      os.path.abspath(os.path.join('detector_and_tracker', 'YOLOX_outputs', args.experiment_name)),
      args.submission_name,
      args.video_id
      ])
################################################################################

