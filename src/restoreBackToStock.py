import os
import argparse
import shutil

def restore(path):
    if not (os.path.isfile(path + "RouteProcSDHQ.dll") | os.path.isfile(path + "RouteProcSD.dll")):
        print("Days game not detected!")
        return False

    # Rename .Packs back to Packs
    if os.path.isdir(path + "./.Packs/"):
        old_path = path + "/.Packs/"
        new_path = path + "/Packs/"
        print(f"Renaming folder from {old_path} to {new_path}")
        os.rename(old_path, new_path)
    else:
        return False

    fileNames = [f for f in os.listdir(path + "/Packs/") if os.path.isfile(os.path.join(path + "/Packs/", f))]
    fileNames = [os.path.splitext(f)[0] for f in fileNames if os.path.isfile(os.path.join(path + "/Packs/", f))]
    for file in fileNames:
        folder_path = path + file
        print(f"Removing folder: {folder_path}")
        shutil.rmtree(folder_path)
    return True
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Readys School Days for modding. ")
    parser.add_argument("path", help="Path to the GPK file to be unpacked.")
    args = parser.parse_args()

    restore(args.path)
