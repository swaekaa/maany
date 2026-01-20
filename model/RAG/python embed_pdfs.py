from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os, glob

# Initialize embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Initialize Chroma
vector_store = Chroma(
    collection_name="college_pdfsn",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

pdf_folder = "./pdfs/"
pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

# Pull existing IDs from Chroma (filenames used as IDs)
existing_ids = set(vector_store._collection.get()["ids"])

for pdf_file in pdf_files:
    file_id = os.path.basename(pdf_file)  # use filename as unique ID

    if file_id in existing_ids:
        print(f"⚠️ Skipping {file_id}, already embedded")
        continue

    loader = PyPDFLoader(pdf_file)
    docs = loader.load()
    splits = text_splitter.split_documents(docs)

    batch_size = 10
    for i in range(0, len(splits), batch_size):
        batch = splits[i:i+batch_size]
        texts = [doc.page_content for doc in batch]
        metadatas = [{"source": file_id} for _ in batch]  # track source file
        vector_store.add_texts(texts, metadatas=metadatas, ids=[f"{file_id}_{j}" for j in range(len(batch))])
        print(f"✅ {file_id} - batch {i//batch_size+1} stored")
