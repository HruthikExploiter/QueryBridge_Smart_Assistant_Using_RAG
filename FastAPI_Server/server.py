from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model.rag import generate_answer, initialize_components
import traceback

# ✅ Initialize vector DB and LLM at startup
try:
    initialize_components()
except Exception as e:
    print(f"❌ Failed to initialize components at startup: {e}")
    traceback.print_exc()

app = FastAPI()

# CORS (for frontend or Postman testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class QueryInput(BaseModel):
    query: str

# Health check
@app.get("/")
def read_root():
    return {"message": "FastAPI is running."}

# Main POST endpoint
@app.post("/ask")
def ask_question(input_data: QueryInput):
    try:
        print(f"📥 Incoming query: {input_data.query}")

        if not input_data.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty.")

        answer, sources = generate_answer(input_data.query)
        print(f"🧠 Answer generated: {answer}")

        return {
            "answer": answer or "No answer generated.",
            "sources": sources or "No sources available."
        }

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))
