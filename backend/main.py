from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
from PyPDF2 import PdfReader

app = FastAPI()

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# summarizer function
def summarize_text(text, max_sentences=5):
    sentences = sent_tokenize(text)
    freq = defaultdict(int)

    for word in word_tokenize(text.lower()):
        freq[word] += 1

    sentence_scores = {}

    for sentence in sentences:
        sentence_scores[sentence] = sum(freq.get(w, 0) for w in word_tokenize(sentence.lower()))

    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    summary_sentences = ranked_sentences[:max_sentences]
    summary = " ".join(summary_sentences)

    return summary


@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    text = ""
    reader = PdfReader(file.file)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    summary = summarize_text(text, max_sentences=5)

    return {
        "summary": summary,
        "characters_extracted": len(text)
    }