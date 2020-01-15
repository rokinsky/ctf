import Crypto.Cipher.AES as AES
from os import urandom, listdir
import sys

DEBUG = True

key = b'\xc9ko\xdf\xa2~\xe0\xf2\x19\x88\x98D\xb4\x98\x1c\xa1'#urandom(16)#b'Q\x96\x00\xf7\xb5\xb8\xc0n\xd7\xfaz\xdd\x957&Y'#

if DEBUG:
    sys.stderr.write('\n\n\n\n\n' + 'KEY ' + repr(key) + '\n')

def enc(msg):

    # I've heard that standard cryptographic padding schemes enable padding
    # oracle attacks — it's much more secure to just pad with spaces.
    while len(msg) % 16 != 0:
        msg += b' '

    if DEBUG:
        sys.stderr.write('ENC ' + repr(msg) + '\n')

    iv = urandom(16)
    cipher = AES.new(mode=AES.MODE_CBC, key=key, iv=iv)
    return iv + cipher.encrypt(msg)

def dec(msg):
    iv = msg[:16]
    msg = msg[16:]
    cipher = AES.new(mode=AES.MODE_CBC, key=key, iv=iv)
    return cipher.decrypt(msg)

print("Welcome to the encrypted shell!")
i = 0

while True:
    #sys.stderr.write("Enter encrypted command." + '\n') 
    print("Enter encrypted command.")
    # Get a line.
    try:
        d = input()
    except EOFError:
        break
    try:
        # Decode it.
        d = bytes.fromhex(d.strip())
        #sys.stderr.write(f'MSG {d}' + '\n')

        # Decrypt it.
        d = dec(d)

        # Leave the message as bytes — Unicode is annoying and just leads to trouble.
        #if DEBUG:
            #sys.stderr.write('DEC ' + repr(d) + '\n')

        # Strip comments.
        if b'#' in d:
            #i = 0
        #    sys.stderr.write('#=' + repr(i) + ' ' + repr(d) + '\n')
            pos = d.index(b'#')
            d = d[:pos]

        # if b' ' in d[:1]:
        #     sys.stderr.write('S=' + repr(i) + ' ' + repr(d) + '\n')

        #if b'g}\n' in d[17:]:
        #    sys.stderr.write('F=' + repr(i) + ' ' + repr(d) + '\n')

        i = (i + 1) % 255
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

            #if DEBUG:
            #    sys.stderr.write('WORD ' + repr(word) + '\n')
        if word:
            words.append(word)
        #words = filter(lambda x: x != b'', d.split(b' '))

        #sys.stderr.write(repr(words[0]) + " " + repr(words[1]) + '\n')

        if not words:
            # Empty command?
            #print('GOOD')
            #sys.stderr.write('EMPTY' + '\n')
            continue

        if words[0] == b'ls':
            sys.stderr.write('LS' + '\n')
            for x in listdir('.'):
                print(enc(x.encode()).hex())
        elif words[0] == b'cat':
            sys.stderr.write('CAT ' + repr(d) + '\n')
            for f in words[1:]:
                if b'/' in f or b'\0' in f:
                    print(enc(f + b': invalid filename').hex())
                else:
                    try:
                        with open(f) as f:
                            for l in f:
                                e = enc(l.encode())
                                sys.stderr.write('FLAG ' + repr(e) + '\n')
                                print(e.hex())
                    except OSError:
                        print(enc(f + b': no such file or directory').hex())
        else:
            print(b'XXX')
            #sys.stderr.write(repr(enc(words[0] + b': unknown command')) + '\n')
    except Exception as e:
        print(enc(f'Exception occured: {e}'.encode()).hex())

