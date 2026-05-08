from fastapi import FastAPI,Request
import time

failure_count = 0
CIRCUIT_OPEN = False
FAILURE_THRESHOLD = 3

app = FastAPI()

@app.get("/")
def home():
    return {"message": "StudySync API"}


@app.middleware("http")
async def add_student_id_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = "BSAI23044"
    return response

def fake_llm_call():
    raise Exception("LLM timeout")

@app.get("/ask-naive")
def ask_naive():
    result = fake_llm_call()
    return {"response": result}

@app.get("/ask-protected")
def ask_protected():

    global failure_count
    global CIRCUIT_OPEN

    if CIRCUIT_OPEN:
        return {
            "message": "LLM unavailable. Using fallback response."
        }

    try:
        result = fake_llm_call()

        failure_count = 0

        return {"response": result}

    except Exception:

        failure_count += 1

        if failure_count >= FAILURE_THRESHOLD:
            CIRCUIT_OPEN = True

        return {"error": "LLM failed"}