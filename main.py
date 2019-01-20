"""
archives files in a folder while preserving the last few versions
"""
import sys
import os, shutil
from datetime import date

def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

#print(sys.argv)
targetPath = sys.argv[1] if len(sys.argv) >= 2 else "C:\\Games\\Steam\\userdata\\24593029"
targetSubFolder = sys.argv[2] if len(sys.argv) >= 3 else "219740"
archiveName = sys.argv[3] if len(sys.argv) >= 4 else targetSubFolder

today = str(date.today())

shouldMakeArchive = True
targetArchiveName = '%s-%s.%s'%(archiveName,today,"zip") # eg. testarchive-2019-01-21.zip

filesAtTarget = os.listdir(targetPath)
for f in filesAtTarget:
        if os.path.isfile(os.path.join(targetPath, f)) and f == targetArchiveName :
                shouldMakeArchive = False
                break


if shouldMakeArchive:
        make_archive(os.path.join(targetPath, targetSubFolder), os.path.join(targetPath, targetArchiveName))
else:
        print("archive already exists")