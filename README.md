# Veriscript

Transform AI-generated text into human-sounding content to avoid detection

# Text Analyzer MVP

A simple tool to analyze text for AI-like patterns.

## Installation

pip install -r requirements.txt

## Usage

python main.py

## Tests

pytest -q

## Architecture

![Architecture](docs/architecture.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    A[Client Request] --> B[FastAPI Server]
    B --> C[Text Input]
    C --> D[Analysis Logic]
    D --> E[Repetition Check]
    D --> F[Burstiness Check]
    E --> G[Flagged Items]
    F --> G
    G --> H[JSON Output]
    H --> I[Client]
```

</details>
