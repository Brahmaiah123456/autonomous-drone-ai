from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from sklearn.feature_extraction.text import HashingVectorizer


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# LOCAL EMBEDDING MODEL
# ============================================================

class LocalEmbedding:
    """
    Lightweight local embedding system.

    Uses scikit-learn HashingVectorizer instead of:
    - PyTorch
    - Sentence Transformers
    - ONNX Runtime

    This keeps the project easy to run on Windows.
    """

    def __init__(self):
        self.vectorizer = HashingVectorizer(
            n_features=384,
            alternate_sign=False,
            norm="l2"
        )

    def embed_documents(self, texts):
        """
        Convert multiple documents into numerical vectors.
        """
        vectors = self.vectorizer.transform(texts)

        return vectors.toarray().tolist()

    def embed_query(self, text):
        """
        Convert one search query into a numerical vector.
        """
        vector = self.vectorizer.transform([text])

        return vector.toarray()[0].tolist()


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():

    documents = []

    print("\nLoading drone knowledge documents...")

    for file_path in DATA_DIR.glob("*.txt"):

        print(f"Loading: {file_path.name}")

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        loaded_documents = loader.load()

        documents.extend(loaded_documents)

    print(f"\nDocuments loaded: {len(documents)}")

    return documents


# ============================================================
# SPLIT DOCUMENTS
# ============================================================

def split_documents(documents):

    print("\nSplitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    return chunks


# ============================================================
# CREATE VECTOR DATABASE
# ============================================================

def create_vector_database():

    print("\n" + "=" * 60)
    print("CREATING DRONE KNOWLEDGE BASE")
    print("=" * 60)

    # Load documents
    documents = load_documents()

    if not documents:

        print("\nERROR: No documents found.")

        return None

    # Split documents
    chunks = split_documents(documents)

    # Create local embedding model
    print("\nCreating local embedding model...")

    embedding_function = LocalEmbedding()

    print("Embedding model ready.")

    # Create Chroma database
    print("\nCreating Chroma vector database...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=str(CHROMA_DIR),
        collection_name="drone_knowledge"
    )

    print("\n" + "=" * 60)
    print("VECTOR DATABASE CREATED SUCCESSFULLY")
    print("=" * 60)

    print("\nDatabase location:")
    print(CHROMA_DIR)

    print(f"\nTotal chunks stored: {len(chunks)}")

    return vector_store


# ============================================================
# LOAD EXISTING VECTOR DATABASE
# ============================================================

def load_vector_database():

    embedding_function = LocalEmbedding()

    vector_store = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_function,
        collection_name="drone_knowledge"
    )

    return vector_store


# ============================================================
# SEARCH KNOWLEDGE BASE
# ============================================================

def search_knowledge(query, number_of_results=3):

    print("\n" + "=" * 60)
    print("SEARCHING DRONE KNOWLEDGE")
    print("=" * 60)

    print("\nQuestion:")
    print(query)

    # If database does not exist, create it
    if not CHROMA_DIR.exists():

        print("\nVector database not found.")

        create_vector_database()

    # Load database
    vector_store = load_vector_database()

    # Search
    results = vector_store.similarity_search(
        query,
        k=number_of_results
    )

    return results


# ============================================================
# DISPLAY SEARCH RESULTS
# ============================================================

def display_results(results):

    print("\n" + "=" * 60)
    print("RETRIEVED KNOWLEDGE")
    print("=" * 60)

    for index, result in enumerate(results, start=1):

        print(f"\n--- RESULT {index} ---")

        print(result.page_content)

        source = result.metadata.get(
            "source",
            "Unknown"
        )

        print(f"\nSource: {source}")

        print("-" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("=" * 60)
    print(" AUTONOMOUS DRONE MISSION INTELLIGENCE SYSTEM")
    print(" RAG KNOWLEDGE ENGINE")
    print("=" * 60)

    # Create knowledge base
    create_vector_database()

    # Test question
    question = (
        "What should happen if the drone battery "
        "falls below 20 percent during a mission?"
    )

    # Search knowledge
    results = search_knowledge(
        question,
        number_of_results=3
    )

    # Display results
    display_results(results)

    print("\n")

    print("=" * 60)
    print("RAG TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)