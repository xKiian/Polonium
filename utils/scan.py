from requests import get
from base64 import b64decode
from zlib import decompress
from re import findall

class Scan:
    def __init__(self, code) -> None:
        self.keywords       = self.get_keywords(code)
        self.urls           = self.get_urls(code)
        self.webhooks       = self.get_webhooks()
        self.invites        = self.get_invites(code)
        self.pastebin       = self.get_pastebin(code)
        self.oneliner       = self.get_oneliner(code)
        self.base64_urls    = self.get_url_from_base64(code)

        if self.base64_urls:
            self.webhooks.extend(self.base64_urls)
    
    def get_urls(self, code):
        return findall(r"http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", code)

    def get_keywords(self, code):
        keywords = [
            "token",
            "steal",
            "account",
            "passwords",
            "wallet",
            "grab",
            "send",
            "login",
            "email",
            "password",
            "secret",
            "key",
            "private",
            "public",
            "address",
            "seed",
            "mnemonic",
            "phrase",
            "pin",
            "code",
            "2fa",
            "2-factor",
            "webhook",
            "firefox",
            "opera",
            "chrome",
            "leveldb",
            "ipify",
            "appdata",
            "localappdata",
            "index.js",
            "discordcanary",
            "discordptb",
            "discord",
            "local storage",
        ]
        found = []
        for keyword in keywords:
            if keyword in code:
                found.append(keyword)
        return found

    def get_webhooks(self):
        webhooks = []
        for url in self.urls:
            if ".com/api/webhooks/" in url:
                webhooks.append(str(url))
        return webhooks

    def get_invites(self, code):
        return findall(r"discord\.com\/invite\/\w+|discord\.gg\/\w+", code)

    def get_pastebin(self, code):
        return findall(r"pastebin\.com\/raw\/\w+|pastebin\.com\/\w+", code)

    def get_oneliner(self, code):
        code = code.splitlines()
        oneliner, rats = [], []
        lline = 0
        lellines = []
        keywords = [
            "base64",
            "decode",
            "download",
            "exec",
            "curl",
            "send",
            "import",
            "compile",
        ]
        for line in code:
            lline += 1
            if " " * 70 in line:
                for keyword in keywords:
                    if keyword in line:
                        rats.append(str(lline))
                        break

                oneliner.append(str(lline))
                
        return [oneliner, rats] 

    def getwaspwebhook(self, url):
        script = get(url.replace("inject", "grab")).read().decode("utf8")
        deobfd = decompress(eval(script[script.index("b'"):script.rindex("))")])).decode()
        urls = self.get_urls(deobfd)
        return self.get_webhooks(urls)

    def get_url_from_base64(self, code):
        try:
            for line in code.splitlines():
                line = b64decode(
                    line.split("b64decode(")[1]
                    .split(")")[0]
                    .replace('"', "")
                    .replace("'", "")
                    .replace(" ", "")
                ).decode("utf-8")
                urls = self.get_urls(line) # get the urls in the new decode string
                for url in urls:
                    url = url.split("'")[0].split('"')[0].split(" ")[0].split(")")[0] # dont judge lmao
                    if "/inject" in url: # wasp
                        url = self.getwaspwebhook(url)
                        return url if url else False
                    return url
        except:return False

    def get_info(self) -> str:
        return {
            "urls"      : self.urls,
            "keywords"  : self.keywords,
            "webhooks"  : self.webhooks,
            "invites"   : self.invites,
            "pastebin"  : self.pastebin,
            "oneliner"  : self.oneliner
        }