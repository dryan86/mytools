#!/usr/bin/env python

import struct
import sys
import zlib
import os
import os.path

XOR_KEY = 0x79

class CompressionBlock(object):
    def __init__(self, pak):
        self.CompressedStart = pak.read_uint64()
        self.CompressedEnd = pak.read_uint64()

class FileEntry(object):
    def __init__(self, pak):
        self.pak = pak
        self.Path = pak.read_string()
        self.Pos = pak.read_uint64()
        self.Size = pak.read_uint64()
        self.UncompressedSize = pak.read_uint64()
        self.CompressionMethod = pak.read_uint32()

        if pak.Version < 2:
            self.Timestamp = pak.read_uint64()

        self.Hash = pak.read_bytes(20)

        if pak.Version >= 3:
            if self.CompressionMethod != 0:
                size = pak.read_uint32()
                self.CompressionBlocks = []
                for i in xrange(0, size):
                    self.CompressionBlocks.append(CompressionBlock(pak))
            self.bEncrypted = pak.read_uint8()
            self.CompressionBlockSize = pak.read_uint32()

        else:
            self.bEncrypted = False

    def decrypt(self, data):
        # FIXME Optimization
        plain = ""
        for b in data:
            plain += chr(ord(b) ^ XOR_KEY)
        return plain

    def extract(self, out):
        fh = self.pak.fh

        if self.CompressionMethod != 0:
            if self.CompressionMethod != 1:
                raise RuntimeError('zlib support only')

            for block in self.CompressionBlocks:
                fh.seek(block.CompressedStart)
                data = fh.read(block.CompressedEnd - block.CompressedStart)
                if self.bEncrypted:
                    data = self.decrypt(data)
                out.write(zlib.decompress(data, 0, self.CompressionBlockSize))

        elif self.bEncrypted:
            fh.seek(self.Pos)
            size = self.Size
            while size > 0:
                chunk = 4096 if size > 4096 else size
                out.write(self.decrypt(fh.read(chunk)))
                size -= chunk

        else:
            fh.seek(self.Pos)
            size = self.Size
            while size > 0:
                chunk = 4096 if size > 4096 else size
                out.write(fh.read(chunk))
                size -= chunk

class PakFile(object):
    def __init__(self, path):
        self.path = path
        self.fh = None

    def init(self):
        self.fh = open(self.path, 'rb')

        self.fh.seek(-45, 2)
        buffer = self.fh.read(45)
        (self.bEncryptedIndex, self.Magic, self.Version,
            self.IndexOffset, self.IndexSize, self.IndexHash) = struct.unpack('<BLLQQ20s', buffer)

        self.fh.seek(self.IndexOffset)
        self.MountPoint = self.read_string()
        self.FileCount = self.read_uint32()

        self.Files = []
        for i in xrange(0, self.FileCount):
            file = FileEntry(self)
            self.Files.append(file)

    def read_uint8(self):
        return ord(self.fh.read(1))

    def read_uint32(self):
        return struct.unpack('<L', self.fh.read(4))[0]

    def read_int32(self):
        return struct.unpack('<l', self.fh.read(4))[0]

    def read_uint64(self):
        return struct.unpack('<Q', self.fh.read(8))[0]

    def read_string(self):
        size = self.read_int32()
        if size < 0:
            # UTF-16
            return self.fh.read((-size) * 2).decode("utf-16").rstrip('\0')
        else:
            return self.fh.read(size).rstrip('\0')

    def read_bytes(self, count):
        return self.fh.read(count)

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, type, value, traceback):
        if self.fh:
            self.fh.close()

def main(argv):
    if len(argv) < 2:
        sys.stderr.write('Syntax: %s file.pak\n' % argv[0])
        return 1

    pak_path = argv[1]
    outdir = "out"
    outdir_abs = os.path.abspath(outdir)
    with PakFile(pak_path) as pak:
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        for file in pak.Files:
            path = os.path.join(outdir, file.Path.replace('/', os.sep))
            path_abs = os.path.abspath(path)
            if not path_abs.startswith(outdir_abs):
                sys.stderr.write('Warning: not extracting "%s" because of suspicious path\n'
                    % file.Path.encode('utf-8'))
                continue

            print file.Path.encode('utf-8')

            parent = os.path.dirname(path)
            if not os.path.exists(parent):
                os.makedirs(parent)

            with open(path, 'wb') as out:
                file.extract(out)

if __name__ == "__main__":
    sys.exit(main(sys.argv))