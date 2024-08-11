import os
import re
import shutil
import argparse
import random

def collectAllFiles(movieFolders):
    allFiles = []
    for folder in movieFolders:
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

def randomizeMovies(basePath):
    moviePattern = re.compile(r'^Movie\d{2}$')
    movieZPattern = re.compile(r'^MovieZ.*$')
    
    movieFolders = []
    movieZFolders = []
    
    for entry in os.listdir(basePath):
        folderPath = os.path.join(basePath, entry)
        if os.path.isdir(folderPath):
            if moviePattern.match(entry):
                movieFolders.append(folderPath)
            elif movieZPattern.match(entry):
                movieZFolders.append(folderPath)
    
    if not movieFolders and not movieZFolders:
        print(f"No folders matching the patterns found in '{basePath}'.")
        return
    
    if movieFolders:
        print(f"Movie folders found: {movieFolders}")
        movieFiles = collectAllFiles(movieFolders)
        if movieFiles:
            print(f"Collected movie files: {movieFiles}")
            shuffledMovieFiles = shuffleFiles(movieFiles)
            distributeFiles(movieFiles, shuffledMovieFiles)
        else:
            print("No files found in the Movie folders.")
    
    if movieZFolders:
        print(f"MovieZ folders found: {movieZFolders}")
        movieZFiles = collectAllFiles(movieZFolders)
        if movieZFiles:
            print(f"Collected MovieZ files: {movieZFiles}")
            shuffledMovieZFiles = shuffleFiles(movieZFiles)
            distributeFiles(movieZFiles, shuffledMovieZFiles)
        else:
            print("No files found in the MovieZ folders.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomize movie files in MovieXX and MovieZ* folders.")
    parser.add_argument("basePath", type=str, help="Base path to search for MovieXX and MovieZ* folders")
    
    args = parser.parse_args()
    
    randomizeMovies(args.basePath)