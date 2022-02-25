# megadetector

## Setup

### Configure your environment (run only once)

```sh
cd /share/$GROUP/$USER
git clone https://github.com/bird-feeder/megadetector.git megadetector_picam
cd megadetector_picam

chmod +x configure.csh
./configure.csh
```

### Connect to your Google Drive account (run only once)

```sh
./rclone config
# >>>> Prompt responses:
# n/s/q> n
# name> gdrive
# Storage> drive
# client_id> leave empty
# client_secret> leave empty
# scope> 1
# root_folder_id> leave empty
# service_account_file> leave empty
# y/n> n
# y/n> n
# COPY THE URL IN THE OUTPUT, AND OPEN IT IN YOUR BROWSER TO LOG IN...
#     ...THEN COPY THE CODE THAT WILL SHOW UP
# config_verification_code> PASTE THE CODE YOU COPIED HERE
# y/n> n
# y/e/d> y
# e/n/d/r/c/s/q> q
```

## Submit a job

```sh
./submit
```


## Post-job submission commands (picam specific)

```sh
set NEW_FOLDER_NAME="downloaded_`date +%m-%d-%Y`"
# If you're the original owner, run:
./rclone move -P --transfers 32 --stats-one-line --max-depth 1 --filter "+ *.jpg" --filter "- *" gdrive:"picam" gdrive:"picam-downloaded/$NEW_FOLDER_NAME"
# If you're NOT the original owner, run:
./rclone --drive-shared-with-me move -P --transfers 32 --stats-one-line --max-depth 1 --filter "+ *.jpg" --filter "- *" gdrive:"picam" gdrive:"picam-downloaded/$NEW_FOLDER_NAME"
```


## Post-job completion commands (picam specific)

```sh
module load conda tensorflow
python exclude_specific_classes.py --images-dir "picam" --exclude "fox_squirrel"
```


## Upload the data to Google Drive when the job is complete

```sh
./upload
```


## Sync the images on label-studio

- Log in to the remote server

```sh
ssh ubuntu@<REPLACE_WITH_SERVER_IP>
```

- Download the files

```sh
cd "/home/ubuntu/apps/label-studio"
NEW_FOLDER_NAME="local-files/picam/downloaded_$(date +%m-%d-%Y)"
# If you're the original owner, run:
rclone copy gdrive:"downloaded_$(date +%m-%d-%Y)" "$NEW_FOLDER_NAME" -P --stats-one-line --transfers 32
# If you're NOT the original owner, run:
rclone --drive-shared-with-me copy gdrive:"downloaded_$(date +%m-%d-%Y)" "$NEW_FOLDER_NAME" -P --stats-one-line --transfers 32
```

- Sync the files

```sh
python sync_picam.py
```
