from connectors.csv_connector import CSVConnector
from engine.schema_discovery import SchemaDiscovery
from engine.prompt_manager import PromptManager
from engine.llm_client import LLMClient
from engine.answer_generator import AnswerGenerator


def main():
    csv_path = "sample_data/sample_deals.csv"

    # Load data
    connector = CSVConnector(csv_path)
    connector.connect()

    dataframe = connector.get_records()

    # Discover schema
    schema_discovery = SchemaDiscovery(dataframe)
    schema = schema_discovery.analyze()

    # Initialise components
    prompt_manager = PromptManager()
    llm_client = LLMClient()
    answer_generator = AnswerGenerator()

    print("=" * 60)
    print("Semantic Business Translator")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask a business question: ").strip()

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        try:
            # Build prompt
            messages = prompt_manager.build_messages(schema, question)

            # Send to LLM
            structured_query = llm_client.generate_query(messages)

            print("\nStructured Query:")
            print(structured_query)

            # Execute query
            answer = answer_generator.generate_answer(
                dataframe,
                structured_query
            )

            print("\nAnswer:")
            print(answer)
            print()

        except Exception as error:
            print("\nAn error occurred:")
            print(error)
            print()

    connector.disconnect()


if __name__ == "__main__":
    main()