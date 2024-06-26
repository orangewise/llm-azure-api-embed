from llm import EmbeddingModel
import llm
import json
import openai


def models_path():
    return llm.user_dir() / "azure-embeddings.json"


def read_models():
    azure_embeddings_path = models_path()
    if not azure_embeddings_path.exists():
        llm.user_dir().mkdir(exist_ok=True, parents=True)
        azure_embeddings_path.write_text(
            json.dumps(
                [
                    {
                        "deployment": "<deployment name>",
                        "api_base": "https://...",
                        "api_version": "2023-05-15",
                        "api_key_name": "<your azure key name>"
                    }
                ],
                indent=2,
            ),
            "utf-8",
        )
    data = json.loads(azure_embeddings_path.read_text("utf-8"))
    fixed = []
    for item in data:
        if isinstance(item, str):
            fixed.append({"deployment": item})
        else:
            fixed.append(item)
    return fixed


@llm.hookimpl
def register_embedding_models(register):
    for model in read_models():
        deployment = model["deployment"]
        needs_key = model["api_key_name"]

        register(
            AzureOpenAIEmbeddingModel(
                model_id=f"azure/{deployment}",
                deployment=deployment,
                api_base=model["api_base"],
                api_version=model["api_version"],
                needs_key=needs_key
            ),
            aliases=None,
        )


class AzureOpenAIEmbeddingModel(EmbeddingModel):
    batch_size = 100

    def __init__(self, model_id, deployment, api_base, api_version, needs_key, dimensions=None):
        self.model_id = model_id
        self.deployment = deployment
        self.api_base = api_base
        self.api_version = api_version
        self.needs_key = needs_key
        self.dimensions = dimensions

    def embed_batch(self, items):
        api_version = self.api_version
        azure_endpoint = self.api_base
        key = self.get_key()
        kwargs = {
            "input": items,
            "model": self.deployment
        }
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions
        client = openai.AzureOpenAI(
            api_key=key, api_version=api_version, azure_endpoint=azure_endpoint)
        results = client.embeddings.create(**kwargs).data
        return ([float(r) for r in result.embedding] for result in results)
