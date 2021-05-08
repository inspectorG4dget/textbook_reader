import collections
import os
import time

from mutagen.mp3 import MP3
import nltk
import streamlit as st

import lib
import pdf as pdf

from playsound import playsound


def selectFilename(root=None):
    if root is None: root = os.getcwd()
    path = [root]
    seg = st.selectbox("Select a file", [fname for fname in os.listdir(os.path.join(*path)) if not fname.startswith('.')])
    if seg: path.append(seg)
    while seg and os.path.isdir(os.path.join(*path)):
        seg = st.selectbox("Select a file", [''] + os.listdir(os.path.join(*path)))
        if seg: path.append(seg)
        if os.path.isfile(os.path.join(*path)): return os.path.join(*path)


def main(assetDir):

    progress = st.progress(0)

    with st.sidebar:
        infilepath = selectFilename()
        if st.button("Preprocess file"):
            st.write("Processing Pages in File")
            if infilepath:
                pdf.preProcess(infilepath, assetDir, progress)

        pageNum = st.number_input("Which Page would you like to re-process?", min_value=1, step=1)
        if st.button("Reprocess"):
            pdf.reprocess(infilepath, pageNum, assetDir, progress)

    startFrom = st.number_input("Which page would you like to start from?",
                                min_value = 1,
                                value = 1,
                                step = 1
                                )
    if st.button("Read aloud"):
        dirpath = os.path.join(assetDir, os.path.basename(infilepath))
        display = st.empty()
        for page in sorted([p for p in os.listdir(dirpath)], key=lambda fpath: int(os.path.basename(fpath).rsplit('.',1)[0])):
            with open(os.path.join(dirpath, page, 'text.txt')) as infile: text = infile.read()
            sentences = nltk.sent_tokenize(text)
            for s,sentence in enumerate(sentences):
                audioFilePath = os.path.join(dirpath, page, f"{s}.mp3")
                displayText = sentences[:s] + [f"**{sentence}**"] + sentences[s+1:]
                displayText = '\n'.join(displayText)
                displayText = lib.wordWrap(displayText, 80)
                display.markdown('\n'.join(displayText))
                playsound(audioFilePath)


if __name__ == "__main__":

    assetDir = os.path.join('DataFiles', 'assets')
    main(assetDir)