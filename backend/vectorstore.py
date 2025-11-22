import os
import chromadb
from chromadb.utils import embedding_functions
from config_manager import ConfigManager
from document_processing import DocumentProcessor as DocPro
from data_chunking import Chunker 

class VectorStore:
    def __init__(self):
        cm = ConfigManager()
        embedding_model_name = cm.get_env_variable(
            source='config',
            key='SENTENCE_EMBEDDING_MODEL',
            section='VECTOR_DB'
        )
        path = cm.get_env_variable(
            source='config',
            key='VECTOR_STORE_PATH',
            section='VECTOR_DB'
        )

        client = chromadb.PersistentClient(path=path)
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model_name
        )
        self.collection = client.get_or_create_collection(name="documents", embedding_function=embedding_function)

    def __process_and_insert_file(self, file_path: str):
        text = DocPro.extract_text(file_path)
        chunks = Chunker.chunk_text(text)

        file_name = os.path.basename(file_path)
        metadatas = [{"source": file_name, "chunk": i} for i in range(len(chunks))]
        ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        

    def insert_data_into_vector_db(self, folder_path: str):
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        for file_path in files:
            self.__process_and_insert_file(file_path)
            print(f"Inserted data from {file_path} into vector database.")
      

    def vectordb_query(self, query: str, n_results: int = 2):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results



if __name__ == "__main__":
    vector_store = VectorStore()
    data_folder = r"./data"
    vector_store.insert_data_into_vector_db(data_folder)
    search_results = vector_store.vectordb_query("What is american health care system?", n_results=2)
    print(search_results)