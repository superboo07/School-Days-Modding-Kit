import os
import shutil
import argparse
import random

def collectAllFiles(scriptFolders):
    allFiles = []
    for folder in scriptFolders:
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

def randomizeScripts(basePath):
    scriptFolderPath = os.path.join(basePath, "Script")
    
    if not os.path.isdir(scriptFolderPath):
        print(f"No 'Script' folder found in '{basePath}'.")
        return
    
    allFiles = collectAllFiles([scriptFolderPath])
    if not allFiles:
        print("No files found in the 'Script' folder.")
        return
    
    print(f"Collected files: {allFiles}")
    shuffledFilePaths = shuffleFiles(allFiles)
    distributeFiles(allFiles, shuffledFilePaths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomize script files in Script folder.")
    parser.add_argument("basePath", type=str, help="Base path to search for Script folder")
    
    args = parser.parse_args()
    
    randomizeScripts(args.basePath)