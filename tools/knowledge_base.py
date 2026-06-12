# tools/knowledge_base.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain.schema import Document
from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, PERSIST_DIR, CACHE_DIR

def build_knowledge_base(documents: List[Document] = None):
    # Embeddings with cache (filing cabinet)
    underlying = OpenAIEmbeddings(model="text-embedding-3-small")
    fs = LocalFileStore(CACHE_DIR)
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        underlying, fs, namespace="research_agent"
    )
    
    if documents is None:
        # Load existing — don't re-embed
        vectorstore = Chroma(
            collection_name="research_knowledge",
            embedding_function=cached_embeddings,
            persist_directory=PERSIST_DIR
        )
        # Get docs for BM25
        results = vectorstore._collection.get()
        docs = [
            Document(page_content=text, metadata=meta)
            for text, meta in zip(
                results["documents"],
                results["metadatas"]
            )
        ]
        bm25 = BM25Retriever.from_documents(docs)
    else:
        # Split
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(documents)
        
        # Store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=cached_embeddings,
            collection_name="research_knowledge",
            persist_directory=PERSIST_DIR
        )
        bm25 = BM25Retriever.from_documents(chunks)

    bm25.k = TOP_K
    
    vector_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K, "fetch_k": TOP_K * 4}
    )
    
    # Hybrid — 30% keyword, 70% semantic
    hybrid = EnsembleRetriever(
        retrievers=[bm25, vector_retriever],
        weights=[0.3, 0.7]
    )
    
    return hybrid

# Build once, reuse everywhere
retriever = build_knowledge_base(None)