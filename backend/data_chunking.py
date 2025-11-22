from document_processing import DocumentProcessor as DocProcessor

class Chunker:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500) -> list:
        chunks = []
        sentnces = text.replace('\n', ' ').split('. ')
        current_chunk = []
        current_chunk_size = 0
        for sentence in sentnces:
            sentence = sentence.strip()
            if not sentence:
                continue
            if not sentence.endswith('.'):
                sentence += '.' 
            sentence_length = len(sentence)

            if current_chunk_size + sentence_length <= chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_chunk_size = sentence_length
            else:
                current_chunk.append(sentence)
                current_chunk_size += sentence_length
        return chunks
    
if __name__=='__main__':
    pdf_path = r"./data/sample.pdf"
    smaple_text = DocProcessor.extract_text(pdf_path)
    chunks = Chunker.chunk_text(smaple_text)
    print(len(chunks),"\n", chunks[1])