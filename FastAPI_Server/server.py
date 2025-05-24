from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from model.rag import generate_answer, initialize_components

# ✅ Initialize vector DB and LLM at startup
initialize_components()

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
        print(f"Incoming query: {input_data.query}")
        answer = generate_answer(input_data.query)
        print(f"Answer generated: {answer}")
        return {"answer": answer}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
