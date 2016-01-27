# -*- coding: utf-8 -*-
import os, sys
import subprocess as sp

ffmpeg_call = "X://ffmpeg/bin/ffmpeg.exe" # call ffmpeg on Windows
digest_folder = "X://somewhere/" # put all original file here
source_extension = "TOD"
output_extension = "mpg"
final_output_name = "output" # with extension output_extension
output_quality = "1" # 1 = original better than 2 better than 3...
output_volume = "9" # dB, "10" for +10 dB, "-10" for -10dB
header_name = "header.jpg"
trailer_name = "trailer.jpg"
headertrailer_durations = "5" # output's header or trailer duration in seconds

# files summary view
def summary():
    print '死懶鬼！搵緊檔案喇。。。' # "welcome! searching files..."
    sys.stdout.flush()
    count = 0
    for file in os.listdir(digest_folder):
        if file.endswith(source_extension):
            print '搵到 ' + file + ' ！' # "found!"
            sys.stdout.flush()
            count += 1
    print '夾埋搵到 ' + str(count) + ' 個 ' + source_extension + ' 檔案。' # "total files found."
    sys.stdout.flush()
    return count
    
# digest all original file, convert into output_extension format, delete the original one
def transcode():
    if int(output_volume) > 0:
        print '哇！啲片咁細聲，全部加大 ' + output_volume + ' dB！' # tell increase dB to all files
    if int(output_volume) < 0:
        print '哇！啲片咁細聲，全部減低 ' + output_volume + ' dB！' # tell decrease dB to all files
    handled_list = []
    for file in os.listdir(digest_folder):
        if file.endswith(source_extension):
            print file + ' 轉緊去 ' + output_extension + '。。。' # "converting into..."
            sys.stdout.flush()
            tranform_format = [ffmpeg_call, '-i', file, '-qscale:v', output_quality, '-af', ('volume=' + output_volume + 'dB'), '-deinterlace', (file[0:-3] + output_extension)]
            sp.call(tranform_format)
            os.remove(file)
            handled_list.append(file[0:-3] + output_extension)
            print file + ' 轉左去 ' + output_extension + ' 喇！' # "converted"
            sys.stdout.flush()
    print '搵到嘅 ' + source_extension + ' 都轉曬。' # "all found files have been converted"
    sys.stdout.flush()
    return handled_list

# header, trailer add into if needed
def header_trailer(seconds):
    status = 0 # 0 = no header trailer, 1 = header, 2 = trailer, 3 = header and trailer
    for file in os.listdir(digest_folder):
        if file == header_name:
            print '睇黎你要加個頭LOGO，等陣。。。' # "header needed"
            sys.stdout.flush()
            header_add = [ffmpeg_call, '-loop', '1', '-i', header_name, '-t', seconds, '-pix_fmt', 'yuv420p', ('header.' + output_extension)]
            sp.call(header_add)
            status += 1
            print '搞掂，頭LOGO已做。' # "header made"
            sys.stdout.flush()
        if file == trailer_name:
            print '睇黎你要加個尾LOGO，等陣。。。' # "trailer needed"
            sys.stdout.flush()
            trailer_add = [ffmpeg_call, '-loop', '1', '-i', trailer_name, '-t', seconds, '-pix_fmt', 'yuv420p', ('trailer.' + output_extension)]
            sp.call(trailer_add)
            status += 2
            print '搞掂，尾LOGO已做。' # "trailer made"
            sys.stdout.flush()
    return status

# combine all transformed format files into one output file
def combine(handled_list):
    concat_files = '|'.join(handled_list)
    status = header_trailer(headertrailer_durations)
    if status == 1:
        concat_files = 'header.mpg|' + concat_files
    if status == 2:
        concat_files += '|trailer.mpg'
    if status == 3:
        concat_files = 'header.mpg|' + concat_files + '|trailer.mpg'
    concat_command = [ffmpeg_call, '-i', ("concat:" + concat_files), '-c', 'copy', (final_output_name + '.' + output_extension)]
    print '全部檔案合併緊做一個，等陣啦。。。' # "Combining all files into one..."
    sys.stdout.flush()
    sp.call(concat_command)
    if status == 1:
        os.remove("header.mpg")
    if status == 2:
        os.remove("trailer.mpg")
    if status == 3:
        os.remove("header.mpg")
        os.remove("trailer.mpg")
    print 'YEAH!!! 完成！！！ 再見喇死懶鬼' # ”Process completed, please go check, Goodbye!“
    sys.stdout.flush()

#program sequence
def start():
    os.chdir(digest_folder) #go to target working directory
    if summary() > 0:
        combine(transcode())
    else:
        print '無檔案搵到。。。係咪玩野呀！！！再見' # "no files found, end"
        sys.stdout.flush()

#start program
start()
