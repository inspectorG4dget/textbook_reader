import glob
import os

import fitz as pdf
import nltk

import lib
import streamlit as st


def preProcess(infilepath, assetDir, progress):
    fname = os.path.basename(infilepath)
    doc = pdf.Document(infilepath)
    progStep = 1/len(doc)
    innerProg = st.empty()
    innerProg = innerProg.beta_columns(2)
    iProg = innerProg[1].progress(0)
    iProgText = innerProg[0].empty()
    for pageNum, page in enumerate(doc, 1):
        outdirpath = os.path.join(assetDir, fname, f"{pageNum}")
        os.makedirs(outdirpath, exist_ok=True)
        text = lib.textify(page)
        with open(os.path.join(outdirpath, 'text.txt'), 'w') as outfile: outfile.write(text)

        sentences = nltk.sent_tokenize(text)
        perSent = 1/len(sentences)

        iProgText.write(f"Processing Sentences on Page {pageNum}")
        for snum, sentence in enumerate(sentences):
            outfilepath = os.path.join(outdirpath, f"{snum}.mp3")
            if os.path.exists(outfilepath): os.remove(outfilepath)
            lib.tts(sentence, outfilepath)
            iProg.progress(snum * perSent)

        progress.progress(pageNum * progStep)


def reprocess(infilepath, pageNum, assetDir, progress):
    fname = os.path.basename(infilepath)
    outdirpath = os.path.join(assetDir, fname, f"{pageNum}")
    for fpath in glob.glob(os.path.join(outdirpath, '*.mp3')):
        os.remove(fpath)
    with open(os.path.join(assetDir, fname, f"{pageNum}", 'text.txt')) as infile:
        text = infile.read()
    with open(os.path.join(assetDir, fname, f"{pageNum}", 'text.txt'), 'w') as outfile:
        outfile.write(text)

    sentences = nltk.sent_tokenize(text)
    perSent = 1/len(sentences)
    st.write(f'Processing Sentences on Page {pageNum}')
    for snum, sentence in enumerate(sentences,1):
        speech = tts(sentence)
        outfilepath = os.path.join(outdirpath, f"{snum}.mp3")
        if os.path.exists(outfilepath): os.remove(outfilepath)
        speech.save(outfilepath)
        progress.progress(snum*perSent)


if __name__ == "__main__":
    print('starting')
    testFile = os.path.join('DataFiles', 'Sample Textbook.pdf')
    assetDir = os.path.join('DataFiles', 'assets')
    preProcess(testFile, assetDir, None)
    print('done')