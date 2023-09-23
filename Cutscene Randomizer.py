# School Days Cutscene Scrambler
# This script assumes you have extracted the games GPK files
# Please place this script in the script/English folder
#
# Scrambles cutscenes, so they run completely out of order
# I've only had the game crash once, but I expect that won't be the last
# The script itself is very buggy atm

import distutils.dir_util as dir_util
import distutils.file_util as file_util
import os
import random
import time


def scrambleDirectory(directory):
    print("Scrambling directory " + directory)
    dirfileList = os.listdir(directory)
    # I probably don't need this, but I don't know if python allows me to edit
    # arrays while they are being iterated through in a for loop without it bugging out
    newfileList = dirfileList
    dir_util.mkpath(".tmp/")
    randomFiles = list()
    for i in dirfileList:
        checking = True
        while checking:
            randomFilename = random.choice(newfileList)
            if not randomFilename in randomFiles:
                checking = False
        randomFiles.append(randomFilename)
        file_util.move_file(directory + i, ".tmp/" + randomFilename)
        print(i, "is now", randomFilename)
    dir_util.remove_tree(directory)
    dir_util.copy_tree(".tmp/", directory)
    dir_util.remove_tree(".tmp/")


dir_util.copy_tree("./00", "./balls/")
dir_util.copy_tree("./01", "./balls/")
dir_util.copy_tree("./02", "./balls/")
dir_util.copy_tree("./03", "./balls/")
dir_util.copy_tree("./04", "./balls/")
dir_util.copy_tree("./05", "./balls/")
scrambleDirectory("./balls/")
dir_util.remove_tree("./00")
dir_util.remove_tree("./01")
dir_util.remove_tree("./02")
dir_util.remove_tree("./03")
dir_util.remove_tree("./04")
dir_util.remove_tree("./05")
fileList = os.listdir("./balls/")
for i in fileList:
    folderName = i[0:2]
    dir_util.mkpath("./" + folderName + "/")
    file_util.copy_file("./balls/" + i, "./" + folderName + "/" + i)
dir_util.remove_tree("./balls/")
