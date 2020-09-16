. ./cmd.sh
. ./path.sh
set -e
mfccdir=`pwd`/mfcc
vaddir=`pwd`/mfcc
data_root=data/test
stage=4
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

    for name in test; do
	utils/fix_data_dir.sh data/$name
        utils/utt2spk_to_spk2utt.pl data/$name/utt2spk > data/$name/spk2utt
    done
fi

if [ $stage -le 2 ]; then

    for name in test; do
    	steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj 40 \
      --cmd "$train_cmd" --write-utt2num-frames true\
      data/$name exp/make_mfcc $mfccdir
    #	utils/fix_data_dir.sh data/$name

 	sid/compute_vad_decision.sh --nj 20 --cmd "$train_cmd" \
      data/$name exp/make_vad $vaddir
    #utils/fix_data_dir.sh data/$name
	
    diarization/vad_to_segments.sh --nj 40 --cmd "$train_cmd" \
	        data/${name} data/test_segmented

	local/nnet3/xvector/prepare_feats.sh --nj 20 --cmd "$train_cmd" \
      data/${name}_segmented data/${name}_segmented_cmn exp/${name}_cmn
    #  utils/fix_data_dir.sh data/${name}_cmn
  #diarization/vad_to_segments.sh --nj 40 --cmd "$train_cmd" \
            #          data/${name}_cmn data/${name}_cmn_segmented	  
    done
fi

#if [ $stage -le 3 ]; then
#	local/nnet3/xvector/tuning/run_xvector_1a.sh --stage $stage --train-stage -1 \
#  --data data/train_cmn --nnet-dir $nnet_dir \
#  --egs-dir $nnet_dir/egs
#fi
if [ $stage -le 4 ]; then
	diarization/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 5G" \
	    --nj 10 --window 1.5 --period 0.75 --apply-cmn false \
	        --min-segment 0.5 $nnet_dir \
		    data/test_segmented $nnet_dir/xvectors_test
#sid/compute_vad_decision.sh --nj 20 --cmd "$train_cmd" \
	     # data/train_cmn exp/make_vad $vaddir
 #   utils/fix_data_dir.sh data/$name
fi
