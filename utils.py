import os
from glob import glob
from constants import *
from pathlib import Path
import shutil
from pydub import AudioSegment

def find_files(dir, pattern="*.wav"):
    files = []
    for path in Path(directory).rglob(pattern):
        files.append(path)
    return files

def extract_wav(in_dir, out_dir):
    files = find_files(in_dir)
    for path in files:
        os.rename(path, out_dir + path.name)

def get_audio_duration(filename):
    sound= AudioSegment.from_wav(filename)
    duration = sound.duration_seconds
    return duration

def make_wav_scp(wave_dir = WAV_DIR):
    files = find_files(wave_dir)
    f = open("wav.scp", "w")
    for path in files:
        recording_id = path.name.split('.')[0].split('-')[0]
        file_path = os.path.abspath(path)
        # print(path)
        f.write(recording_id + " " + file_path + "\n")
    f.close()

def make_segments(wave_dir = WAV_DIR):
    files = find_files(wave_dir)
    f = open("segments", "w")
    for path in files:
        uttid = path.name.split('.')[0]
        spkid = path.name.split('.')[0].split('-')[0]
        duration = get_audio_duration(path)
        
        f.write("{} {} 0.00 {}\n".format(uttid, spkid, str(duration)))
    f.close()

def make_utt2spk(wave_dir = WAV_DIR):
    files = find_files(wave_dir)
    # print(files)
    f = open("utt2spk", "w")
    for path in files:
        utter_id = path.name.split('.')[0]
        recording_id = path.name.split('.')[0].split('-')[0]

        f.write(utter_id + " " + recording_id + "\n")
    f.close()