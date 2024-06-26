# llm-azure-api-embed

[![PyPI](https://img.shields.io/pypi/v/llm-azure-api-embed.svg)](https://pypi.org/project/llm-azure-api-embed/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/orangewise/llm-azure-api-embed/blob/main/LICENSE)

Create embeddings using the Azure OpenAI API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-azure-api-embed
```
## Usage

Setup your deployemnts in ``

```json
[
  {
    "deployment": "ada",
    "api_base": "https://<endpoint name>.openai.azure.com",
    "api_version": "2023-05-15",
    "api_key_name": "<your key name>"
  }
]
```

You can then use your Azure embedding models like this:

```bash
llm embed -m azure/ada -c "hello world"
```

See [the LLM embeddings documentation](https://llm.datasette.io/en/stable/embeddings/index.html) for more you can do with the tool.


## Development

### Install 

```
llm install -e .
```

Confirm installation:

```
llm plugins
```