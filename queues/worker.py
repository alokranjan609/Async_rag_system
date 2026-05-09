from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_qdrant import QdrantVectorStore
import os


os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    temperature=0.7
)

llm = ChatHuggingFace(llm=llm)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="pdf_chunks"
)



def process_query(query:str):
    print(f"Processing query: {query}")
    retrieved_docs = vector_store.similarity_search(query, k=2)
    retrieved_content = "\n\n".join([doc.page_content for doc in retrieved_docs])
    SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the following retrieved documents:\n\n{retrieved_docs}\n\nAnswer the question: {query}"""
    model_input = SYSTEM_PROMPT.format(retrieved_docs=retrieved_content, query=query)
    response = llm.invoke([HumanMessage(content=model_input)])
    return response.content