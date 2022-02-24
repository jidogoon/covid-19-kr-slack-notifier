import os


class FileReader:
    def __init__(self, file_path: str, default_value: str = None):
        self.file_path = file_path
        self.default_value = default_value

    def read(self) -> str:
        if os.path.exists(self.file_path) is False:
            return self.default_value

        with open(self.file_path, 'r', encoding='utf-8') as f:
            result = f.read().strip()
            f.close()
            return result

    def read_lines(self) -> [str]:
        return (self.read() or '').split('\n')


class FileWriter:
    def __init__(self, file_path: str, data: str):
        self.file_path = file_path
        self.data = data

    def write(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.data)
            f.close()
