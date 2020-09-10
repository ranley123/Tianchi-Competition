import os
from glob import glob
from pathlib import Path
import shutil
from pydub import AudioSegment

def find_files(dir, pattern="*.wav"):
    files = []
    for path in Path(dir).rglob(pattern):
        files.append(path)
    return files

def extract_wav(in_dir, out_dir):
    files = find_files(in_dir)
    for path in files:
        os.rename(path, out_dir + path.name)

def get_audio_duration(filename):
    sound= AudioSegment.from_wav(filename)
    duration = sound.duration_seconds
    return round(duration,4)

def load_n_col(filename, first_title=True, numpy=False):
    data = []
    with open(filename) as fp:
        for line in fp:
            data.append(line.strip().split())
    if first_title:
        data = data[1:]
    columns = list(zip(*data))
    if numpy:
        columns = [np.array(list(i)) for i in columns]
    else:
        columns = [list(i) for i in columns]
    return columns

def make_wav_scp(wave_dir):
    files = find_files(wave_dir)
    f = open("wav.scp", "w")
    for path in files:
        recording_id = path.name.split('.')[0].split('-')[0]
        file_path = os.path.abspath(path)
        # print(path)
        f.write(recording_id + " " + file_path + "\n")
    f.close()

def make_segments(wav_dir, out_dir):
    files = find_files(wav_dir)
    cols = load_n_col(os.path.join(wav_dir,"train.txt"))
    assert(len(files) == len(cols[0]))

    f = open(os.path.join(out_dir, "segments"), "w")
    for i in range(len(files)):
        path = files[i]
        uttid = path.name.split('.')[0]
        spkid = ""
        if int(cols[1][i]) == 1:
            spkid = "fake"
        else:
            spkid = cols[2][i]
        duration = get_audio_duration(path)
        
        f.write("{} {} 0.00 {}\n".format(uttid, spkid, str(duration)))
    f.close()

def make_utt2spk(wave_dir):
    files = find_files(wave_dir)
    # print(files)
    f = open("utt2spk", "w")
    for path in files:
        utter_id = path.name.split('.')[0]
        recording_id = path.name.split('.')[0].split('-')[0]

        f.write(utter_id + " " + recording_id + "\n")
    f.close()

if __name__ == "__main__":
    make_segments("/Users/ranley/Downloads/train")