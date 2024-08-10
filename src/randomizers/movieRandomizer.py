import os
import re
import shutil
import argparse

def collectAllFiles(movieFolders):
    allFiles = []
    for folder in movieFolders:
        for root, _, files in os.walk(folder):
            for file in files:
                allFiles.append((os.path.join(root, file), folder, os.path.relpath(root, folder)))
    return allFiles

def shuffleFiles(allFiles):
    import random
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
            print("Error copying file.")
        finally:
            print(f"Copied {shuffledFilePath} to {targetFilePath}")

def randomizeMovies(basePath):
    regexPattern = r'^Movie\d{2}$'
    movieFolderPattern = re.compile(regexPattern)
    
    folders = []
    for entry in os.listdir(basePath):
        folderPath = os.path.join(basePath, entry)
        if os.path.isdir(folderPath) and movieFolderPattern.match(entry):
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
    parser = argparse.ArgumentParser(description="Randomize movie files in MovieXX folders.")
    parser.add_argument("basePath", type=str, help="Base path to search for MovieXX folders")
    
    args = parser.parse_args()
    
    randomizeMovies(args.basePath)