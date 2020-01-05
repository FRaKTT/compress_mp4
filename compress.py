import os
import sys
import subprocess
from shutil import copyfile


EXIF_DATES = ['-createDate', '-mediaCreateDate', '-trackCreateDate', 
              '-modifyDate', '-mediaModifyDate', '-trackModifyDate']


def transcode(src, dst):
    """exec command: ffmpeg -i src_file -c:v libx264 -c:a copy -y dst_file"""
    cmd = ['ffmpeg', '-i', src, '-c:v', 'libx264', '-c:a', 'copy', '-y', dst]  # form command
    print(cmd)
    return_code = subprocess.call(cmd)  # run command
    print(return_code)


def names(src_files):
    """selecting mp4 files and forming names with original marks"""
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
    cmd = ['exiftool', '-tagsFromFile', src] + EXIF_DATES + [dst]
    print(cmd)
    return_code = subprocess.call(cmd)


def get_metadata(tags, f):
    # cmd = ['exiftool'] + EXIF_DATES + [f]
    # cmd = ['exiftool', '-avgbitrate', target]
    cmd = ['exiftool'] + tags + [f]
    print(cmd)
    return_code = subprocess.call(cmd)

# strange changes after transcoding:
# Media Time Scale: 90к -> 48k
# Track Volume: 100% -> 0%
# Video Frame Rate: 29.991 -> 30

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('need files in arguments:')
        print('> python3 transcode.py target.mp4')
        sys.exit()
    arguments = sys.argv[1:]  # skip script name
    names_pairs = names(arguments)
    for target, orig in names_pairs:
        copyfile(target, orig)  # copy original file
        transcode(orig, target)  # compress file
        get_metadata(EXIF_DATES + ['-avgBitrate'], orig)
        get_metadata(EXIF_DATES + ['-avgBitrate'], target)
        copy_metadata_dates(orig, target)  # copy dates
        get_metadata(EXIF_DATES + ['-avgBitrate'], target)


