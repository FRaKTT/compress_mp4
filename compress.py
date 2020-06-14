import os
import sys
import subprocess
from shutil import copyfile

# exiftool flags
EXIF_DATES = ['-createDate', '-mediaCreateDate', '-trackCreateDate', 
              '-modifyDate', '-mediaModifyDate', '-trackModifyDate']


def run_command(cmd):
    """Run command using subprocess module"""
    print(' '.join(cmd))
    return_code = subprocess.run(cmd)
    return return_code


def transcode(src, dst):
    """Exec ffmpeg command"""
    # ffmpeg -i src_file -c:v libx264 -c:a copy -y dst_file
    cmd = [
        'ffmpeg', 
        '-i', src, 
        '-c:v', 'libx264', # libx264 for video
        '-c:a', 'copy', # copy audio
        '-y', # overwrite output file without asking 
        dst]
    run_command(cmd)


def names(src_files):
    """Select mp4 files and form names with 'original' marks"""
    src_orig_pairs = []
    orig_mark = '_original'
    for src in src_files:
        if os.path.isfile(src):  # select only files
            dirname, basename = os.path.split(src)
            body, ext = os.path.splitext(basename)
            if ext.lower() == '.mp4':  # select only mp4
                orig_basename = body + ext + orig_mark
                orig = os.path.join(dirname, orig_basename)
                src_orig_pairs.append((src, orig))
    return src_orig_pairs


def copy_metadata_dates(src, dst):
    cmd = ['exiftool', '-tagsFromFile', src, '-overwrite_original'] + EXIF_DATES + [dst]
    run_command(cmd)


def get_metadata(filename, *tags):
    cmd = ['exiftool'] + list(tags) + [filename]
    run_command(cmd)

# strange changes after transcoding:
# Media Time Scale: 90к -> 48k
# Track Volume: 100% -> 0%
# Video Frame Rate: 29.991 -> 30

if __name__ == '__main__':
    try:
        arguments = sys.argv[1:]  # skip script name (sys.argv[0])
    except:
        print('need files in arguments:')
        print('> python3 compress.py target.mp4')
        sys.exit()

    for target, orig in names(arguments):
        copyfile(target, orig)  # copy original file
        transcode(orig, target)  # compress file
        print()
        get_metadata(orig, *EXIF_DATES, '-avgBitrate')
        get_metadata(target, *EXIF_DATES, '-avgBitrate')
        copy_metadata_dates(orig, target)  # copy dates
        get_metadata(target, *EXIF_DATES, '-avgBitrate')


