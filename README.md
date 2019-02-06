# Python file history

Use it to make a backup zip archive of any subfolder at the desired path, appending the current date to the archive and deleting all old versions, except the desired number.

Usage:
`main.py /home/MyFolder/subfolderToArchive 2`

Will create an archive inside /home/MyFolder/ called subfolderToArchive-YYYY-MM-DD.zip.

Also will scan the folder for any archives with the same name but with older dates and will delete all but the most recent 2.
If the last param is not provided, will default to 1.

Optional args: -b (backup folder path to send an archive copy to), -a (archive name), -c (version count to store)

Should work on all OS if python3 is installed
