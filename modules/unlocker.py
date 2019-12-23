import random
import os
import string
import pickle

def run(filename, drive, output, verbosity):
	cwd = os.getcwd() # store this for later while we read the manifest file

	try:
		lockedFile = open(filename, "rb")
	except FileNotFoundError:
		return "FileNotFoundError - missingfile"
	data = pickle.load(lockedFile)
	lockedFile.close()

	bytesRead = data[1]
	fileIndentifier = data[0]

	lockedBytes = []

	for b in bytesRead:
		lockedBytes.append(b)

	try:
		os.chdir(drive + ":\\deadbolt\\" )
	except FileNotFoundError:
		return "FileNotFoundError - nodirectory"

	try:
		manifestFile = open("manifest.txt", "rb")
	except FileNotFoundError:
		return "FileNotFoundError - nomanifest"

	manifestData = pickle.load(manifestFile)
	manifestFile.close()

	if verbosity == 1:
		print("read manifest")

	filenameNoEx = (os.path.splitext(filename))[0] # Get the filename path

	keyFileName = manifestData[fileIndentifier][2]
	try:
		keyFile = open(keyFileName+".dkey", "rb")
	except FileNotFoundError:
		return "FileNotFoundError - nokeyfile"
	bytesKey = pickle.load(keyFile)
	keyFile.close()

	if verbosity == 1:
		print("read key file")

	os.chdir(cwd) # go back to original directory

	"""
	try:
		with open(filename, "rb") as f:
			    bytesRead = f.read()
			    for b in bytesRead:
			    	lockedBytes.append(b)
	except FileNotFoundError:
		return "FileNotFoundError - missingfile"
	"""


	if verbosity == 1:
		print("read locked bytes")

	unlockedBytes = []
	for key in bytesKey:
		unlockedBytes.append(lockedBytes[bytesKey[key]]) # by iterating through bytesKey in order, the order of the original data is preserved. 

	if verbosity == 1:
		print("decoded locked file")

	unlockedBytesToWrite = bytes(unlockedBytes)
	newFile = open(manifestData[fileIndentifier][0] + "_deadbolt" + manifestData[fileIndentifier][1], "wb")
	newFile.write(unlockedBytesToWrite)
	newFile.close()

	if verbosity == 1:
		print("wrote unlocked file")

	return "OK"