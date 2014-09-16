#!/usr/bin/env python
# vim:fileencoding=utf-8
from calibre.ptempfile import PersistentTemporaryDirectory
import os, json, StringIO

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
    version = (0, 0, 1)
    on_import = True

    def openFile(path, mode='r'):
        if os.path.exists(path):
            file = open(path, mode)
        else:
            file = StringIO.StringIO(readFile(re.sub("html","yves",path)))
        return file

    def run(self, yvesfile):
        yves_temp_directory = PersistentTemporaryDirectory('yves_input')
        log.debug('Convert yves ' + yvesfile + ' to html')
        manifestJson = readFile(yvesfile)

        yvesDir = os.path.dirname(yvesfile)

        bibleMetaData = json.loads(manifestJson)
        bibleName = bibleMetaData['local_abbreviation'] + ".html"

        log.debug(manifestJson)

        DEST = open(os.path.join(yves_temp_directory, bibleName), 'w')
        DEST.write( '<html><head><title>' )
        DEST.write( bibleMetaData['title'].encode('utf8') )
        DEST.write( '</title>\n')
        DEST.write( '<style type="text/css">' )
        DEST.write( '</style>' )
        DEST.write( '</head><body>\n' )
        for book in bibleMetaData['books']:
            DEST.write('<div class="book">\n<div class="bookTitle">')
            DEST.write(book['abbreviation'].encode('utf8'))
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
                chapterLines = self.openFile( os.path.join(yvesDir,book['usfm'],chapterFile + ".html")).readlines()
                DEST.writelines( chapterLines[2:len(chapterLines)-2] )
            DEST.write('</div>\n')
        DEST.write( '</body></html>\n' )

        return HTML2ZIP.run(self, os.path.join( yves_temp_directory, bibleName ))

