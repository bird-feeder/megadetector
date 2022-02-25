#!/bin/tcsh

cat <<'EOF'


                     _.--.
                 .-"`_.--.\   .-.___________
               ."_-"`     \\ (  0;------/\"'`
             ,."=___      =)) \ \      /  \
              `~` .=`~'~)  ( _/ /     /    \
      =`---====""~`\          _/     /      \
                    `-------"`      /  DATA  \
                                   /  UPLOAD  \
                                  (   SCRIPT   )
MOHAMMAD ALYETAMA                  '._      _.'
malyeta@ncsu.edu                      '----'

'EOF'

set NEW_FOLDER_NAME="downloaded_`date +%m-%d-%Y`"
printf "ARE YOU THE ORIGINAL OWNER OF THE FOLDER (Y/N)? "
set RCLONE_ANS=$<

cat <<'EOF'
     _   _ ___ _    ___   _   ___ ___ _  _  ___   ___   _ _____ _         
    | | | | _ | |  / _ \ /_\ |   |_ _| \| |/ __| |   \ /_|_   _/_\        
    | |_| |  _| |_| (_) / _ \| |) | || .` | (_ | | |) / _ \| |/ _ \ _ _ _ 
     \___/|_| |____\___/_/ \_|___|___|_|\_|\___| |___/_/ \_|_/_/ \_(_(_(_)
                                                                          
'EOF'

if ( $RCLONE_ANS == y | $RCLONE_ANS == Y ) set DRIE_SHARED_WITH_ME=""
if ( $RCLONE_ANS == n | $RCLONE_ANS == N ) set DRIVE_SHARED_WITH_ME="--drive-shared-with-me"

eval './rclone $DRIVE_SHARED_WITH_ME copy "picam/output/" --include "*.json" --max-depth 1 gdrive:"picam-detections/$NEW_FOLDER_NAME" --transfers 32 -P --stats-one-line'
eval './rclone $DRIVE_SHARED_WITH_ME copy "picam/output/with_detections" gdrive:"picam-detections/$NEW_FOLDER_NAME/with_detections" --transfers 32 -P --stats-one-line'
eval './rclone $DRIVE_SHARED_WITH_ME copy "picam/output/with_detections_excluded" gdrive:"picam-detections/$NEW_FOLDER_NAME/with_detections_excluded" --transfers 32 -P --stats-one-line'
eval 'set META="picam/output/meta.txt"; ./rclone $DRIVE_SHARED_WITH_ME size --filter "+ *.jpg" --filter "- *.json" gdrive:picam-detections/$NEW_FOLDER_NAME > "$META" && ./rclone $DRIVE_SHARED_WITH_ME copy "$META" gdrive:picam-detections/$NEW_FOLDER_NAME

echo "\nFinished uploading!\n"
