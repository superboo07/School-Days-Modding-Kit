# School Days Cutscene Scrambler
# This script assumes you have extracted the games GPK files
# Please place this script in the script/English folder
#
# Scrambles cutscenes so they run completely out of order
# I've only had the game crash once but I expect that won't be the last
# The script itself is very buggy atm

import distutils.dir_util as dir_util
import distutils.file_util as file_util
import os
import random


def scrambleDirectory(directory):
    print("Scrambling directory " + directory)
    dirfileList = os.listdir(directory)
    dirfileList.pop(len(dirfileList) - 1)
    newfileList = dirfileList
    dir_util.mkpath("tmp/")
    for i in dirfileList:
        randomIndex = random.randint(0, len(newfileList) - 1)
        file_util.copy_file(directory + "/" + i, "tmp/")
        file_util.move_file("tmp/" + i, "tmp/" + newfileList[randomIndex])
        print(newfileList[randomIndex])
        newfileList.pop(randomIndex)
    dir_util.remove_tree(directory)
    dir_util.copy_tree("tmp/", directory)
    dir_util.remove_tree("tmp/")


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
    folderName = i[:2]
    dir_util.mkpath("./" + folderName + "/")
    file_util.move_file("./balls/" + i, "./" + folderName + "/")
dir_util.remove_tree("./balls/")
