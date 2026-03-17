import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple

hostName: str = "localhost"
serverPort: int = 8080
path_data_page: str = os.path.dirname(os.path.dirname(__file__)) + "/web/contacts.html"


class MyServer(BaseHTTPRequestHandler):

    def __get_contacts(self) -> str:
        with open(path_data_page, "r", encoding="utf-8") as contacts:
            content = contacts.read()
        return content

    def do_GET(self) -> None:
        page_content = self.__get_contacts()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))


if __name__ == "__main__":
    server_address: Tuple[str, int] = (hostName, serverPort)
    webServer = HTTPServer(server_address, MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
