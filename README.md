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

## Submit a job

```sh
./submit.csh
```

## Upload the data to Google Drive when the job is complete

```sh
./upload.csh
```
