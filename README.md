# megadetector

## Setup

### Configure your environment (run only once)

```sh
cd /share/$GROUP/$USER
git clone https://github.com/Biodiversity-CatTracker2/megadetector.git
cd megadetector

chmod +x megadetector_setup.sh
./megadetector_setup.sh
```

### Connect to your Google Drive account (run only once)

```sh
./rclone config  # Follow the prompts (name the new remote: gdrive)
```

## Run for every job

### Set folder name and confidence threshold

```sh
set GOOGLE_DRIVE_FOLDER_FULL_PATH="GOOGLE_DRIVE/FOLDER/PATH"  # EDIT THIS (see comments)*
# *if you're not the original owner of the folder, don't type `Shared with me` in `GOOGLE_DRIVE_FOLDER_FULL_PATH`;
#     ...otherwise, type down the full path
set CONFIDENCE="REPLACE_ME_WITH_CONFIDENCE_THRESHOLD"  # EDIT THIS (MUST BE DECIMAL)
set IMAGES_DIR=`basename "${GOOGLE_DRIVE_FOLDER_FULL_PATH}"`  # DON'T EDIT
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
set JOB_TIME="01:00"  # EDIT THIS (hh:mm)
sed -i "/#BSUB -W/c\#BSUB -W $JOB_TIME" megadetector_job.csh
```

### Submit the job

```sh
bsub -env "IMAGES_DIR='$IMAGES_DIR', CONFIDENCE='$CONFIDENCE', GROUP='$GROUP', USER='$USER'" < megadetector_job.csh
```

### Upload the data to Google Drive when the job is complete

```sh
set GOOGLE_DRIVE_FOLDER_FULL_PATH="GOOGLE_DRIVE/FOLDER/PATH"  # EDIT THIS (see comments)*
# *if you're not the original owner of the folder, don't type `Shared with me` in `GOOGLE_DRIVE_FOLDER_FULL_PATH`;
#     ...otherwise, type down the full path
set IMAGES_DIR=`basename "${GOOGLE_DRIVE_FOLDER_FULL_PATH}"`  # DON'T EDIT

# If you're the original owner of the folder, use:
./rclone copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" --transfers 32 -P
# If you're NOT the original owner of the folder, use:
./rclone --drive-shared-with-me copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" --transfers 32 -P
```
