# Semantic Business Translator

A modular Python application that translates natural language business questions into structured JSON queries using the OpenAI Responses API and executes them against tabular business data using pandas.

The project demonstrates prompt engineering, schema-aware query generation, modular software architecture, and deterministic query execution.

---

## Features

- Translate natural language into structured JSON queries
- Schema-aware prompt generation
- Metadata-driven semantic column mapping
- Execute structured queries on CSV data
- Support for:
  - Count
  - List
  - Sum
  - Average
  - Minimum
  - Maximum
- Equality-based filtering
- Modular connector architecture for future CRM integrations
- OpenAI Responses API integration

---

## Architecture

```
                    User Question
                           │
                           ▼
                  Prompt Manager
                           │
                           ▼
                     OpenAI API
                           │
                           ▼
                 Structured JSON
                           │
                           ▼
                 Answer Generator
                           │
                           ▼
                    Business Answer
```

The language model is responsible only for translating natural language into a structured JSON query.

All business logic and query execution are performed locally using pandas. This separation keeps execution deterministic, testable, and independent of the language model.

---

## Project Structure

```
semantic-business-translator/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── connectors/
│   ├── base_connector.py
│   ├── csv_connector.py
│   └── hubspot_connector.py
│
├── engine/
│   ├── answer_generator.py
│   ├── explanation_engine.py
│   ├── intent_parser.py
│   ├── llm_client.py
│   ├── prompt_manager.py
│   ├── query_engine.py
│   ├── schema_discovery.py
│   └── semantic_mapper.py
│
├── prompts/
│   ├── examples.json
│   ├── explanation_prompt.txt
│   ├── intent_prompt.txt
│   ├── output_schema.json
│   ├── semantic_mapping_prompt.txt
│   └── system_prompt.txt
│
├── sample_data/
│   ├── sample_contacts.csv
│   └── sample_deals.csv
│
└── docs/
    ├── api_design.md
    └── architecture.md
```

---

## How It Works

1. Load business data using a connector.
2. Analyse the dataset schema.
3. Generate metadata describing each column.
4. Construct prompts using the prompt assets.
5. Send the prompt to the OpenAI Responses API.
6. Receive a structured JSON query.
7. Execute the query locally using pandas.
8. Return the final business answer.

---

## Supported Operations

The current implementation supports:

- Count matching records
- List matching records
- Sum numeric values
- Average numeric values
- Minimum values
- Maximum values
- Equality (`=`) filtering

---

## Example

### User Question

```text
How many open deals are assigned to Rahul?
```

### Structured Query

```json
{
  "intent": "count",
  "entity": "deals",
  "target_column": null,
  "filters": [
    {
      "column": "Assigned To",
      "operator": "=",
      "value": "Rahul"
    },
    {
      "column": "Status",
      "operator": "=",
      "value": "Open"
    }
  ]
}
```

### Output

```text
There are 5 matching records.
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/adiinterviewprep121/semantic-business-translator.git
```

Move into the project directory.

```bash
cd semantic-business-translator
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your OpenAI API key.

```text
OPENAI_API_KEY=your_api_key
```

---

## Running the Application

```bash
python app.py
```

Example session:

```text
============================================================
Semantic Business Translator
============================================================

Ask a business question:
> What is the average deal value?

Average Deal Value: 24350.00
```

---

## Design Decisions

The project follows a modular architecture where each component has a single responsibility.

| Component | Responsibility |
|----------|----------------|
| Connector | Retrieves business data from the source system |
| Schema Discovery | Generates metadata describing the dataset |
| Prompt Manager | Builds prompts for the language model |
| LLM Client | Communicates with the OpenAI Responses API |
| Answer Generator | Executes structured queries locally |

The connector layer abstracts the underlying data source. Any CRM or business system can be integrated by implementing the connector interface and returning a pandas DataFrame. The remaining application components remain unchanged.

The language model is responsible only for translating natural language into a structured JSON query. All query execution is performed locally, making the system deterministic and easy to test.

---

## Future Improvements

Potential enhancements include:

- Support for additional filter operators (`>`, `<`, `>=`, `<=`, `!=`, `contains`)
- Fuzzy matching for column names and categorical values
- Additional CRM connectors
- SQL database connectors
- Query explanation generation
- Conversation memory
- Unit and integration tests
- Logging and monitoring

---

## Requirements

- Python 3.10+
- OpenAI API Key

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## License
This project was developed as part of a technical interview assessment and is intended for demonstration purposes.
