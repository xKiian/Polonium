from utils.scan import Scan
from json import loads, dumps

class Checker:
    def __init__(self, file) -> None:
        self.code       = open(file, "r", errors="ignore").read()
        self.scanned    = Scan(self.code).get_info()
        self.urls       = self.scanned["urls"]
        self.keywords   = self.scanned["keywords"]
        self.webhooks   = self.scanned["webhooks"]
        self.invites    = self.scanned["invites"]
        self.pastebin   = self.scanned["pastebin"]
        self.oneliner   = self.scanned["oneliner"]

        print(f"URLs: {self.urls}")

if __name__ == "__main__":
    file = input("File: ").strip("'").strip('"')
    Checker(file)