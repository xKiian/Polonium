from .cfbypass import *

class RaiseError(Exception):
    pass

class walter:
    def __init__(
      self, 
      proxies: str = None, 
      timeout: int = None
    ):
        self.proxies = proxies
        self.timeout = timeout
        self.session = init()

    def send(
      self, 
      method: str,
      url: str, 
      headers: dict = None, 
      cookies: dict = None,
      json: dict = None, 
      data: dict = None
    ):

        try:
            resp = self.session.request(
                method=method,
                url=url,
                headers=headers,
                cookies=cookies,
                data=data,
                json=json,
                proxies=self.proxies,
                timeout=self.timeout,
            )
            return resp
        except Exception as e:
            raise RaiseError(f"error `{e}`")
