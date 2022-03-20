#!/bin/tcsh

cat <<'EOF'
((
\\``.
\_`.``-.
( `.`.` `._
 `._`-.    `._
   \`--.   ,' `.
    `--._  `.  .`.
     `--.--- `. ` `.
         `.--  `;  .`._
           :-   :   ;. `.__,.,__ __
 JOB        `\  :	,-(     ';o`>.
 SUBMISSION   `-.`:   ,'   `._ .:  (,-`,
 SCRIPT          \    ;      ;.  ,:
             ,"`-._>-:        ;,'  `---.,---.
             `>'"  "-`       ,'   "":::::".. `-.
              `;"'_,  (\`\ _ `:::::::::::'"     `---.
               `-(_,' -'),)\`.       _      .::::"'  `----._,-"")
                   \_,': `.-' `-----' `--;-.   `.   ``.`--.____/
MOHAMMAD ALYETAMA    `-^--'                \(-.  `.``-.`-=:-.__)
malyeta@ncsu.edu                            `  `.`.`._`.-._`--.)
                                                 `-^---^--.`--
'EOF'


set GOOGLE_DRIVE_FOLDER_FULL_PATH="picam"
set NEW_FOLDER_NAME="downloaded_`date +%m-%d-%Y`"
mkdir -p "picam/$NEW_FOLDER_NAME"
set IMAGES_DIR="picam/$NEW_FOLDER_NAME"

set CONFIDENCE="0.8"

printf "ENTER THE JOB TIME (MUST BE IN hh:mm; for example: 01:30): "
set JOB_TIME=$<
sed -i "/#BSUB -W/c\#BSUB -W $JOB_TIME" megadetector_job.csh

printf "ARE YOU THE ORIGINAL OWNER OF THE FOLDER (Y/N)? "
set RCLONE_ANS=$<


cat <<'EOF'
    ___   _____      ___  _ _    ___   _   ___ ___ _  _  ___   ___   _ _____ _         
   |   \ / _ \ \    / | \| | |  / _ \ /_\ |   |_ _| \| |/ __| |   \ /_|_   _/_\        
   | |) | (_) \ \/\/ /| .` | |_| (_) / _ \| |) | || .` | (_ | | |) / _ \| |/ _ \ _ _ _ 
   |___/ \___/ \_/\_/ |_|\_|____\___/_/ \_|___|___|_|\_|\___| |___/_/ \_|_/_/ \_(_(_(_)
                                                                                       
'EOF'

if ( $RCLONE_ANS == y | $RCLONE_ANS == Y ) ./rclone copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" --transfers 32 -P --stats-one-line
if ( $RCLONE_ANS == n | $RCLONE_ANS == N ) ./rclone --drive-shared-with-me copy gdrive:"$GOOGLE_DRIVE_FOLDER_FULL_PATH" "$IMAGES_DIR" --transfers 32 -P --stats-one-line
echo "\nFinished downloading!\n"

bsub -env "GROUP='$GROUP', USER='$USER'" < megadetector_job.csh

sleep 5
bjobs
echo "Check status by running: bjobs\n"
