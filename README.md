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
./rclone config
# >>>>> Prompt responses:
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
# config_verification_code> ENTER THE CODE YOU COPIED HERE
# y/n> n
# y/e/d> y
# e/n/d/r/c/s/q> q
```

## Run for every job

#### Set folder name and job time

---

##### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> NEEDS MANUAL EDITING
```sh
set IMAGES_DIR="REPLACE_ME_WITH_FOLDER_NAME"  # EDIT THIS (ONLY THE FOLDER NAME, NOT THE FULL PATH)
set GOOGLE_DRIVE_FOLDER_FULL_PATH="/REPLACE/WITH/GOOGLE_DRIVE/FOLDER/PATH"  # EDIT THIS (THE FULL PATH)*
# *if you're not the original owner of the folder, don't add `/shared_with_me/` in `GOOGLE_DRIVE_FOLDER_FULL_PATH`;
#     ...otherwise, type down the full path
set CONFIDENCE="REPLACE_ME_WITH_CONFIDENCE_THRESHOLD"  # MUST BE DECIMAL
```
##### END OF MANUAL EDITING <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

---

```sh
set TOTAL_NUM_OF_IMGS=`ls $IMAGES_DIR/*.JPG | wc -l`
set JOB_TIME=`expr $TOTAL_NUM_OF_IMGS / 2 / 60 + $TOTAL_NUM_OF_IMGS / 4 / 60`
if ( $JOB_TIME < 10 ) set JOB_TIME=10
sed -i "/#BSUB -W/c\#BSUB -W $JOB_TIME # <<<<<<<<<<<<<< EDIT TIME! (in minutes)" megadetector_job.csh
echo "Will allocate $JOB_TIME minutes to the job"
```

#### Download the data from Google Drive

[See this section to know which command to use](####Set-folder-name-and-job-time)

- If you're **not** the original owner of the folder, use:

```sh
./rclone --drive-shared-with-me copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" -P
```

- If you're the original owner of the folder, use:

```sh
./rclone copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" -P
```

### Submit the job

```sh
bsub < run_mycode.csh $IMAGES_DIR $CONFIDENCE
```

#### Upload the data to Google Drive when the job is complete

[See this section to know which command to use](####Set-folder-name-and-job-time)

- If you're **not** the original owner of the folder, use:

```sh
./rclone --drive-shared-with-me copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" -P
```

- If you're the original owner of the folder, use:

```sh
./rclone copy "$IMAGES_DIR/output" gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" -P
```
