import json
from pathlib import Path


class PromptManager:
    """
    Loads and manages all prompt assets required to communicate
    with the LLM.
    """

    def __init__(self):
        self.prompt_directory = Path("prompts")

        self.system_prompt = self._load_text("system_prompt.txt")
        self.intent_prompt = self._load_text("intent_prompt.txt")
        self.semantic_prompt = self._load_text("semantic_mapping_prompt.txt")

        self.output_schema = self._load_json("output_schema.json")
        self.examples = self._load_json("examples.json")

    def build_messages(self, schema: dict, question: str) -> list:
        system_content = "\n\n".join(
            [
                self.system_prompt,
                self.intent_prompt,
                self.semantic_prompt,
                "",
                "IMPORTANT INSTRUCTIONS",
                "----------------------",
                "Return ONLY valid JSON.",
                "Do NOT include markdown.",
                "Do NOT wrap the JSON in triple backticks.",
                "Do NOT provide explanations.",
                "Do NOT include any text before or after the JSON.",
                "",
                "OUTPUT SCHEMA",
                json.dumps(self.output_schema, indent=4),
                "",
                "EXAMPLES",
                json.dumps(self.examples, indent=4),
            ]
        )

        user_content = (
            "The following metadata describes the available dataset.\n\n"
            "Each key represents one dataset column.\n\n"
            "Rules:\n"
            "- Use ONLY the supplied column names.\n"
            "- Never invent new column names.\n"
            "- Use unique_values for categorical matching.\n"
            "- sample_values are examples only.\n"
            "- Numeric fields contain minimum and maximum values.\n\n"
            "DATASET SCHEMA:\n\n"
            f"{json.dumps(schema, indent=4)}\n\n"
            "USER QUESTION:\n\n"
            f"{question}"
        )

        return [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]

    def _load_text(self, filename: str) -> str:
        path = self.prompt_directory / filename

        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def _load_json(self, filename: str):
        path = self.prompt_directory / filename

        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)