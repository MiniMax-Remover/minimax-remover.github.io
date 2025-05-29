import os
import numpy as np
from decord import VideoReader, cpu
from moviepy.editor import ImageSequenceClip

def convert_with_decord_to_16fps(directory=".", target_fps=12):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            filepath = os.path.join(directory, filename)
            print(f"Processing: {filename}")
            try:
                vr = VideoReader(filepath, ctx=cpu(0))
                original_fps = vr.get_avg_fps()
                total_frames = len(vr)

                # 计算采样间隔
                step = int(round(original_fps / target_fps))
                if step <= 0:
                    step = 1  # 防止除以0或负数

                sampled_indices = list(range(0, 72, step))
                frames = [vr[i].asnumpy() for i in sampled_indices]

                # 使用 moviepy 写入视频
                clip = ImageSequenceClip(frames, fps=target_fps)
                output_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}_12fps.mp4")
                clip.write_videofile(output_path, codec="libx264", fps=target_fps, audio=False)

            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    convert_with_decord_to_16fps()