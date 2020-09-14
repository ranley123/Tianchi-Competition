. ./cmd.sh
. ./path.sh
set -e
mfccdir=`pwd`/mfcc
vaddir=`pwd`/mfcc
data_root=data/train
stage=1
nnet_dir=exp/xvector_models
num_components=1024 # the number of UBM components (used for VB resegmentation)
ivector_dim=400 # the dimension of i-vector (used for VB resegmentation)

if [ $stage -le 0 ]; then
    ln -s /home/ranley/Documents/kaldi/egs/callhome_diarization/v1/utils .
fi

if [ $stage -le 1 ]; then

    for name in train; do
        utils/fix_data_dir.sh data/$name
        utils/utt2spk_to_spk2utt.pl data/$name/utt2spk > data/$name/spk2utt
    done
fi