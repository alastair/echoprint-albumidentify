#!/usr/bin/python

import os
import subprocess
import wave
import tempfile
import pycodegen
import struct
import json
import sys

supported_types = [".mp3", ".ogg", ".flac"]


def decode(file):
	if os.path.splitext(file)[1] in supported_types:
		(fd,outfile)=tempfile.mkstemp(suffix=".wav")
		os.close(fd)
		args = ["ffmpeg", "-y", "-i", file, "-ac", "1", "-ar", "22050", "-f", "wav", "-t", "20", "-ss", "10", outfile]
		print "decoding",file,"..."
		subprocess.call(args, stderr=open("/dev/null", "w"))
		return outfile
	else:
		return None

def fingerprint(file):
	outfile = ""
	MAGIC = 32768.0
	try:
		outfile = decode(file)
		if outfile is not None:
			wav = wave.open(outfile, "rb")
			print "num frames:",wav.getnframes()

			frames = wav.readframes(wav.getnframes())
			fs = []
			for i in range(0, len(frames), 2):
				fs.append(struct.unpack("<H", frames[i:i+2])[0]/MAGIC)
			
			print "num samples", len(fs)
			cg = pycodegen.pycodegen(fs, 10)
			codes = cg.getCodes()
			print "num codes", len(codes)
			codestr = " ".join([str(x) for x in codes])
			query = json.dumps({"codes": codestr})
			return query

	finally:
		if outfile is not None and os.path.exists(outfile):
			print "unlinking file"
			os.unlink(outfile)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >>sys.stderr, "usage: %s <file>" % sys.argv[0]
		sys.exit(1)
	else:
		print json.dumps(fingerprint(sys.argv[1]))
