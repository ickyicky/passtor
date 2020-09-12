import json


class Storage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch(self, key: str) -> bytes:
        with open(self.file_path) as f:
            return json.load(f)[key].encode()

    def store(self, key: str, data: bytes) -> None:
        full_data = {}

        try:
            with open(self.file_path) as f:
                full_data = json.load(f)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass

        full_data[key] = data.decode()
        with open(self.file_path, "w") as f:
            json.dump(full_data, f)
