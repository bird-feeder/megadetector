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

### Download the data from Google Drive

```sh
set GOOGLE_DRIVE_FOLDER_FULL_PATH="/REPLACE/WITH/GOOGLE_DRIVE/FOLDER/PATH"  # EDIT THIS (see comments)*
# *if you're not the original owner of the folder, don't add `/shared_with_me/` in `GOOGLE_DRIVE_FOLDER_FULL_PATH`;
#     ...otherwise, type down the full path

# If you're the original owner of the folder, use:
./rclone copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" -P
# If you're NOT the original owner of the folder, use:
./rclone --drive-shared-with-me copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" -P
```

### Set folder name and confidence threshold

```sh
set IMAGES_DIR="REPLACE_ME_WITH_FOLDER_NAME"  # EDIT THIS (ONLY THE FOLDER NAME, NOT THE FULL PATH)
set CONFIDENCE="REPLACE_ME_WITH_CONFIDENCE_THRESHOLD"  # MUST BE DECIMAL
```

### Set the job time assuming `$TOTAL_NUM_OF_IMGS / 60`

```sh
set TOTAL_NUM_OF_IMGS=`ls $IMAGES_DIR/*.JPG | wc -l`
set JOB_TIME=`expr $TOTAL_NUM_OF_IMGS / 60`
if ( $JOB_TIME < 10 ) set JOB_TIME=10
sed -i "/#BSUB -W/c\#BSUB -W $JOB_TIME # <<<<<<<<<<<<<< EDIT TIME! (in minutes)" megadetector_job.csh
echo "Will allocate $JOB_TIME minutes to the job"
```

### Submit the job

```sh
bsub < run_mycode.csh $IMAGES_DIR $CONFIDENCE
```

### Upload the data to Google Drive when the job is complete

```sh
set GOOGLE_DRIVE_FOLDER_FULL_PATH="/REPLACE/WITH/GOOGLE_DRIVE/FOLDER/PATH"  # EDIT THIS (see comments)*
# *if you're not the original owner of the folder, don't add `/shared_with_me/` in `GOOGLE_DRIVE_FOLDER_FULL_PATH`;
#     ...otherwise, type down the full path

# If you're the original owner of the folder, use:
./rclone copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" -P
# If you're NOT the original owner of the folder, use:
./rclone --drive-shared-with-me copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" -P
```
