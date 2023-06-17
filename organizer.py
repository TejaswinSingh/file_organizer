import sys
import os
import utils # own custom module
import shutil
import argparse
import time
from dupsremover import deleteDups
import remove_empty


def main():
    startTime = time.time()
    # Create the parser
    parser = argparse.ArgumentParser(description='File Organizer')

    # Add the optional arguments
    parser.add_argument('directory', nargs='?', default='.', help='directory_path')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--ignore', action='store_true', help='ignore sub directories')
    group.add_argument('-f', '--full', action='store_true', help='fully sorts sub directories')
    group.add_argument('-q', '--quick', action='store_true', help='quick sorts sub directories')

    # Parse the command line arguments
    args = parser.parse_args()

    # Check which flags the user provided
    if args.ignore:
        mode = 'ignore'
    elif args.full:
        mode = 'full'
    else:
        mode = 'quick'  # default
    
    cur_dir = args.directory
    # check validity of cur_dir
    if not os.path.exists(cur_dir) or not os.path.isdir(cur_dir):
        sys.exit(f"\nerror::1 >>>> path {cur_dir} doesn't exists <<<<\n")

    # make a dict to store the paths of all organizer buckets 
    # like audio, video, image, text etc...
    organizerBuckets = makeBuckets(cur_dir)

    organize(cur_dir, organizerBuckets, subfolders=mode) 
    # delete any empty folders
    remove_empty.remove(cur_dir)
    finishTime = time.time()
    executionTime = finishTime - startTime

    print(f"\nFinished in {executionTime:.4f}s\n")


# __________________________
def makeBuckets(folder):
    buckets = {}

    try:
        audioFolder = utils.makeFolder_try_organizer(folder, name='audio')
        buckets['audio'] = os.path.join(folder, audioFolder)  # get the full path name
        videoFolder = utils.makeFolder_try_organizer(folder, name='video')
        buckets['video'] = os.path.join(folder, videoFolder)
        textFolder = utils.makeFolder_try_organizer(folder, name='text')
        buckets['text'] = os.path.join(folder, textFolder)
        imagesFolder = utils.makeFolder_try_organizer(folder, name='image')
        buckets['image'] = os.path.join(folder, imagesFolder)
        subtitlesFolder = utils.makeFolder_try_organizer(folder, name='subtitle')
        buckets['subtitle'] = os.path.join(folder, subtitlesFolder)
    except Exception as e:
        sys.exit(f"Error >>>> {e} <<<<")

    return buckets
# _________________________ 


# ________________________
# organizes a given folder
def organize(folder, buckets, subfolders='full'):
    # files from subfolders will be moved to the organizer buckets of the parent folder
    # for full search we must ensure there are no duplicates in a given folder
    if subfolders == 'full':
        files = utils.getfiles(folder) 
        files = deleteDups(files, return_val='list')
        for file in files:
            try:
                if isAudio(file):
                    shutil.move(file, buckets['audio'])
                elif isVideo(file):
                    shutil.move(file, buckets['video'])
                elif isText(file):
                    shutil.move(file, buckets['text'])    
                elif isImage(file):
                    shutil.move(file, buckets['image']) 
                elif isSub(file):
                    shutil.move(file, buckets['subtitle']) 
            except Exception as e:
                print(f"{e}")

    # first we create an organizer flag file in each bucket folder
    for genre, path in buckets.items():
        try:
            with open(f"{path}\\organizer_{genre}.py", "w") as file:
                text = f"{genre}\n\n"
                text += "This is a flag file used by the organizer utility. DO NOT DELETE IT"
                file.write(text)
        except Exception as e:
            sys.exit(f"Error >>>> {e} <<<<")

    if subfolders == 'full':
        return

    # now we iterate through all items in the folder and put them in 
    # corresponding buckets
    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)
        if entry_path in buckets.values():   # this ensures we don't search our bucket folders
            continue
        if os.path.isfile(entry_path):
            try:
                if isAudio(entry_path):
                    shutil.move(entry_path, buckets['audio'])
                elif isVideo(entry_path):
                    shutil.move(entry_path, buckets['video'])
                elif isText(entry_path):
                    shutil.move(entry_path, buckets['text'])    
                elif isImage(entry_path):
                    shutil.move(entry_path, buckets['image']) 
                elif isSub(entry_path):
                    shutil.move(entry_path, buckets['subtitle']) 
            except Exception as e:
                print(f"{e}")
        elif os.path.isdir(entry_path): 
            if subfolders == 'ignore':  # ignore any subfolders
                continue 
            # organizes files in subfolders as well (default)
            elif subfolders == 'quick':  
                new_buckets = makeBuckets(entry_path)
                organize(entry_path, new_buckets, subfolders)   
# ___________________________________________________________
 


# music file formats
# _________________________________ #
#
# headers
audio_file_headers = [
    (b'ID3', 0),          # MP3
    (b'RIFF', 0),         # WAV
    (b'OggS', 0),         # OGG
    (b'fLaC', 0),         # FLAC
    (b'ftypM4A', 4),      # AAC
    (b'FORM', 0),         # AIFF
    (b'8PSID', 0),        # SID
    (b'PSM\x00', 0),      # PSF1 (PS1 Sound Format)
    (b'PSF', 0),          # PSF2 (Portable Sound Format)
    (b'PK', 30),          # MOD (ProTracker, FastTracker)
    (b'MThd', 0),         # MIDI
    (b'fLaC', 4),         # FLAC (alternate header signature)
    (b'FSSD', 0),         # SPC (SNES audio)
    (b'SN', 0),           # SND (Acorn/RISC OS audio)
    (b'SSND', 0),         # AIFF (AIFC)
    (b'ajkg', 4),         # AIFC (Compressed AIFF)
    (b'BM', 0),           # WMA, WMV (Windows Media Audio/Video)
    (b'PK\x03\x04', 0),   # ZIP (contains audio files)
    (b'fLaC', 8),         # OGG (Ogg FLAC)
    (b'ftypisom', 4),     # M4A (Apple Lossless)
    (b'fLaC', 4),         # ALAC (Apple Lossless, alternate signature)
    (b'\xFF\xFB', 0),     # MP3 (MPEG Layer 3)
    (b'\xFF\xF3', 0),     # MP3 (MPEG Layer 3)
    # Add more file headers as needed
]
# extensions
audio_file_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.aiff', '.sid', '.psf', '.mod', '.mid']
# ________________________________________________________ #



# video file formats
# ____________________________ #
#
# headers
video_file_headers = [
    (b'RIFF', 0),         # AVI
    (b'ftypmp42', 4),     # MP4
    (b'ftypisom', 4),     # MP4
    (b'ftypMSNV', 4),     # MP4
    (b'ftypM4V', 4),      # M4V
    (b'moov', 4),         # MOV
    (b'FLV', 0),          # FLV
    (b'3g2a', 4),         # 3G2
    (b'3gp', 4),          # 3GP
    (b'fLaC', 4),         # FLV (alternate header signature)
    # Add more file headers as needed
]
# extensions
video_file_extensions = ['.avi', '.mp4', '.m4v', '.mov', '.flv', '.3g2', '.3gp']
# _____________________________________ #
    


# Image file formats
# ____________________
# 
# headers
image_file_formats = {
    "JPEG": [
        (b'\xFF\xD8\xFF', 0)  # JPEG/JPG
    ],
    "PNG": [
        (b'\x89\x50\x4E\x47', 0)  # PNG
    ],
    "GIF": [
        (b'GIF', 0)  # GIF
    ],
    "BMP": [
        (b'\x42\x4D', 0)  # BMP
    ],
    "TIFF": [
        (b'\x49\x49\x2A\x00', 0),  # TIFF (little-endian)
        (b'\x4D\x4D\x00\x2A', 0)   # TIFF (big-endian)
    ],
    "WEBP": [
        (b'RIFF', 0),
        (b'WEBPVP8', 8),
        (b'WEBPVP8L', 8),
        (b'WEBPVP8X', 8)
    ],
    "ICO": [
        (b'\x00\x00\x01\x00', 0),  # ICO
        (b'\x00\x00\x02\x00', 0)   # CUR
    ],
    "PSD": [
        (b'8BPS', 0)  # PSD
    ],
    # Add more file formats and headers as needed
}
# extensions
image_file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.ico', '.psd']
# ________________________________________ #



# _____________________________________________________________________________________ #
# Checks image
def isImage(file):
    fileExtension = os.path.splitext(file)[1].lower()  # Get the lowercase extension of the file
    with open(file, "rb") as f:
        header = f.read(32)  # Read the first 32 bytes
        for format_name, headers in image_file_formats.items():
            for magic, offset in headers:
                if header.startswith(magic) or fileExtension in image_file_extensions:
                    return True
        return False
# ____________________ #



# _______________________________________________ #
# check Audio
def isAudio(file):
    fileExtension = os.path.splitext(file)[1] # returns a tuple containing two parts - base name and extension of the file
    #print(fileExtension)
    with open(file, "rb") as f:
        header = f.read(32)   # read the first 32 bytes
        for magic, offset in audio_file_headers:
            # this or is intentional
            if header.lower().startswith(magic.lower(), offset) or fileExtension.lower() in audio_file_extensions:
                return True
        return False
# _____________________ #

    

# ____________________________________________ #
# check video
def isVideo(file):
    fileExtension = os.path.splitext(file)[1]
    with open(file, "rb") as f:
        header = f.read(32)
        for magic, offset in video_file_headers:
            if header.lower().startswith(magic.lower(), offset) or fileExtension.lower() in video_file_extensions:
                return True
        return False
# _______________________ #



# ____________________ #
# check text
def isText(file):
    text_file_extensions = ['.txt', '.csv', '.log', '.xml', '.json', '.html', '.htm']
    fileExtension = os.path.splitext(file)[1]
    if fileExtension in text_file_extensions:
        return True
    return False
# ________________ #



# _______________ #
# check subtitles
def isSub(file):
    subtitle_extensions = [".srt", ".ssa", ".ass", ".sub", ".usf", ".sub", ".idx", ".vtt"]
    fileExtension = os.path.splitext(file)[1]
    if fileExtension.lower() in subtitle_extensions:
        return True
    return False
# _________________ #



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(f"\nError >>>> {e} <<<<\nProgram completion stopped. May lead to unexpected results\n")
