from config_manager import ConfigManager
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from rag import RAGClient
from vectorstore import VectorStore 


app = FastAPI()
class RequestData(BaseModel):
    prompt: str
    # max_length: int = 20


@app.post("/generate")
async def generate_response(data: RequestData):
    rag_client = RAGClient()
    vs = VectorStore()
    results = vs.vectordb_query(data.prompt, n_results=2)
    context = " ".join(results['documents'][0])
    sources = [f"{meta['source']} (chunk {meta['chunk']})" for meta in results['metadatas'][0]]

    response = rag_client.generate_response(data.prompt, context)
    return {"generated_text": response["generated_text"]}
   

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    