import os
import struct
import zlib
from pathlib import Path
import argparse

class GpkEntry:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.isPacked = True

def createGpkIndex(entries):
    indexData = bytearray()
    entryOffsets = []
    entrySizes = []

    # Write placeholder for index section
    for entry in entries:
        nameBytes = entry.name.encode('utf-16le')
        nameLength = len(nameBytes) // 2
        indexData.extend(struct.pack('<H', nameLength))
        indexData.extend(nameBytes)
        indexData.extend(b'\x00' * 6)  # Reserved or padding
        entryOffsets.append(len(indexData))  # Save current index position for offset
        indexData.extend(struct.pack('<I', 0))  # offset (to be filled later)
        entrySizes.append(len(entry.data))  # size (to be filled later)
        indexData.extend(b'\x00' * 4)  # Reserved
        indexData.extend(struct.pack('<I', len(entry.data)))  # Unpacked size
        indexData.extend(b'\x00')  # Header length placeholder

    # Compute total size of index data
    indexSize = len(indexData)
    indexData.extend(b'\x00' * (indexSize % 16))  # Align to 16 bytes boundary

    for i, entry in enumerate(entries):
        entryOffset = indexSize + sum(entrySizes[:i])
        struct.pack_into('<I', indexData, entryOffsets[i], entryOffset)

    return indexData

def encryptData(data, key):
    return bytearray([b ^ key[i % len(key)] for i, b in enumerate(data)])

def packFolderToGpk(folderPath, gpkFile, key):
    entries = []
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            filePath = Path(root) / file
            with open(filePath, 'rb') as f:
                data = f.read()
                compressedData = zlib.compress(data)
                entry = GpkEntry(file, compressedData)
                entries.append(entry)

    indexData = createGpkIndex(entries)
    encryptedIndexData = encryptData(indexData, key)

    # Ensure the output directory exists
    outputDir = os.path.dirname(gpkFile)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Write the GPK file
    tempFile = gpkFile + '.temp'
    with open(tempFile, 'wb') as f:
        for entry in entries:
            f.write(entry.data)

        # Write the index section
        indexStartOffset = f.tell()
        f.write(b'STKFile0PIDX')
        f.write(struct.pack('<I', len(encryptedIndexData)))
        f.write(b'STKFile0PACKFILE')
        f.write(struct.pack('<I', len(encryptedIndexData)))
        f.write(encryptedIndexData)

    # Replace the original file with the temp file
    os.rename(tempFile, gpkFile)

    print(f"GPK file created: {gpkFile}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack a folder into a GPK file.")
    parser.add_argument("folderPath", help="Path to the folder to be packed.")
    parser.add_argument("gpkFile", help="Path to the GPK file to be created.")
    parser.add_argument("key", type=lambda x: bytes.fromhex(x), help="Encryption key as a hex string.")

    args = parser.parse_args()

    packFolderToGpk(args.folderPath, args.gpkFile, args.key)
