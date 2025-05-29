import decord
from decord import VideoReader, cpu
import numpy as np
from moviepy.editor import ImageSequenceClip
import os
from tqdm import tqdm
import cv2

# 找到当前目录下 h > w 的视频文件
video_files = [f for f in os.listdir('./') if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

for video_file in video_files:
    try:
        vr = VideoReader(video_file, ctx=cpu(0))
        h, w, _ = vr[0].shape
        if h <= w:
            continue  # 只处理 h > w 的视频

        # 计算新的尺寸
        new_h = int(h * 1.05)//32*32
        new_w = w

        print(f"Processing {video_file} - Original size: ({h}, {w}), New size: ({new_h}, {new_w})")

        # 读取并resize帧
        resized_frames = []
        for frame in tqdm(vr):
            resized = cv2.resize(frame.asnumpy(), (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            resized_frames.append(resized)

        # 使用moviepy写入视频
        output_filename = f"resized_{video_file}"
        fps = vr.get_avg_fps()
        clip = ImageSequenceClip(resized_frames, fps=fps)
        clip.write_videofile(output_filename, codec='libx264')

    except Exception as e:
        print(f"Failed to process {video_file}: {e}")