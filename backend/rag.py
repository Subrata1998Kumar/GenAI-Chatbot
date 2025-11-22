from openai import OpenAI
from config_manager import ConfigManager
from vectorstore import VectorStore as vs

class RAGClient:
    def __init__(self):
        cm = ConfigManager()
        api_key = cm.get_env_variable(source='env', key='RAG_API_KEY')
        base_url = cm.get_env_variable(source='env', key='RAG_BASE_URL')
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.rag_model_name = cm.get_env_variable(source='config', key='RAG_MODEL_NAME', section='RAG_MODEL')
    
    def __get_prompt(self, query: str, context: str):
        prompt = f"""Based on the following context, please answer the question.
        If the answer cannot be derived from the context, say "I cannot answer this based on the provided context."
        
        Context:
        {context}

        Question: {query}

        Answer:"""

        return prompt
    
    def generate_response(self, query: str, context: str):
        """Generate a response using OpenAI"""

        prompt = self.__get_prompt(query, context)
        print(prompt)
        response = self.client.chat.completions.create(
            model=self.rag_model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            # temperature=0,
            # max_tokens=500
        )
        return {"generated_text": response.choices[0].message.content}
    
if __name__ == "__main__":
    rag_client = RAGClient()
    vs = vs()
    query = "Explain the american health care system?"
    results = vs.vectordb_query(query, n_results=2)
    sources = [f"{meta['source']} (chunk {meta['chunk']})" for meta in results['metadatas'][0]]
    context = " ".join(results['documents'][0])
    
    response = rag_client.generate_response(query, context)
    print("Generated Response:", response["generated_text"])
    print("Sources:", sources)