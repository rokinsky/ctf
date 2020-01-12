import Crypto.Cipher.AES as AES
from os import getrandom, listdir
import sys

DEBUG = False

key = getrandom(16)

def enc(msg):
    if DEBUG:
        sys.stderr.write('ENC ' + repr(msg) + '\n')
    # I've heard that standard cryptographic padding schemes enable padding
    # oracle attacks — it's much more secure to just pad with spaces.
    while len(msg) % 16 != 0:
        msg += b' '
    iv = getrandom(16)
    cipher = AES.new(mode=AES.MODE_CBC, key=key, iv=iv)
    return iv + cipher.encrypt(msg)

def dec(msg):
    iv = msg[:16]
    msg = msg[16:]
    cipher = AES.new(mode=AES.MODE_CBC, key=key, iv=iv)
    return cipher.decrypt(msg)

print("Welcome to the encrypted shell!")
while True:
    print("Enter encrypted command.")
    # Get a line.
    try:
        d = input()
    except EOFError:
        break
    try:
        # Decode it.
        d = bytes.fromhex(d.strip())

        # Decrypt it.
        d = dec(d)

        # Leave the message as bytes — Unicode is annoying and just leads to trouble.
        if DEBUG:
            sys.stderr.write('DEC ' + repr(d) + '\n')

        # Strip comments.
        if b'#' in d:
            pos = d.index(b'#')
            d = d[:pos]

        # Split by spaces.
        words = []
        word = b''
        for x in d:
            if x == ord(' '):
                if word:
                    words.append(word)
                    word = b''
            else:
                word += bytes([x])
        if word:
            words.append(word)

        if not words:
            # Empty command?
            continue

        if words[0] == b'ls':
            for x in listdir('.'):
                print(enc(x.encode()).hex())
        elif words[0] == b'cat':
            for f in words[1:]:
                if b'/' in f or b'\0' in f:
                    print(enc(f + b': invalid filename').hex())
                else:
                    try:
                        with open(f) as f:
                            for l in f:
                                print(enc(l.encode()).hex())
                    except OSError:
                        print(enc(f + b': no such file or directory').hex())
        else:
            print(enc(words[0] + b': unknown command').hex())
    except Exception as e:
        print(enc(f'Exception occured: {e}'.encode()).hex())

