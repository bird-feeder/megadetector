#!/bin/tcsh

cat <<'EOF'

                                                           .
                  .                                    .::'
                  `::.          CONFIGURATION        .`  :
                   :  '.            SCRIPT         .`o    :
                  :    o'.                        ~~}     :
                  :     {~~                        `:     `:.
                .:`     :'                          :    .:   `.
             .`   :.    :                           :   :       `.
           .`       :   :                           `.   `.       :
          :       .'   .'                            `.    `..    :
          :    ..'    .'   MOHAMMAD ALYETAMA          `:.. '.````:
          :''''.' ..:'     malyeta@ncsu.edu              ::`::`:   :.      .
        .:   :'::'::        ..........................:"``````'"`:   `:""": :
.:"""""""""""`''''''""""""""                     ...........""""""`:   `:"`,'
:                            ..........""""""""""                   ':   `:
`............."""""""""""""""                                         `..:'
  `:..'

'EOF'

sleep 1
module load conda cuda tensorflow
pip install --user loguru humanfriendly jsonpickle GPUtil python-dotenv tqdm "pymongo[srv]" pandas matplotlib

wget -O megadetector_v4_1_0.pb https://lilablobssc.blob.core.windows.net/models/camera_traps/megadetector/md_v4.1.0/md_v4.1.0.pb

git clone https://github.com/microsoft/CameraTraps
git clone https://github.com/microsoft/ai4eutils

cp CameraTraps/detection/run_tf_detector_batch.py .
cp CameraTraps/visualization/visualize_detector_output.py .
rm CameraTraps/detection/run_tf_detector.py
mv run_tf_detector.py CameraTraps/detection

curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip
cd rclone-*-linux-amd64
chmod 755 rclone
cp rclone ..
cd ..
rm rclone-current-linux-amd64.zip
rm -rf rclone-*-linux-amd64

mkdir -p logs

mv submit.csh submit
chmod +x submit
mv upload.csh upload
chmod +x upload
