#!/usr/bin/env python

import sys, os, json

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

def loadJson(string):
    return json.loads(string)

def yvesDir2HTML(yvesfile, yves_temp_directory):
        # for iOS bibles, everything is stored in a plist, eventually use something like this:
        # xmltodict.parse(plistDecode.plistFromString(base64.decodestring(xmltodict.parse(plistDecode.plistFromFile('tv.lifechurch.bible.plist','xml1'))['plist']['dict']['dict'][0]['data'][0]),'xml1'))
        bibleMetaData = loadJson(readFile(yvesfile))

        yvesDir = os.path.dirname(yvesfile)

        bibleName = bibleMetaData['abbreviation'] + ".html"

        DEST = open(os.path.join(yves_temp_directory, bibleName), 'w')
        DEST.write( '<html dir="' + bibleMetaData['language']['text_direction'].encode('utf8') + '"><head><title>' )
        DEST.write( bibleMetaData['local_title'].encode('utf8') )
        DEST.write( '</title>\n')
        if( bibleMetaData.has_key('publisher') and bibleMetaData['publisher'] and bibleMetaData['publisher'].has_key('name') and bibleMetaData['publisher']['name'] ):
            DEST.write( '<meta name="Publisher" content="' + bibleMetaData['publisher']['name'].encode('utf8') + '">\n')
        if( bibleMetaData.has_key('copyright_long') and bibleMetaData['copyright_long'].has_key('text') and bibleMetaData['copyright_long']['text'] ):
            DEST.write( '<meta name="Copyright" content="' + bibleMetaData['copyright_long']['text'].encode('utf8') + '">\n')
        if( bibleMetaData.has_key('language') and bibleMetaData['language'].has_key('iso_639_1') and bibleMetaData['language']['iso_639_1'] ):
            DEST.write( '<meta name="DC.language" content="' + bibleMetaData['language']['iso_639_1'].encode('utf8') + '">\n')
        elif( bibleMetaData.has_key('language') and bibleMetaData['language'].has_key('iso_639_3') and bibleMetaData['language']['iso_639_3'] ):
            DEST.write( '<meta name="DC.language" content="' + bibleMetaData['language']['iso_639_3'].encode('utf8') + '">\n')
        DEST.write( '<meta name="Source" content="YouVersion">\n')
        DEST.write( '<style type="text/css">' )
        DEST.write( '</style>' )
        DEST.write( '</head><body>\n' )
        for book in bibleMetaData['books']:
            DEST.write('<div class="book">\n<div class="bookTitle">')
            DEST.write(book['human_long'].encode('utf8'))
            DEST.write('</div>\n')
            for chapter in book['chapters']:
                chapterFile = chapter['usfm'][len(book['usfm'])+1:]
                # DEST.write('<a href="')
                # DEST.write(book['usfm'])
                # DEST.write("/")
                # DEST.write(chapterFile)
                # DEST.write('.html">')
                # DEST.write(book['abbreviation'].encode('utf8'))
                # DEST.write(' ')
                # DEST.write(chapter['human'])
                # DEST.write('</a>')
                # DEST.write('\n<br />\n')
                chapterLines = readFile( os.path.join(yvesDir,book['usfm'],chapterFile + ".yves")).splitlines()
                DEST.writelines( chapterLines[2:len(chapterLines)-2] )
            DEST.write('</div>\n')
        DEST.write( '</body></html>\n' )

        return bibleName

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        for file in sys.argv[1:]:
            print loadJson(readFile(file))
    else:
        print yvesDir2HTML("manifest.yves",".")
