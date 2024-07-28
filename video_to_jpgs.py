from moviepy.editor import VideoFileClip
import numpy as np
import os
from datetime import timedelta
import glob

SAVING_FRAMES_PER_SEC = 15
LOCATION = '/Users/romanvisotsky/Documents/GitHub/ticktok_parsing/frames'


def fit_jpgs(video_file):
	video_clip = VideoFileClip(video_file)
	file_name  = video_file.split('/')[-1]

	if not os.path.isdir(f'{LOCATION}/{file_name}'):
		os.mkdir(f'{LOCATION}/{file_name}')

	saving_frames_per_sec = min(video_clip.fps , SAVING_FRAMES_PER_SEC)
	step = 1 / video_clip.fps if saving_frames_per_sec == 0 else 1 / saving_frames_per_sec

	count = 0
	for current_duration in np.arange(0,video_clip.duration , step):
		frame_filename = os.path.join(f'{LOCATION}/{file_name}', f"{count}.jpg")

		video_clip.save_frame(frame_filename , current_duration)
		count += 1


videos = glob.glob(f'/Users/romanvisotsky/Documents/GitHub/ticktok_parsing/videos/*.mp4')
for video_file in videos:

	fit_jpgs(video_file)

