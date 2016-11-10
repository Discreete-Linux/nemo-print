#!/usr/bin/env python
# Print Plugin for Nemo
##
# Encoding: UTF-8
""" A nemo extension which allows printing of files """
import gettext
from gi.repository import GObject, Nemo
import os
import subprocess
import magic
import sys

class NautilusPrintExtension(GObject.GObject, Nemo.MenuProvider):
    """ Allows printing of many file types """
    def __init__(self):
        """ Init the extionsion. """
        print "Initializing nemo-print extension"
        self.oootypes = [ "application/vnd.oasis.opendocument.database", \
"application/vnd.oasis.opendocument.formula-template", \
"application/vnd.oasis.opendocument.formula", \
"application/vnd.oasis.opendocument.spreadsheet", \
"application/vnd.oasis.opendocument.spreadsheet-template", \
"application/vnd.oasis.opendocument.presentation-template", \
"application/vnd.oasis.opendocument.text-template", \
"application/vnd.oasis.opendocument.graphics-template", \
"application/vnd.oasis.opendocument.text", \
"application/vnd.oasis.opendocument.graphics", \
"application/vnd.oasis.opendocument.text-master", \
"application/vnd.oasis.opendocument.presentation", \
"application/vnd.oasis.opendocument.chart", \
"application/vnd.oasis.opendocument.chart-template", \
"application/rtf", "application/msword", \
"application/vnd.ms-excel", "application/csv", \
"application/excel", "application/msexcel", \
"application/tab-separated-values", "application/vnd.ms-word", \
"application/vnd.sun.xml.*", "application/vnd.stardivision.*", \
"application/vnd.wordperfect", "application/wordperfect", \
"application/x-excel", "application/xls", "application/x-ms-excel", \
"application/x-msexcel", "application/x-xls", "text/csv", \
"text/comma-separated-values", "text/rtf", "text/spreadsheet", \
"text/tab-separated-values", "text/x-comma-separated-values" ]

        self.plaintypes = [ "text/plain", "application/pdf", \
"application/postscript", "image/tiff", "image/bmp", "image/x-bmp", \
"image/gif", "image/jpeg", "image/png", "image/x-png", \
"image/x-pixmap", "image/x-portable-pixmap" ]
        self.cookie = magic.open(magic.MAGIC_MIME)
        self.cookie.load()

    def menu_activate_cb(self, menu, myfiles):
        """ Print file(s) """
        ooofiles = []
        lprfiles = []
        for myfile in myfiles:
            filename = myfile.get_location().get_path()
            ftype = self.cookie.file(filename)
            print ftype
            if ftype.split(';')[0] in self.oootypes:
                ooofiles.append(filename)
            elif ftype.split(';')[0] in self.plaintypes:
                lprfiles.append(filename)

        if len(ooofiles) > 0:
            args = [ "soffice", "-p" ]
            args.extend(ooofiles)
            print args
            subprocess.Popen(args)
        if len(lprfiles) > 0:
            for filename in lprfiles:
                subprocess.Popen(["lpr", filename])

    def validFiles(self, files):
        """ Check if files are valid for us """
        for myfile in files:
            if not ( ( myfile.get_uri_scheme() == 'file' ) or \
                ( myfile.get_uri_scheme() == 'smb' ) ):
                return False
            elif ( not myfile.get_mime_type() in self.oootypes ) and \
                ( not myfile.get_mime_type() in self.plaintypes ):
                return False
        return True

    def get_file_items(self, window, files):
        """ Tell nemo whether and when to show the menu """
        if len(files) == 0:
            return
        myfile = files[0]
        if not self.validFiles(files):
            return
        item = Nemo.MenuItem(name='Nemo::nemo_print',
                                 label=gettext.dgettext('nemo-print', 'Print').decode('utf-8'),
                                 tip=gettext.dgettext('nemo-print', 'Print the file(s) on the default printer').decode('utf-8'),
                                 icon="printer")
        item.connect('activate', self.menu_activate_cb, files)
        return item,
