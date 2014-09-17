#!/usr/bin/env python
# vim:fileencoding=utf-8
from calibre.ptempfile import PersistentTemporaryDirectory
import os, json

__license__ = 'GPL v3'
__copyright__ = '2014, Randall Mason <Randall@Mason.CH>'


from calibre.ebooks.html.to_zip import HTML2ZIP
from calibre_plugins.yves_input.yvesDecode import readFile

class YVES2ZIP(HTML2ZIP):

    name = 'YVES to ZIP'
    author = 'Randall Mason'
    description = _('Convert YVES files to HTMLZ')
    supported_platforms = ['linux','osx','windows']
    file_types = set(['yves'])
    minimum_calibre_version = (2, 3, 0)
    version = (0, 0, 3)
    on_import = True

    def run(self, yvesfile):
        yves_temp_directory = PersistentTemporaryDirectory('yves_input')

        manifestJson = readFile(yvesfile)
        # for iOS bibles, everything is stored in a plist, eventually use something like this:
        # xmltodict.parse(plistDecode.plistFromString(base64.decodestring(xmltodict.parse(plistDecode.plistFromFile('tv.lifechurch.bible.plist','xml1'))['plist']['dict']['dict'][0]['data'][0]),'xml1'))

        yvesDir = os.path.dirname(yvesfile)

        bibleMetaData = json.loads(manifestJson)
        bibleName = bibleMetaData['abbreviation'] + ".html"

        DEST = open(os.path.join(yves_temp_directory, bibleName), 'w')
        DEST.write( '<html><head><title>' )
        DEST.write( bibleMetaData['local_title'].encode('utf8') )
        DEST.write( '</title>\n')
        if( bibleMetaData.has_key('publisher') & bibleMetaData['publisher'].has_key('name') ):
            DEST.write( '<meta name="Publisher" content="' + bibleMetaData['publisher']['name'].encode('utf8') + '">\n')
        if( bibleMetaData.has_key('copyright_long') & bibleMetaData['copyright_long'].has_key('text') ):
            DEST.write( '<meta name="Copyright" content="' + bibleMetaData['copyright_long']['text'].encode('utf8') + '">\n')
        if( bibleMetaData.has_key('language') & bibleMetaData['language'].has_key('iso_639_1') ):
            DEST.write( '<meta name="DC.language" content="' + bibleMetaData['language']['iso_639_1'].encode('utf8') + '">\n')
        elif( bibleMetaData.has_key('language') & bibleMetaData['language'].has_key('iso_639_3') ):
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

        return HTML2ZIP.run(self, os.path.join( yves_temp_directory, bibleName ))

