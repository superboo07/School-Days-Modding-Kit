import os
import re
import shutil
import argparse
from collections import defaultdict
import random

def collectParentFiles(eventFolders):
    parentFiles = []
    
    for folder in eventFolders:
        for root, _, files in os.walk(folder):
            for file in files:
                baseName, ext = os.path.splitext(file)
                if len(baseName) == 13:
                    parentFiles.append((os.path.join(root, file), folder, os.path.relpath(root, folder), ext))
    
    print(f"Collected parent files: {parentFiles}")  # Log collected parent files
    return parentFiles

def shuffleFiles(parentFiles):
    parentFilePaths = [file[0] for file in parentFiles]
    print(f"Parent files before shuffling: {parentFilePaths}")  # Log parent files before shuffling
    shuffledParentFiles = parentFilePaths[:]
    random.shuffle(shuffledParentFiles)
    print(f"Parent files after shuffling: {shuffledParentFiles}")  # Log parent files after shuffling
    return shuffledParentFiles

def distributeFiles(parentFiles, shuffledParentFiles):
    shuffledPathsIter = iter(shuffledParentFiles)
    for parentFilePath, parentBaseFolder, parentRelativeDir, parentExt in parentFiles:
        parentFileName = os.path.basename(parentFilePath)
        parentBaseName, _ = os.path.splitext(parentFileName)
        targetDir = os.path.join(parentBaseFolder, parentRelativeDir) if parentRelativeDir else parentBaseFolder
        os.makedirs(targetDir, exist_ok=True)
        shuffledParentFilePath = next(shuffledPathsIter)
        
        try:
            # Copy and rename shuffled parent file
            targetParentFilePath = os.path.join(targetDir, parentBaseName + parentExt)
            shutil.copy(shuffledParentFilePath, targetParentFilePath)
            print(f"Copied {shuffledParentFilePath} to {targetParentFilePath}")
        except Exception as e:
            print(f"Error processing file: {e}")

def randomizeEvents(basePath):
    regexPattern = r'^Event\d{2}$'
    eventFolderPattern = re.compile(regexPattern)
    
    folders = []
    for entry in os.listdir(basePath):
        folderPath = os.path.join(basePath, entry)
        if os.path.isdir(folderPath) and eventFolderPattern.match(entry):
            folders.append(folderPath)
    
    if not folders:
        print(f"No folders matching the pattern found in '{basePath}'.")
        return
    
    print(f"Folders found: {folders}")
    parentFiles = collectParentFiles(folders)
    if not parentFiles:
        print("No parent files found in the folders.")
        return
    
    print(f"Collected parent files: {parentFiles}")
    shuffledParentFiles = shuffleFiles(parentFiles)
    distributeFiles(parentFiles, shuffledParentFiles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomize event files in EventXX folders.")
    parser.add_argument("basePath", type=str, help="Base path to search for EventXX folders")
    
    args = parser.parse_args()
    
    randomizeEvents(args.basePath)