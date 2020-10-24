import glob
import os

import PyPDF2 as pdf
import nltk
from gtts import gTTS as tts

import lib
import streamlit as st


def preProcess(infilepath, assetDir, progress):
    fname = os.path.basename(infilepath)
    with open(infilepath, 'rb') as infile:
        doc = pdf.PdfFileReader(infile)
        perPage = 1/doc.getNumPages()
        for pageNum, page in enumerate(doc.pages, 1):
            outdirpath = os.path.join(assetDir, fname, f"{pageNum}")
            os.makedirs(outdirpath, exist_ok=True)
            text = page.extractText()
            text = lib.sanitize(text)

            with open(os.path.join(outdirpath, 'text.txt'), 'w') as outfile:
                outfile.write(text)

            st.write(f"Processing Sentences on Page {pageNum}")
            innerProg = st.progress(0)
            sentences = nltk.sent_tokenize(text)
            numSentences = len(sentences)
            for snum, sentence in enumerate(sentences, 1):
                speech = tts(sentence)
                outfilepath = os.path.join(outdirpath, f"{snum}.mp3")
                if os.path.exists(outfilepath): os.remove(outfilepath)
                speech.save(outfilepath)
                innerProg.progress(snum/numSentences)

            progress.progress(pageNum * perPage)


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
    with open(testFile, 'rb') as infile:
        doc = pdf.PdfFileReader(infile)
        for pageNum, page in enumerate(doc.pages, 1):
            text = page.extractText()
            newText = lib.sanitize(text)
    # assetDir = os.path.join('DataFiles', 'assets')
    # preProcess(testFile, assetDir, None)
    print('done')