from rag.rag_pipeline import search_knowledge


def rag_agent(question):
    """
    RAG Agent:
    Searches the drone knowledge base and returns
    relevant evidence for the other agents.
    """

    print("\n" + "=" * 60)
    print("RAG AGENT")
    print("=" * 60)

    print(f"\nQuestion: {question}")

    # Search the knowledge base
    results = search_knowledge(
        question,
        number_of_results=3
    )

    evidence = []

    for result in results:

        source = result.metadata.get(
            "source",
            "Unknown"
        )

        evidence.append({
            "source": source,
            "content": result.page_content
        })

    print(f"\nRetrieved {len(evidence)} pieces of evidence.")

    return evidence


if __name__ == "__main__":

    question = input(
        "\nEnter a drone question: "
    )

    evidence = rag_agent(question)

    print("\n" + "=" * 60)
    print("RAG EVIDENCE")
    print("=" * 60)

    for i, item in enumerate(evidence, start=1):

        print(f"\n--- Evidence {i} ---")
        print(f"Source: {item['source']}")
        print(item["content"])