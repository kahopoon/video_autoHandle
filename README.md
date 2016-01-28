# video_autoHandle
Put all "A" kind format video files, convert all to "B" kind format with trimming audio volume, detect if header or trailer footage is/are needed, and combine (concatenate) all files into one file in "B" kind format. Upload that to youtube, send email with youtube link when finished.

# Prerequisite
This script is designed for Windows platform, you have to change command pattern if you would like to run it on Linux.

FFmpeg
https://www.ffmpeg.org/

Google APIs Client Library for Python
https://developers.google.com/api-client-library/python/start/installation

Youtube video upload script
https://developers.google.com/youtube/v3/guides/uploading_a_video

# Usage
python main.py -s [start_time] -e [end_time] -d [dB] -h [seconds_shutdown]
start_time: first video file 's time stamp to start
end_time: last video file's time stamp to end
dB: increase of decrease volume in dB
seconds_shutdown: shutdown machine in specific seconds after end of script

# Example
python main.py -s 00:00:30 -e 00:10:00 -d 6 -h 60
Command state the output video file will be start at 30 second from the first video file and end with last video file's 10 minutes. Output will be gain 6dB and shutdown machine on after 60 seconds of finished script
