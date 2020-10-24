import itertools
import re

import streamlit as st


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
             'i.e.': 'i.e - ',
             'dient': 'different',
             }

    s = re.sub(r'(\S{1})-(\s{2})?'+'\n?', r'\1', s)
    s = re.sub(r'\n\s*', ' ', s)
    s = ' '.join(s.split(' '))

    for k,v in repls.items():
        s = s.replace(k,v)

    words = s.split()
    for w,word in enumerate(words):
        # if word=='how' and words[w+2]=='parts':
        #     st.warning(word)
        #     for char in words[w+1]:
        #         st.warning(f"{char}: {ord(char)}")

        if all(1<=ord(char)<=255 for char in word): continue
        if any(char not in repls for char in word):
            st.warning(word)
            for char in word:
                st.warning(f"{char}: {ord(char)}")

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
