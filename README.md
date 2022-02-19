# megadetector

## Setup

### Configure your environment (run only once)

```sh
cd /share/$GROUP/$USER
git clone https://github.com/Biodiversity-CatTracker2/megadetector.git
cd megadetector

chmod +x configure.csh
./configure.csh
```

### Connect to your Google Drive account (run only once)

```sh
./rclone config
# Follow the prompts (name the new remote: gdrive)
```

## Run for every job

### Set folder name and confidence threshold

```sh
# IMPORTANT: Don't type "shared with me" or "My Drive" in GOOGLE_DRIVE_FOLDER_FULL_PATH!
set GOOGLE_DRIVE_FOLDER_FULL_PATH="THIS/IS/PLACEHOLDER"
set CONFIDENCE="PLACEHOLDER"
# Don't edit the line below
set IMAGES_DIR=`basename "${GOOGLE_DRIVE_FOLDER_FULL_PATH}"`
```

### Download the data from Google Drive

```sh
# If you're the original owner of the folder, use:
./rclone copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" --transfers 32 -P
# If you're NOT the original owner of the folder, use:
./rclone --drive-shared-with-me copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" --transfers 32 -P
```

### Set the job time

```sh
# Edit the line below to change the job time (hh:mm)
set JOB_TIME="01:00"
sed -i "/#BSUB -W/c\#BSUB -W $JOB_TIME" megadetector_job.csh
```

### Submit the job

```sh
bsub -env "IMAGES_DIR='$IMAGES_DIR', CONFIDENCE='$CONFIDENCE', GROUP='$GROUP', USER='$USER'" < megadetector_job.csh
```

### Upload the data to Google Drive when the job is complete

```sh
set GOOGLE_DRIVE_FOLDER_FULL_PATH="THIS/IS/PLACEHOLDER"
set IMAGES_DIR=`basename "${GOOGLE_DRIVE_FOLDER_FULL_PATH}"`

# If you're the original owner of the folder, use:
./rclone copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" --transfers 32 -P
# If you're NOT the original owner of the folder, use:
./rclone --drive-shared-with-me copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" --transfers 32 -P
```
