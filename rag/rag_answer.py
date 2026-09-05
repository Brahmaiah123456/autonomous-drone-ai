from ollama import chat

from rag.rag_pipeline import search_knowledge


def build_context(results):
    """Combine retrieved documents into context."""

    context = ""

    for i, result in enumerate(results, start=1):

        source = result.metadata.get(
            "source",
            "Unknown"
        )

        context += f"""
--- SOURCE {i} ---
Source: {source}

{result.page_content}
"""

    return context


def answer_question(question):
    """Retrieve knowledge and generate a grounded answer."""

    print("\nSearching drone knowledge base...")

    # Step 1: Retrieve relevant documents
    results = search_knowledge(
        question,
        number_of_results=3
    )

    # Step 2: Build RAG context
    context = build_context(results)

    # Step 3: Create grounded prompt
    prompt = f"""
You are an AI assistant for an autonomous drone mission system.

Answer the user's question using ONLY the provided drone knowledge.

Do not invent safety rules.

If the answer is not available in the provided knowledge,
say that the information is not available and recommend human review.

DRONE KNOWLEDGE:
{context}

USER QUESTION:
{question}

Give a clear and concise answer.
Mention the relevant safety action when applicable.
"""

    print("\nGenerating answer with local LLM...")

    # Step 4: Ask local Ollama model
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a safe and explainable "
                    "drone AI assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    # Step 5: Display answer
    print("\n" + "=" * 60)
    print("DRONE AI ANSWER")
    print("=" * 60)

    print("\n" + answer)

    # Step 6: Display sources
    print("\n" + "=" * 60)
    print("SOURCES USED")
    print("=" * 60)

    for i, result in enumerate(results, start=1):

        source = result.metadata.get(
            "source",
            "Unknown"
        )

        print(f"{i}. {source}")

    return answer


if __name__ == "__main__":

    question = input(
        "\nAsk the drone system a question: "
    )

    answer_question(question)