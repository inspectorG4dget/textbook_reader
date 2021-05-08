import collections
import operator
import re

import requests
import streamlit as st
from bs4 import BeautifulSoup as BS
from gtts import gTTS as TTS

Sentence = collections.namedtuple('Sentence', 'text audioPath spanID')


def sanitize(s):
    repls = {"\nÞ": 'fi',
             "˜": "Th",
             '\n-\n': '',
             '-\n': '',
             # '\n': ' ',
             chr(8442): "'",
             chr(8482): "'",
             chr(8217): "'",
             chr(8212): " - ",
             chr(8211): " - ",
             chr(8220): '"',
             chr(8221): '"',
             chr(8226): '- ',
             chr(64257): '"',
             chr(64258): '"',
             '"': 'fi',
             'i.e.': 'i.e - ',
             'dient': 'different',
             }

    reRepls = {r'(\S{1})-\s*$': r'\1',
               r'.$': '. ',
               }

    for k,v in reRepls.items(): re.sub(k,v, s)
    for k,v in repls.items(): s = s.replace(k,v)

    # words = s.split()
    # for w,word in enumerate(words):
        # if word=='how' and words[w+2]=='parts':
        #     st.warning(word)
        #     for char in words[w+1]:
        #         st.warning(f"{char}: {ord(char)}")

        # if all(1<=ord(char)<=255 for char in word): continue
        # if any(char not in repls for char in word):
        #     st.warning(word)
        #     for char in word:
        #         st.warning(f"{char}: {ord(char)}")

    for char in s:
        if not 1 <= ord(char) <= 255:
            s = s.replace(char, '_')

    return s


def wordWrap(s, width):
    answer = []
    temp = []
    for word in s.split():
        if sum(map(len, temp)) + len(temp) + len(word) >= width:
            answer.append(' '.join(temp))
            temp = []
        temp.append(word)

    if temp: answer.append(' '.join(temp))
    return answer


def getHeader(soup):
    header = soup.div.p
    return header


def getPos(e):
    style = e.attrs['style']
    style = dict((part.split(":") for part in style.split(';')))
    keys = 'top left'.split()
    pos = operator.itemgetter(*keys)(style)
    return dict(zip(keys, pos))


def textify(page):
    html = page.getText('html')
    soup = BS(html, 'html.parser')
    header = getHeader(soup)
    hpos = getPos(header)

    answer = []
    for e in soup.div.children:
        if isinstance(e, str): continue
        if getPos(e)['top'] == hpos['top']: continue
        answer.append(sanitize(e.text))

    return ''.join(answer)


def tts(text, outfilepath):

    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl=en&ttsspeed=1&total=1&idx=0&client=tw-ob&tk=838940.655735"
    doc = requests.get(url)
    with open(outfilepath, 'wb') as f:
        f.write(doc.content)