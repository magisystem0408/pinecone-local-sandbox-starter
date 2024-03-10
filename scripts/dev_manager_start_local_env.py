import os
import yaml
from pinecone import Pinecone, PodSpec

from config.main import PINECONE_API_KEY, LOCAL_GEN_CONFIG_FILE_NAME
from typing import TypedDict

from uuid import uuid4

OUTPUTFILE_PATH = f"./{LOCAL_GEN_CONFIG_FILE_NAME}.yaml"

DIMENSION = 256  # NOTE: 次元数(256次元で固定)


class _GenerationConfigYamlFilePineCone(TypedDict):
    index: str


class GenerationConfigYamlFile(TypedDict):
    pinecone: _GenerationConfigYamlFilePineCone


if __name__ == '__main__':
    # NOTE: check exist configuration file

    if os.path.exists(OUTPUTFILE_PATH):
        raise Exception(f"【Already Find {LOCAL_GEN_CONFIG_FILE_NAME} file】")

    pinecone_index_name = "local-" + str(uuid4())
    pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

    try:
        pinecone_client.create_index(
            name=pinecone_index_name,
            dimension=DIMENSION,
            metric="cosine",
            spec=PodSpec(
                environment="asia-northeast1-gcp",
                pod_type="s1.x1",
                pods=1
            )
        )

        with open(OUTPUTFILE_PATH, "w") as f:
            data: GenerationConfigYamlFile = {
                "pinecone": {
                    "index": pinecone_index_name
                }
            }
            yaml.dump(data, f, encoding='utf-8', allow_unicode=True)


    except Exception as e:
        print(str(e))
