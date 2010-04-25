#!/usr/bin/python

import sys
import os
from pyechonest import *
import wave
import glob
import pycodegen
import subprocess
import tempfile
import struct
import json
import fp
import echonest

supported_types = [".mp3", ".ogg", ".flac"]

def main(dir):
	for f in os.listdir(dir):
		print "file",f
		query = fp.fingerprint(os.path.join(dir, f))
		echonest.pp(echonest.fp_lookup(query))

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >>sys.stderr, "usage: %s <dir>" % sys.argv[0]
		sys.exit(1)
	else:
		main(sys.argv[1])
