import io
import zlib

import numpy as np
import requests


class TransformerClient:
    def __init__(self, host="0.0.0.0", port=5000):
        self.url = f"http://{host}:{port}/"

    def encode(self, query):
        request = {"message": query}

        response = requests.post(self.url, json=request)

        return self.uncompress_nparr(response.content)

    @staticmethod
    def uncompress_nparr(bytestring):
        return np.load(io.BytesIO(zlib.decompress(bytestring)))
