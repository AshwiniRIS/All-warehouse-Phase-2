import gzip
import base64

with open("state.json", "rb") as f:
    compressed = gzip.compress(f.read())

encoded = base64.b64encode(compressed).decode()

print(encoded)