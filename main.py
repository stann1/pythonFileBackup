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
parser.add_argument('targetFolder', help='The target folder to archive, archive is stored in the parent folder')
parser.add_argument('--versioncount', '-c', help='Number of version histories to keep, the rest are deleted', type=int, default=DEFAULT_VERSIONS_TO_KEEP)
parser.add_argument('--archivename', '-a', help='The target folder to archive inside the root')
parser.add_argument('--backupfolder', '-b', help='Additional copy of the archive will be stored in this folder, existing files are overwritten')
parser.add_argument('--force', help='Overwrite existing file', action="store_true")

args=parser.parse_args()

print(sys.argv)
print(args)

if len(sys.argv)<= 1:
        raise Exception('Missing arguments for targetPath and targetSubfolder')

targetFolder = args.targetFolder
destination = os.path.abspath(os.path.join(targetFolder, os.pardir))      # parent of the target folder
targetFolderName = os.path.basename(os.path.normpath(targetFolder))
versionsToKeep = args.versioncount
archiveName = args.archivename or targetFolderName    # name of the archive will be the name of the subfolder
backupFolder = args.backupfolder

today = str(date.today())

shouldMakeArchive = True
targetArchiveName = '%s-%s.%s'%(archiveName,today,"zip") # eg. testarchive-2019-01-21.zip

archivesToDelete = []
filesAtTarget = os.listdir(destination)
for f in filesAtTarget:
        if os.path.isfile(os.path.join(destination, f)):
                if  f == targetArchiveName :
                        shouldMakeArchive = False
                elif archiveName in f :
                        archivesToDelete.append(f)


if shouldMakeArchive or args.force:
        source = os.path.normpath(targetFolder)
        make_archive(source, os.path.join(destination, targetArchiveName))
        print("Created archive " + targetArchiveName)

        if backupFolder:
                make_archive(source, os.path.join(backupFolder, targetArchiveName))
                print("Created backup copy in " + backupFolder)
else:
        print("archive already exists, use --force to overwrite")

if len(archivesToDelete) > 0 and len(archivesToDelete) > versionsToKeep :
        delete_old_versions(archivesToDelete, versionsToKeep, destination)
else:
        print("No old version deleted")