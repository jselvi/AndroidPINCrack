AndroidPINCrack is a Python script that bruteforce the Android Passcode given the hash and salt.
Of course there are some other faster ways to crack than a python script, but it can be useful for numeric passcoders or wordlist attack.

**WARNING! (year 2020): This script has been not tested in the last 5 years or more, so it may not work in modern Android devices.**

```
$ ./AndroidPINCrack.py 
Usage: AndroidPINCrack.py [options]

Options:
  -h, --help                                   show this help message and exit
  -H HASH, --hash=HASH                         password.key hash
  -s SALT, --salt=SALT                         Hash salt
  -m MODEL, --model=MODEL                      Android Version/Model
  -c CHARSET, --charset=CHARSET                Password charset to test (default=numeric)
  -l LENGTH, --length=LENGTH                   Passcode max length (default=4)
  -w WORDLIST_FILE, --wordlist=WORDLIST_FILE   wordlist file
```

By default, it bruteforces numeric 4-length passwords:

```
$ ./AndroidPINCrack.py -H DC6831BFE0B8563B82A8AAB9CB5B294BD4B3072A93AF306 -s 7026104367013576733
Found! Passcode = 0101
```

It seems that Samsung has modified the hashing algorithm, so you need to use the proper flag:

```
$ ./AndroidPINCrack.py -H DC59AACF2AFCE72E737190323022FFB6E2831446 -s 988796901418269782 -m samsung
Found! Passcode = 1234
```

You can use some other flags, such as a wordlist instead of bruteforcing:

```
$ ./AndroidPINCrack.py -H DC59AACF2AFCE72E737190323022FFB6E2831446 -s 988796901418269782 -m samsung -w wordlist.txt
Found! Passcode = 1234
```
