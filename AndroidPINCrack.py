#!/usr/bin/python3
# Android Hash Cracker
# Jose Selvi - jselvi[a.t]pentester[d0.t]es - http://www.pentester.es
# Version 0.2 - 05/May/2013
# 	- Fixed problems in hex() at Python 2.6 (thanks @ldelgadoj)
# Version 0.3 - 04/Aug/2020
# 	- Ported to Python3 (only changes in "print" were needed)

# Libraries
from optparse import OptionParser
from itertools import product
import hashlib
from binascii import hexlify

# Charsets
CHARSET_NUMERIC = "0123456789"
CHARSET_ALPHA = "abcdefghijklmnopqrstuvwxyz."
CHARSET_ALPHANUMERIC = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHARSET_FULL = """ !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

# Android Default Hashing Algorithm
def hashDefault(passcode,salt):
	salted_passcode = passcode + salt
	guess_digest = hashlib.sha1(salted_passcode).digest()
	guess_hash = hexlify( guess_digest ).upper()
	return guess_hash

# Special Samsung Hashung Algorithm
def hashSamsung(passcode,salt):
	salted_passcode = passcode + salt
	buf=str()
	for i in range(1024):
		step_string = str(buf) + str(i) + salted_passcode
		buf = hashlib.sha1( step_string ).digest()
	return hexlify(buf).upper()

# Generate Hash
def generateHash(passcode,salt,model):
	if model == "SAMSUNG":
		return hashSamsung(passcode,salt)
	else:
		return hashDefault(passcode,salt)

###
### Main
###

# Get Parameters
usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-H", "--hash", type="string", dest="hash", help="password.key hash")
parser.add_option("-s", "--salt", type="int", dest="salt", help="Hash salt")
parser.add_option("-m", "--model", type="choice", dest="model", choices=['default','samsung'], default="default", help="Android Version/Model")
parser.add_option("-c", "--charset", type="choice", dest="charset", choices=['numeric','alpha', 'alphanumeric','full'], default="numeric", help="Password charset to test (default=numeric)")
parser.add_option("-l", "--length", type="int", dest="length", default=4, help="Passcode max length (default=4)")
parser.add_option("-w", "--wordlist", type="string", dest="wordlist_file", help="wordlist file")
(options, args) = parser.parse_args()
if not options.hash or not options.salt:
        parser.print_help()
        exit()

# Check lenght
if options.length < 4:
	print("Error! Min passcode len in Android is 4!")
	exit()
if options.length > 16:
	print("Error! Max passcode len in Android is 16!")
	exit()
if options.length > 6:
	print("Maybe you should use a faster tool such as Hashcat... but let's move on!")

# Split hashes
HASH_SHA1 = options.hash.upper()[:40]
HASH_MD5 = options.hash.upper()[41:]

# From Numeric Salt to Hex (len should be 8?)
#SALT = hex(options.salt).lstrip('0x').rstrip('L').zfill(8)
SALT = hex(options.salt).lstrip('0x').rstrip('L')

# Get Charset
if options.charset == 'numeric':
	CHARSET = CHARSET_NUMERIC
elif options.charset == 'alpha':
	CHARSET = CHARSET_ALPHA
elif options.charset == 'alphanumeric':
	CHARSET = CHARSET_ALPHANUMERIC
elif options.charset == 'full':
	CHARSET = CHARSET_FULL
else:
	CHARSET = CHARSET_NUMERIC

# Get Model
MODEL = options.model.upper()

try:
	# Generate Passcodes
	if not options.wordlist_file:
		for l in range(3, options.length):
			for passcode in product(CHARSET, repeat=l+1):
				passcode = "".join([x for x in passcode])
				# GenerateHash
				GUESS_HASH = generateHash( passcode, SALT, MODEL )
				# CompareHash
				if GUESS_HASH == HASH_SHA1:
					print("Found! Passcode = " +  passcode)
					exit()
	# Or using wordlist
	else:
		for passcode in open(options.wordlist_file):
			passcode = passcode.rstrip()
			# GenerateHash
			GUESS_HASH = generateHash( passcode, SALT, MODEL )
			# CompareHash
			if GUESS_HASH == HASH_SHA1:
				print("Found! Passcode = " +  passcode)
				exit()

	# Not found...
	print("Bad luck... Is that your specific model?")
	exit()

except KeyboardInterrupt:
	exit()
