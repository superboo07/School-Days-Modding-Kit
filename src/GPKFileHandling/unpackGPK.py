# Ported from https://github.com/morkt/GARbro/blob/master/ArcFormats/Stack/ArcGPK.cs

import os
import struct
import zlib
from pathlib import Path
import pefile
import argparse

class GPKEntry:
    def __init__(self, name, offset, size, unpackedSize, isPacked, header=None):
        self.name = name
        self.offset = offset
        self.size = size
        self.unpackedSize = unpackedSize
        self.isPacked = isPacked
        self.header = header

class GPKOpener:
    def __init__(self, filePath, outputDir):
        self.filePath = filePath
        self.outputDir = outputDir
        self.entries = []

    def tryOpen(self):
        print(f"Attempting to open GPK file: {self.filePath}")
        with open(self.filePath, 'rb') as f:
            f.seek(0, os.SEEK_END)
            maxOffset = f.tell()
            print(f"File size: {maxOffset} bytes")

            idxOffset = maxOffset - 32

            if idxOffset <= 0:
                print("Invalid index offset. The file may be corrupt.")
                return False

            f.seek(idxOffset)
            lastBytes = f.read(32)
            print(f"Last 32 bytes of the file: {lastBytes}")

            if lastBytes[:11] != b'STKFile0PIDX':
                print("STKFile0PIDX signature not found. This may not be a valid GPK file.")

            if lastBytes[16:31] != b'STKFile0PACKFILE':
                print("STKFile0PACKFILE signature not found. This may not be a valid GPK file.")

            idxSize = struct.unpack('<I', lastBytes[12:16])[0]
            print(f"Index size: {idxSize} bytes")

            if idxSize > idxOffset:
                print("Index size is larger than the offset, indicating corruption.")
                return False

            idxOffset -= idxSize
            key = self.queryKey()

            if key is None:
                print("Failed to retrieve decryption key.")
                return False

            print("Decryption key retrieved successfully.")

            f.seek(idxOffset)
            indexData = f.read(idxSize)

            decryptedData = bytearray()
            for i in range(len(indexData)):
                decryptedData.append(indexData[i] ^ key[i % len(key)])

            print("Index data decrypted. Decompressing...")

            decompressedData = zlib.decompress(decryptedData[4:])
            print("Decompression complete. Parsing entries...")

            self.parseEntries(decompressedData)
            print(f"Parsed {len(self.entries)} entries from the index.")
            return True

    def queryKey(self):
        # This function will search for a decryption key in the executable files nearby.
        print("Querying for decryption key...")
        dirPath = os.path.dirname(self.filePath)
        parentDir = os.path.abspath(os.path.join(dirPath, os.pardir))
        exeFiles = list(Path(dirPath).glob("*.exe")) + list(Path(parentDir).glob("*.exe"))

        for exeFile in exeFiles:
            print(f"Checking executable: {exeFile}")
            code = self.extractResource(str(exeFile), "CODE", "CIPHERCODE")
            if code is not None:
                if len(code) == 20:
                    print("Found 20-byte key, trimming to 16 bytes.")
                    code = code[4:20]
                print(f"Key extracted successfully from {exeFile}.")
                return code

        print("No valid key found in the executables.")
        return None

    def extractResource(self, filePath, resourceType, resourceName):
        try:
            pe = pefile.PE(filePath)
            for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if entry.name and entry.name.string.decode() == resourceType:
                    for res in entry.directory.entries:
                        if res.name and res.name.string.decode() == resourceName:
                            rva = res.directory.entries[0].data.struct.OffsetToData
                            size = res.directory.entries[0].data.struct.Size
                            peData = pe.get_data(rva, size)
                            print(f"Resource data found: {peData.hex()}")
                            return peData
        except Exception as e:
            print(f"Failed to extract resource from {filePath}: {e}")
        return None

    def parseEntries(self, data):
        offset = 0
        while offset < len(data):
            nameLength = struct.unpack_from('<H', data, offset)[0] * 2
            offset += 2

            if nameLength == 0:
                print("Reached the end of the entries.")
                break

            name = data[offset:offset + nameLength].decode('utf-16le')
            offset += nameLength

            offset += 6  # Skip unnecessary data

            entryOffset = struct.unpack_from('<I', data, offset)[0]
            offset += 4

            entrySize = struct.unpack_from('<I', data, offset)[0]
            offset += 4

            offset += 4  # Skip unnecessary data

            unpackedSize = struct.unpack_from('<I', data, offset)[0]
            offset += 4

            isPacked = unpackedSize != 0

            headerLength = struct.unpack_from('<B', data, offset)[0]
            offset += 1

            header = None
            if headerLength > 0:
                header = data[offset:offset + headerLength]
                offset += headerLength

            entry = GPKEntry(name, entryOffset, entrySize, unpackedSize, isPacked, header)
            print(f"Parsed entry: {name}, offset: {entryOffset}, size: {entrySize}, unpacked size: {unpackedSize}")
            self.entries.append(entry)

    def unpackEntries(self):
        outputSubdir = os.path.join(self.outputDir, Path(self.filePath).stem)
        os.makedirs(outputSubdir, exist_ok=True)
        print(f"Starting to unpack {len(self.entries)} entries to {outputSubdir}...")

        with open(self.filePath, 'rb') as f:
            for entry in self.entries:
                print(f"Unpacking entry: {entry.name}")
                f.seek(entry.offset)
                data = f.read(entry.size)

                if entry.header:
                    print(f"Applying header of {len(entry.header)} bytes to the entry data.")
                    data = entry.header + data

                if entry.isPacked:
                    print("Entry is packed. Decompressing...")
                    data = zlib.decompress(data)

                outputPath = os.path.join(outputSubdir, entry.name)
                outputDir = os.path.dirname(outputPath)
                os.makedirs(outputDir, exist_ok=True)

                with open(outputPath, 'wb') as outFile:
                    outFile.write(data)

                print(f"Entry {entry.name} unpacked successfully.")

        print(f"All entries unpacked successfully to {outputSubdir}.")

def unpackGPK(gpkFile, outputDirectory):
    opener = GPKOpener(gpkFile, outputDirectory)
    if opener.tryOpen():
        opener.unpackEntries()
        print(f"Unpacking completed successfully to {outputDirectory}.")
    else:
        print(f"Failed to unpack {gpkFile}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unpack GPK files.")
    parser.add_argument("gpkFile", help="Path to the GPK file to be unpacked.")
    parser.add_argument("outputDirectory", help="Directory where the unpacked files will be saved.")

    args = parser.parse_args()

    unpackGPK(args.gpkFile, args.outputDirectory)
