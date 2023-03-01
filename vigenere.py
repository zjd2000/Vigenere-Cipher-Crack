#coding=utf-8
import re

def a2i(ch):
    ch = ch.upper()
    arr = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
           'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
           'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
    return arr[ch]

def i2a(i):
    i = i % 26
    arr = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z')
    return arr[i]

class Cipher(object):
    def encipher(self, string):
        return string

    def decipher(self, string):
        return string

    def a2i(self,ch):
        ch = ch.upper()
        arr = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
               'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
               'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
        return arr[ch]

    def i2a(self,i):
        i = i % 26
        arr = (
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V',
            'W', 'X', 'Y', 'Z')
        return arr[i]

    def remove_punctuation(self, text, filter='[^A-Z]'):
        return re.sub(filter, '', text.upper())

    def remove_blank(self,text):
        return text.upper().replace('\n','').replace(' ','')

class Vigenere(Cipher):
    def __init__(self, key='fortification'):
        self.key = [k.upper() for k in key]

    def encipher(self, string):
        string = self.remove_punctuation(string)
        ret = ''
        i = 0
        for c in string:
            if not c.isupper():
                ret += c
                continue
            i = i % len(self.key)
            ret += self.i2a(self.a2i(c) + self.a2i(self.key[i]))
            i = i + 1
        return ret

    def decipher(self, string):
        string = self.remove_punctuation(string)
        ret = ''
        i = 0
        for c in string:
            if not c.isupper():
                ret += c
                continue
            i = i % len(self.key)
            ret += self.i2a(self.a2i(c) - self.a2i(self.key[i]))
            i = i + 1
        return ret

def encryption(plaintext, key):
    v = Vigenere(key)
    cipher = v.encipher(plaintext)
    print(cipher)
    return cipher

def decryption(ciphertext, key):
    v = Vigenere(key)
    plain = v.decipher(ciphertext)
    print(plain)
    return plain

def gcd(num):
    gcdl = []
    for i in range(1, sorted(num)[0] + 1):
        for index, j in enumerate(num):
            if j % i == 0:
                if (index + 1) == len(num):
                    gcdl.append(i)
                    break
                continue
            else:
                break
    if not gcdl:
        return 1
    else:
        return sorted(gcdl)[-1]

def kasiski(ciphertext):
    seglen = 3
    cipher = ciphertext
    seglist = []
    for i in range(seglen):
        segtmp = re.findall(r'.{3}', cipher)
        seglist += segtmp
        cipher = re.sub(r'.', '', cipher, count=1)
    repeatlist = []
    for i in range(len(seglist)):
        for j in range(len(seglist)):
            if (seglist[i] == seglist[j] and i != j):
                repeatlist.append(seglist[i])
    repeatlist = list(set(repeatlist))
    for i in repeatlist:
        count = ciphertext.count(i)
        if (count < 3): continue
        loclist = [0] * count
        pre = 0
        for j in range(count):
            loc = ciphertext.find(i, pre)
            loclist[j] = loc
            pre = loc + 1
        sublist = []
        for j in range(1,count):
            sublist.append(loclist[j]-loclist[j-1])
        print(i,':',loclist,' ', sublist ,', gcd:', gcd(sublist))

def getCI(ciphertext):
    cipher = ciphertext
    length = len(cipher)
    lettercount = [0] * 26
    CI = 0
    for i in range(26):
        lettercount[i] = cipher.count(i2a(i))
        CI += lettercount[i]*(lettercount[i]-1) / (length*(length-1))
    return CI

def coincidenceIndex(ciphertext, keylen):
    cipherset = [''] * keylen
    for i in range(keylen):
        for j in range(i,len(ciphertext),keylen):
            cipherset[i] += ciphertext[j]
    print(keylen, end=': ')
    for i in range(keylen):
        print(format(getCI(cipherset[i]), '.3f'), end=' ')
    print()
    return cipherset

def chi(ciphertext):
    cipher = ciphertext
    standard = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 'F': 0.022, 'G': 0.020, 'H': 0.061,
                'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019,
                'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091, 'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001,
                'Y': 0.020, 'Z': 0.001}
    frequency = standard.copy()
    corelation = [0] * 26
    length = len(cipher)
    for key,value in frequency.items():
        frequency[key] = cipher.count(key)/length
    for i in range(26):
        for j in range(26):
            corelation[i] += frequency[i2a((i+j)%26)] * standard[i2a(j)]
    return corelation

if __name__ == '__main__':
    with open('assignment.txt','r', errors='ignore') as infile:
        ciphertext = infile.read().upper()
    print('Length of cipher:', len(ciphertext))
    print('----------------Kasiski test:----------------')
    kasiski(ciphertext)
    print('----------------Coincidence Index Test:----------------')
    for i in range(1, 19): coincidenceIndex(ciphertext, i)
    cipherset = coincidenceIndex(ciphertext, 6)
    keyletter = [0] * 6
    print('----------------Chi Test:----------------')
    for i in range(6):
        corelation = chi(cipherset[i])
        for k in range(len(corelation)):
            corelation[k] = round(corelation[k],3)
        print(corelation)
        max = 0
        for j in range(0,26):
            if (corelation[j]>max):
                keyletter[i] = j
                max = corelation[j]
    print('KEY=',end='')
    for i in range(6):
        print(i2a(keyletter[i]),end='')
    print()
    print(decryption(ciphertext,'FIELLA').lower())


