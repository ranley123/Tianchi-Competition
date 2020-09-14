import os
from glob import glob
from pathlib import Path
import shutil
from pydub import AudioSegment

def find_files(dir, pattern="*.wav"):
    files = []
    for path in Path(dir).rglob(pattern):
        files.append(path)
    files = sorted(files)
    return files

def extract_wav(in_dir, out_dir):
    files = find_files(in_dir)
    for path in files:
        os.rename(path, out_dir + path.name)

def get_audio_duration(filename):
    sound= AudioSegment.from_wav(filename)
    duration = sound.duration_seconds
    return round(duration,4)

def load_n_col(filename, numpy=False):
    data = []
    with open(filename) as fp:
        for line in fp:
            data.append(line.strip().split())
    columns = list(zip(*data))
    if numpy:
        columns = [np.array(list(i)) for i in columns]
    else:
        columns = [list(i) for i in columns]
    return columns

def make_wav_scp(wav_dir, out_dir):
    files = find_files(wav_dir)
    f = open(os.path.join(out_dir, "wav.scp"), "w")
    for path in files:
        uttid = path.name.split('.')[0]
        file_path = os.path.abspath(path)
        # print(path)
        f.write("{} {}\n".format(uttid, file_path))
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

def make_utt2spk(wav_dir, out_dir):
    f = open(os.path.join(out_dir, "utt2spk"), "w")
    fr = open(os.path.join(wav_dir, "train.txt"), "r")
    lines = fr.readlines()

    for line in lines:
        parts = line.strip().split()
        uttid = parts[0].split('.')[0]
        spkid = parts[2]
        if spkid == "0":
            spkid = "fake"

        f.write("{} {}\n".format(uttid, spkid))
    f.close()

def make_spk2utt(utt2spk, out_dir):
    cols = load_n_col(utt2spk)
    spks = cols[1]
    f = open(os.path.join(out_dir, "spk2utt"), "w")
    prev = spks[0]
    cur_list = []

    for i in range(len(spks)):
        cur = spks[i]
        if prev == cur:
            cur_list.append(cols[0][i])
        else:
            res = ""
            for item in cur_list:
                res += " " + item
            f.write("{}{}\n".format(prev, res))
            prev = cur
    
    f.close()




if __name__ == "__main__":
    make_segments("data/train", "data/train")
    make_wav_scp("data/train", "data/train")
    make_utt2spk("data/train", "data/train")
