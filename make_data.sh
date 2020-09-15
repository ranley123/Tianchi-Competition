if [ $# -ne 2 ]; then
  echo "Usage: $0 <callhome-speech> <out-data-dir>"
  echo "e.g.: $0 /mnt/data/LDC2001S97 data/"
  exit 1;
fi

src_dir=$1
data_dir=$2

tmp_dir=$data_dir/.tmp/
mkdir -p $tmp_dir

 awk '{print $1}' $data_dir/wav.scp > $tmp_dir/reco.list

 awk '{print $1, $2}' $data_dir/segments > $data_dir/utt2spk
 utils/utt2spk_to_spk2utt.pl $data_dir/utt2spk > $data_dir/spk2utt
 mv $data_dir/segments .
# utils/validate_data_dir.sh --no-text --no-feats $data_dir
 utils/fix_data_dir.sh $data_dir
