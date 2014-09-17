#!/usr/bin/env python

import sys

def readFile(paramFile):
    file = open(paramFile, 'r')
    arrayOfByte = file.read()
    return readString(arrayOfByte)

def readString(arrayOfByte):
    i = 0
    byteArray = []
    while (i < len(arrayOfByte)):
      if (len(arrayOfByte) > i + 1):
        j = ((int('0xFF',16) & ord(arrayOfByte[(i + 1)])) >> 5 | (int('0xFF',16) & ord(arrayOfByte[(i + 1)])) << 3)
        byteArray.append(j)
        byteArray.append(((int('0xFF',16) & ord(arrayOfByte[i])) >> 5 | (int('0xFF',16) & ord(arrayOfByte[i])) << 3))
      else:
        byteArray.append(((int('0xFF',16) & ord(arrayOfByte[i])) >> 5 | (int('0xFF',16) & ord(arrayOfByte[i])) << 3))
      i += 2;
    return ''.join([ chr(x & 0xFF) for x in byteArray])

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        for file in sys.argv[1:]:
            print readFile(file)
    else:
        print readFile("manifest.yves")
