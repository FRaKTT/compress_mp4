# compress_mp4
Compress mp4 video files without visible loss of quality

Principle of operation - transoding with libx264
Base command: "ffmpeg -i src_file.mp4 -c:v libx264 -c:a copy dst_file.mp4"

Need ffmpeg and exiftool
