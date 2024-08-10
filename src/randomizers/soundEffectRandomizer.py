import os
import re
import shutil
import argparse
import random

def collectAllFiles(seFolders):
    allFiles = []
    for folder in seFolders:
        for root, _, files in os.walk(folder):
            for file in files:
                allFiles.append((os.path.join(root, file), folder, os.path.relpath(root, folder)))
    return allFiles

def shuffleFiles(allFiles):
    filePaths = [file[0] for file in allFiles]
    random.shuffle(filePaths)
    return filePaths

def distributeFiles(allFiles, shuffledFilePaths):
    shuffledPathsIter = iter(shuffledFilePaths)
    for (originalFilePath, originalBaseFolder, originalRelativeDir) in allFiles:
        originalFileName = os.path.basename(originalFilePath)
        targetDir = os.path.join(originalBaseFolder, originalRelativeDir) if originalRelativeDir else originalBaseFolder
        os.makedirs(targetDir, exist_ok=True)
        targetFilePath = os.path.join(targetDir, originalFileName)
        shuffledFilePath = next(shuffledPathsIter)
        try:
            shutil.copy(shuffledFilePath, targetFilePath)
        except: 
            print("Error copying file. It's okay to ignore this!")
        finally:
            print(f"Copied {shuffledFilePath} to {targetFilePath}")

def randomizeSoundEffects(basePath, includeSoundEffects, includeVoices):
    regexParts = []
    if includeSoundEffects:
        regexParts.append(r'^(Se\d{2}|SysSe)')
    if includeVoices:
        regexParts.append(r'(Voice\d{2})$')
    
    if not regexParts:
        print("No options selected!")
        return
    
    regexPattern = '|'.join(regexParts)
    seFolderPattern = re.compile(regexPattern)
    
    folders = []
    for entry in os.listdir(basePath):
        folderPath = os.path.join(basePath, entry)
        if os.path.isdir(folderPath) and seFolderPattern.match(entry):
            folders.append(folderPath)
    
    if not folders:
        print(f"No folders matching the pattern found in '{basePath}'.")
        return
    
    print(f"Folders found: {folders}")
    allFiles = collectAllFiles(folders)
    if not allFiles:
        print("No files found in the folders.")
        return
    
    print(f"Collected files: {allFiles}")
    shuffledFilePaths = shuffleFiles(allFiles)
    distributeFiles(allFiles, shuffledFilePaths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomize sound effects based on regex parts.")
    parser.add_argument("basePath", type=str, help="Base path to search for sound effect folders")
    parser.add_argument("includeSoundEffects", action="store_true", help="Include sound effects as part of the regex (^(Se\\d{2}|SysSe)")
    parser.add_argument("includeVoices", action="store_true", help="Include voices as part of the regex (Voice\\d{2})$")
    
    args = parser.parse_args()
    
    randomizeSoundEffects(args.basePath, args.includeSoundEffects, args.includeVoices)