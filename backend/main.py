from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pdfplumber

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "PDF Summarizer API is running"}

def simple_summarize(text: str) -> str:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return " ".join(paragraphs[:8])  # take first 8 meaningful lines

@app.post("/summarize", summary="Summarize PDF", description="Upload a PDF and get summary")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            return JSONResponse(status_code=400, content={"error": "Only PDF files allowed"})

        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            return {"summary": "No readable text found in the PDF."}

        raw_summary = simple_summarize(text)

        formatted_summary = "\n".join(
            f"• {s.strip()}."
            for s in raw_summary.split(".")
            if len(s.strip()) > 20
        )

        return {"summary": formatted_summary}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})