import moviepy
import csv
import random

from moviepy.editor import *

print("====加载节奏===")
beat_ls = []
with open('./beats/a1.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        beat_time = int(float(row[0])*10.0)
        beat_ls.append(beat_time)
print("====加载节奏完毕===")

print("====开始视频剪辑===")
clip_ls = []
for i,b in enumerate(beat_ls[:120]):
    start = random.randint(20,60*8)
    if i == 0:
        time = beat_ls[0]/10.0
    else:
        time = (beat_ls[i]-beat_ls[i-1])/10.0
    clip = VideoFileClip("./video/1.mp4").subclip(start,start+time)
    clip_ls.append(clip)
    print(str(i)+"/"+str(len(beat_ls)))
print("====节奏加载完毕===")
 
print("====开始视频合成===")
print(clip_ls)
finalclip = concatenate_videoclips(clip_ls)
print("====视频合成完毕===")

print("====开始加载音乐===")
audio_clip = AudioFileClip(r'./music/a.mp3').volumex(0.5)
audio = afx.audio_loop( audio_clip, duration=finalclip.duration)
final_video = finalclip.set_audio(audio)
print("====音乐加载完毕===")

print("====生成最终视频===")
final_video.write_videofile("./video/1_output2.mp4")