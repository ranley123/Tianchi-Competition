. ./cmd.sh
. ./path.sh
set -e
mfccdir=`pwd`/mfcc
vaddir=`pwd`/mfcc
data_root=data/train
stage=2
nnet_dir=exp/xvector_models
num_components=1024 # the number of UBM components (used for VB resegmentation)
ivector_dim=400 # the dimension of i-vector (used for VB resegmentation)

if [ $stage -le 0 ]; then
    ln -s /home/dcase/Documents/yuhuan/datasets/kaldi/egs/callhome_diarization/v1/utils .
    ln -s /home/dcase/Documents/yuhuan/datasets/kaldi/egs/callhome_diarization/v1/steps .
    ln -s /home/dcase/Documents/yuhuan/datasets/kaldi/egs/callhome_diarization/v1/sid .
    ln -s /home/dcase/Documents/yuhuan/datasets/kaldi/egs/callhome_diarization/v1/diarization .
fi

if [ $stage -le 1 ]; then

    for name in train; do
       # utils/fix_data_dir.sh data/$name
        utils/utt2spk_to_spk2utt.pl data/$name/utt2spk > data/$name/spk2utt
    done
fi

if [ $stage -le 2 ]; then

    for name in train; do
    	steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj 40 \
      --cmd "$train_cmd" --write-utt2num-frames true \
      data/$name exp/make_mfcc $mfccdir
    	utils/fix_data_dir.sh data/$name  
    done
fi


