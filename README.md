# ORIX POC- New


Codebase analysis:

- Prompts and data extraction schema are at [`server/utils/prompt.py`](./server/utils/prompt.py)
- LLM request logic is at [`server/services/openai_request.py`](./server/services/openai_request.py)

What needs to be done?

- Generalize this logic to ensure we can support Microsoft Phi-4 as well as OpenAI GPT 4o
- Also try out Meta LLama 3.3 70B if possible
- Use structured data extraction using function calling
    - This has already been tried in [this demo video](https://youtu.be/OcZSS37SUCE?si=3IFJe3hIIahtK5nd&t=714) with Phi-4
- Mock out everything else that doesn't matter- Azure Cosmos DB, AWS S3, etc
- We only need to test the LLM inference part