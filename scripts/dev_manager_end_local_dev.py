import os
import yaml
from pinecone import Pinecone

from config.main import PINECONE_API_KEY, LOCAL_GEN_CONFIG_FILE_NAME

OUTPUTFILE_PATH = f"./{LOCAL_GEN_CONFIG_FILE_NAME}.yaml"

if __name__ == "__main__":


    pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

    try:
        with open(OUTPUTFILE_PATH, "rb") as f:
            yaml = yaml.safe_load(f)

        pinecone_index_name = yaml['pinecone']['index']
        pinecone_client.delete_index(pinecone_index_name)
        os.remove(OUTPUTFILE_PATH)

    except Exception as e:
        print(str(e))
