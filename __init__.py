#!/usr/bin/env python
# vim:fileencoding=utf-8
from calibre.ptempfile import PersistentTemporaryDirectory

__license__ = 'GPL v3'
__copyright__ = '2019, Randall Mason <Randall@Mason.CH>'

import os

from calibre.customize import FileTypePlugin
from calibre_plugins.yves_input.yvesDecode import yvesDir2HTML

class YVES2ZIP(FileTypePlugin):

    name = 'YVES to ZIP'
    author = 'Randall Mason'
    description = _('Convert YVES files to HTMLZ')
    supported_platforms = ['linux','osx','windows']
    file_types = set(['yves'])
    minimum_calibre_version = (1, 25, 0)
    version = (0, 0, 8)
    on_import = True

    def run(self, yvesfile):
        from calibre.ebooks.html.to_zip import HTML2ZIP
        html2zip = HTML2ZIP(None)
        yves_temp_directory = PersistentTemporaryDirectory('yves_input')
        bibleName = yvesDir2HTML(yvesfile,yves_temp_directory)

        return html2zip.run(os.path.join( yves_temp_directory, bibleName ))
