#!/usr/bin/python3

"""
archives files in a folder while preserving the last few versions
"""
import sys, os, shutil, argparse
from datetime import date

DEFAULT_VERSIONS_TO_KEEP = 1 # 1 will keep only the current archive and 1 version back, 0 would mean current archive only

def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

def delete_old_versions(fileList, numberToKeep, targetPath):
        print('Deleting all but the last %s old versions...'%(numberToKeep))
        fileList.sort()
        for i in range(len(fileList) - numberToKeep):
                print('Deleted ' + fileList[i])
                os.remove(os.path.join(targetPath, fileList[i]))

# get optional args
parser=argparse.ArgumentParser()
parser.add_argument('targetPath', help='The target root folder')
parser.add_argument('targetSubFolder', help='The target folder to archive inside the root')
parser.add_argument('--versioncount', help='Number of version histories to keep, the rest are deleted', type=int, default=DEFAULT_VERSIONS_TO_KEEP)
parser.add_argument('--archivename', help='The target folder to archive inside the root')
parser.add_argument('--force', help='Overwrite existing file', action="store_true")

args=parser.parse_args()

print(sys.argv)
print(args)

if len(sys.argv)<= 1:
        raise Exception('Missing arguments for targetPath and targetSubfolder')

targetPath = args.targetPath
targetSubFolder = args.targetSubFolder
versionsToKeep = args.versioncount
archiveName = args.archivename if args.archivename else targetSubFolder    # name of the archive will be the name of the subfolder

today = str(date.today())

shouldMakeArchive = True
targetArchiveName = '%s-%s.%s'%(archiveName,today,"zip") # eg. testarchive-2019-01-21.zip

archivesToDelete = []
filesAtTarget = os.listdir(targetPath)
for f in filesAtTarget:
        if os.path.isfile(os.path.join(targetPath, f)):
                if  f == targetArchiveName :
                        shouldMakeArchive = False
                elif archiveName in f :
                        archivesToDelete.append(f)


if shouldMakeArchive or args.force:
        make_archive(os.path.join(targetPath, targetSubFolder), os.path.join(targetPath, targetArchiveName))
        print("Created archive " + targetArchiveName)
else:
        print("archive already exists, use --force to overwrite")

if len(archivesToDelete) > 0 and len(archivesToDelete) > versionsToKeep :
        delete_old_versions(archivesToDelete, versionsToKeep, targetPath)
else:
        print("No old version deleted")