import os
import argparse
import GPKFileHandling.unpackGPK as unpackGPK
import restoreBackToStock

def makeModdable(path):
    if not (os.path.isfile(path + "RouteProcSDHQ.dll") | os.path.isfile(path + "RouteProcSD.dll")):
        print("Days game not detected!")
        return False

    if restoreBackToStock.restore(path):
        print("Restored game back to stock")
    fileNames = [f for f in os.listdir(path + "/Packs/") if os.path.isfile(os.path.join(path + "/Packs/", f))]
    for file in fileNames:
        unpackGPK.unpackGPK(path + "/Packs/" + file, path)

    print("Unpack finished, renaming packs to .packs so the game can't see it")
    os.rename(path + "/Packs/", path + "/.Packs/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Readys School Days for modding. ")
    parser.add_argument("path", help="Path to the GPK file to be unpacked.")
    args = parser.parse_args()

    makeModdable(args.path)
