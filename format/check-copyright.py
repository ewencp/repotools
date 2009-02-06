#!/usr/bin/python
#  Sirikata Repository Utilities - Check Copyrights
#  check-copyright.py
#
#  Copyright (c) 2009, Ewen Cheslack-Postava
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of Sirikata nor the names of its contributors may
#    be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# check-copyright.py [path]
# This is a utility for checking for copyright notices and licenses in
# header comments of source code files. We require a copyright notice
# and license to appear at the top of every file. We try to autodetect the
# type of comments for the file and check the top of the file for 3 items
#  1) Name of the file
#  2) Copyright notice, e.g. Copyright (c) 2009, Ewen Cheslack-Postava
#  3) The license, currently always the BSD license
# Any missing items will be printed as a report to stdout
#
# Parameters:
#  path - the root directory to search; defaults to the current directory

import os
import re
import sys
import getopt

# Try to automatically detect the type of comments in the file based
# on one of the lines
def get_comment_type(type, line):
    comment_types = [ ('#', '#'),
                      ('/*', '*'),
                      ('//', '//') ]
    if type != None: return type
    bare_line = line.lstrip()
    for (first, subsequent) in comment_types:
        if bare_line.find(first) == 0:
            type = subsequent

    return type

# Based on a given comment type, decide whether this is a comment line or not
def is_comment_line(type, line):
    if type == None: return False
    bare_line = line.lstrip()
    if bare_line.find(type) == 0:
        return True
    return False

# Check one file for copyright information, including filename in comment
def check_file_copyright(path):
    filename = os.path.basename(path)
    file = open(path, 'r')
    found_filename = False
    found_copyright_note = False
    found_license_text = False
    comment_type = None
    for line in file:
        comment_type = get_comment_type(comment_type, line)
        if not is_comment_line(comment_type, line): continue
        if re.search(filename, line):
            found_filename = True
        if re.search('Copyright', line):
            found_copyright_note = True
        if re.search('Redistribution and use in source and binary forms,'.lower(), line.lower()):
            found_license_text = True
    file.close()
    if not found_filename:
        print path, ": Missing filename in header comment."
    if not found_copyright_note:
        print path, ": Missing copyright note in header comment."
    if not found_license_text:
        print path, ": Missing license text in header comment."



# regexps for directories to ignore
dir_ignores = [
    '[.].*',
    'CMakeFiles'
    ]

# regexps for files to ignore
file_ignores = [
    '[.].*',
    'Makefile',
    'AUTHORS',
    'LICENSE',
    'Doxyfile',
    '.*[.]sln',
    '.*[.]suo',
    '.*[.]vcproj',
    '.*[.]ncb',
    'cmake_install[.]cmake',
    'CMakeCache[.]txt',
    '.*[.]pb[.]h',
    '.*[.]pb[.]cc',
    '.*[.]o',
    '.*[.]so',
    '.*[.]a'
    ]

def usage():
    print "Usage: check-copyright.py [--ignore-dir regexp] [--ignore-file regexp] [root-path]"

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:f:", ["help", "ignore-dir=", "ignore-file="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    search_dir = '.'
    if len(args) == 1:
        search_dir = args[0]
    elif len(args) > 1:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--ignore-dir"):
            dir_ignores.append(arg)
        elif opt in ("-f", "--ignore-file"):
            file_ignores.append(arg)

    for root, dirs, files in os.walk(search_dir):
        for name in files:
            ignored = False
            for ignore in file_ignores:
                if re.match(ignore, name): ignored = True
            if not ignored: check_file_copyright(os.path.join(root, name))
        # get rid of ignore directories
        for ignore in dir_ignores:
            for d in dirs:
                if re.match(ignore, d): dirs.remove(d)


if __name__ == "__main__":
    main(sys.argv[1:])
