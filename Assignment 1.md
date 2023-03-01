*Contents:*

[TOC]

## Request

1. Each team member designs a Vigenere Cipher system and sends an 

   encrypted ciphertext to the Team Captain, who will  merge these ciphertexts to a single .txt file (separate each ciphertext explicitly) and forward this file to TA through email as the challenge. DDL: 2023/2/25 10:00 (UTC+8).

   - TA's email: [dabeidouretriever@sjtu.edu.cn](mailto:dabeidouretriever@sjtu.edu.cn)
   - Please set the email's subject as "CS7350-Assignment1-<your Team Name>-Submit challenge". The challenge should be appended as an attached document and renamed as "CS7350-Assignment1-<your Team Name>-Submit challenge.txt".
   - TA will forward these challenges to another team for cracking and, at the same time, you will receive the challenge from another team before 2023/2/26 10:00 (UTC+8). 

2. Write down how your crack it step-by-step as your assignment in English.

   - Please submit your assignment by yourself. DDL: 2023/3/5 23:59 (UTC+8).



## Vigenere Cipher System

Vigenere cipher is a kind of substitution cipher. Its main idea is to replace the plaintext with the key in a circular way. I ameliorate the source code of the **Cipher,** the parent class, in the **pycipher** library[1], trying to implement the encryption and decryption system with brief python code. This class provides some abstract functions and conversion functions between English characters and natural numbers. 

```python
class Cipher(object):
    def encipher(self, string):
        return string
    def decipher(self, string):
        return string
    def a2i(self, ch):
        ch = ch.upper()
        arr = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8,'J': 9, 'K': 10,'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16,'R': 17, 'S': 18, 'T': 19, 'U': 20,'V': 21, 'W': 22, 'X': 23, 'Y': 24,'Z': 25}
        return arr[ch]

	def i2a(self, i):
        i = i % 26
        arr = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N','O','P', 'Q', 'R', 'S', 'T', 'U', 'V','W', 'X', 'Y', 'Z')
        return arr[i]
    def remove_punctuation(self, text, filter='[^A-Z]'):
        return re.sub(filter, '', text.upper())
    def remove_blank(self,text):
        return text.upper().replace('\n','').replace(' ','')
```

Inherited from the parent, class **Vigenere** is implemented to specific encryption and decryption functions. When encrypting or decrypting text, just call the above functions. *We removed the spaces between the words, but reserved a part (punctuation marks), so that the cracker knew that he was cracking an English article.*

```python
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
```

## Crack Cipher Step-by-step

### Cipher Text

Nothing can be observed obviously, which means there is no shortcut.

```python
ywwppstuimzddnscehjnmcdtyqqpxysiqptsdmcfplniresassczfftzczfrnvxpcexbmyuijymfhormrdnoqtirpaxnscxenpegplndiotnypmdniygwtycjkltwdmwsolniescveipecottjytwdypmddcmwswnrjixpobducxztmmvtyttirpicjtppytxklzzlnvxpcmxwjdeuigmetshmvelistcypeitiddttaejehfbxsprjivpllxwietqzmxepaslfpsaaqsctntzhpcttjytwdfagszoqbllecfvwpcvjiwlxoimpqzrftpstgmagszoqaxfoesbwtsaamenzrwmgeltyqxfoefvhfyrjumeeisoiqqowbwpgewghljwjuydeahpmpgeypirzaqwjtycwmedtnlaxfoesbwlydgmgzxisoxspbjaxstgmagszoqqresehqxjehnamdyoyirpipjkxleitvffeaswfwtgfbmzytmixxfsyjiqflkqpwpd
```

### Determine key length

#### Kasiski Test

Kasiski test is used to find the length of key through computing the maximum common divisor of the distance between two duplicate strings. The implementation process can be divided into two parts: the first step is to find all repeated *segments* with a length of at least $3$; the second step is to calculate the maximum common divisor of distance. The definition of function **kasiski** is as following:

```python
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
```

And ``gcd()`` is defined as:

```python
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
```

Execute code with ``seglen=3``and we get these:

```
XFO : [332, 356, 422]   [24, 66] , gcd: 6
SZO : [291, 327, 453]   [36, 126] , gcd: 18
AGS : [289, 325, 451]   [36, 126] , gcd: 18
FOE : [333, 357, 423]   [24, 66] , gcd: 6
TWD : [123, 147, 285]   [24, 138] , gcd: 6
ZOQ : [292, 328, 454]   [36, 126] , gcd: 18
IRP : [86, 181, 475]   [95, 294] , gcd: 1
GSZ : [290, 326, 452]   [36, 126] , gcd: 18
```

Execute code with ``seglen=4``and we get these:

```
GSZO : [290, 326, 452]   [36, 126] , gcd: 18
XFOE : [332, 356, 422]   [24, 66] , gcd: 6
SZOQ : [291, 327, 453]   [36, 126] , gcd: 18
AGSZ : [289, 325, 451]   [36, 126] , gcd: 18
```

Execute code with ``seglen=5``and we get these:

```
GSZOQ : [290, 326, 452]   [36, 126] , gcd: 18
AGSZO : [289, 325, 451]   [36, 126] , gcd: 18
```

From the above results, we can roughly infer that the length of the key may be ``6`` or ``18``.

#### Coincidence Index

Coincidence index is an other way to determine the key length. The test by coincidence Index takes advantage of the idea of birthday attack. Coincidence index refers to *the sum of the same probability of two random elements[2]*, that is, $CI=\sum_{i=1}^nP_i^2$, where $P_i$ stands for the probability of occurrence of each letter. In a completely random English text $CI = 0.0385$, and in a meaningful English text $CI = 0.065$. In practice, we use the estimated value $CI'=\sum_{i=1}^n\frac{f_i\cdot(f_{i}-1)}{L\cdot(L-1)}$ of $CI$. Divide the ciphertext into ``m`` groups according to the compensation of ``keylen``, and calculate the ``CI`` of each group. If the result is close to $0.065$, ``keylen`` is the key length.

```python
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

for i in range(1, 19): 
    coincidenceIndex(ciphertext, i)
```

The main results are as follows. By observation, we can find that ``CI`` is the closest to ``0.065`` when ``keylen=6``. When the key length is a multiple of $6$, the $CI$ is also very close to $0.065$, which is because we can just write the key several times to get a "new" key.

```
1: 0.044 
2: 0.049 0.046 
3: 0.053 0.044 0.048 
4: 0.047 0.042 0.047 0.046 
5: 0.042 0.042 0.038 0.052 0.048 
6: 0.065 0.057 0.067 0.072 0.060 0.059 
7: 0.040 0.040 0.048 0.048 0.041 0.051 0.044 
8: 0.041 0.035 0.049 0.047 0.054 0.047 0.047 0.052 
9: 0.048 0.050 0.056 0.065 0.034 0.047 0.056 0.047 0.045 
10: 0.047 0.048 0.048 0.057 0.053 0.040 0.047 0.035 0.051 0.048 
11: 0.037 0.053 0.050 0.042 0.035 0.052 0.035 0.056 0.052 0.041 0.039 
12: 0.051 0.053 0.053 0.072 0.048 0.053 0.071 0.060 0.071 0.061 0.065 0.056 
13: 0.038 0.032 0.050 0.049 0.036 0.031 0.062 0.037 0.044 0.055 0.033 0.031 0.045 
14: 0.033 0.048 0.054 0.038 0.039 0.066 0.056 0.047 0.035 0.051 0.072 0.056 0.030 0.039 
15: 0.044 0.040 0.044 0.066 0.045 0.055 0.066 0.039 0.057 0.067 0.037 0.045 0.055 0.045 0.034 
16: 0.045 0.027 0.055 0.055 0.053 0.044 0.036 0.034 0.042 0.036 0.028 0.044 0.058 0.048 0.060 0.071 
17: 0.028 0.037 0.039 0.045 0.039 0.043 0.034 0.065 0.041 0.043 0.052 0.047 0.053 0.044 0.041 0.055 0.030 
18: 0.071 0.084 0.071 0.079 0.044 0.069 0.069 0.047 0.069 0.067 0.057 0.071 0.084 0.042 0.057 0.059 0.064 0.057
```

### Determine key content

#### Chi-Squared Test

We define the quasi coincidence index as $\mathcal{X}=\sum_{i=1}^np_iq_i$, $p_i$ indicates the probability of occurrence of the letter $i$ in the Virginia ciphertext, $q_i$ indicates the probability of the letter $i$ in the normal English text. When the two frequency distributions are similar, the value of $\mathcal{X}$ is relatively high.

```python
def chi(ciphertext):
    cipher = ciphertext
    standard = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D':0.043, 'E': 0.127, 'F': 0.022, 'G': 0.020,'H': 0.061,'I': 0.070, 'J': 0.002, 'K':0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019, 'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091, 'U': 0.028,'V': 0.010, 'W': 0.023, 'X': 0.001,'Y': 0.020, 'Z': 0.001}
    frequency = standard.copy()
    corelation = [0] * 26
    length = len(cipher)
    for key,value in frequency.items():
        frequency[key] = cipher.count(key)/length
    for i in range(26):
        for j in range(26):
            corelation[i] += frequency[i2a((i+j)%26)] * 				standard[i2a(j)]
    return corelation
```

Execute ``chi(ciphertext)`` for the 6 groups of ``ciphertext`` in 3.2, we get:

```
[0.037, 0.043, 0.034, 0.03, 0.042, 0.068, 0.037, 0.031, 0.034, 0.042, 0.034, 0.037, 0.04, 0.03, 0.036, 0.041, 0.047, 0.036, 0.042, 0.037, 0.045, 0.038, 0.034, 0.03, 0.038, 0.039]
[0.037, 0.041, 0.04, 0.032, 0.042, 0.038, 0.033, 0.039, 0.063, 0.04, 0.029, 0.031, 0.045, 0.036, 0.035, 0.041, 0.037, 0.032, 0.038, 0.043, 0.038, 0.04, 0.044, 0.041, 0.035, 0.031]
[0.035, 0.035, 0.034, 0.036, 0.065, 0.044, 0.03, 0.026, 0.044, 0.04, 0.038, 0.037, 0.035, 0.031, 0.039, 0.045, 0.038, 0.037, 0.039, 0.051, 0.042, 0.034, 0.028, 0.037, 0.043, 0.034]
[0.043, 0.048, 0.038, 0.032, 0.038, 0.036, 0.026, 0.037, 0.034, 0.03, 0.038, 0.069, 0.045, 0.031, 0.036, 0.049, 0.033, 0.036, 0.038, 0.03, 0.026, 0.034, 0.044, 0.042, 0.045, 0.041]
[0.046, 0.042, 0.036, 0.028, 0.038, 0.04, 0.041, 0.04, 0.033, 0.027, 0.039, 0.064, 0.042, 0.032, 0.033, 0.045, 0.036, 0.04, 0.036, 0.036, 0.037, 0.042, 0.041, 0.038, 0.037, 0.034]
[0.065, 0.037, 0.034, 0.034, 0.042, 0.029, 0.035, 0.038, 0.034, 0.035, 0.042, 0.046, 0.039, 0.042, 0.039, 0.048, 0.036, 0.033, 0.033, 0.037, 0.032, 0.036, 0.043, 0.037, 0.036, 0.041]
```

Find the maximum value above, we known that the key is ``FIELLA``.

### Crack it!

```python
print(decryption(ciphertext,'FIELLA').lower())
```

Then we get this, which is obviously a meaningful text.

```
toseesomebodyforthefirsttimemynameisyeyuelianthankyouforyourinterestinjieqiuwomenscollegeasformeihavelivedinthiscitysincechildhoodandworkedhardtobuildthisschoolcreatedbymymotherintoanexcellentschoolintermsofstudyitiscertainlyneedlesstosaythattherearealsoetiquetteandbehaviorinordertobuildaschoolthatcanserveasamodelforallhighschoolstudentsihaveacorrectattitudeandunremittingeffortseverydaywemustachievethegoalofincreasingstudentsandbecomingthebesthighschoolinthecitythisisnotanexpectationbutanobligationthatmustbefulfilled
```

Organize the language, we get the following text. It seems to be a speech by the president of a women's college.

```
To see somebody for the first time my name is yeyuelian. Thank you for your interest in Jieqiu Women's College. As for me, I have lived in this city since childhood and worked hard to build this school created by my mother into an excellent school in terms of study. It is certainly need less to say that there are also etiquette and behavior in order to build a school that can serve as a model for all high school students. I have a correct attitude and unremitting efforts everyday. We must achieve the goal of increasing students and becoming the best high school in the city .This is not an expectation but an obligation that must be fulfilled.
```

## Reference

[1]:[GitHub - jameslyons/pycipher: python module containing many classical cipher algorithms: Caesar, Vigenere, ADFGVX, Enigma etc.](https://github.com/jameslyons/pycipher)

[2]:[维吉尼亚密码的原理及破解 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/111611977)



## Appendix

Please visit my github page for the complete code:

