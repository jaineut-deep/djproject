import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple
from urllib.parse import parse_qs

hostName: str = "localhost"
serverPort: int = 8080
path_data_page: str = os.path.dirname(os.path.dirname(__file__)) + "/web/contacts.html"


class MyServer(BaseHTTPRequestHandler):
    """Класс, отвечающий за обработку входящих запросов от клиентов"""

    def __get_contacts(self) -> str:
        """Метод, возвращающий содержание стартовой html-страницы веб-сервиса в виде строки"""

        with open(path_data_page, "r", encoding="utf-8") as contacts:
            content = contacts.read()
        return content

    def do_GET(self) -> None:
        """Метод для обработки входящих GET-запросов"""

        page_content = self.__get_contacts()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))

    def do_POST(self) -> None:
        """Метод для обработки входящих POST-запросов и печати в консоль всех введенных пользователем данных"""

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = b"POST request received with data: " + post_data
        self.wfile.write(response)
        body_post = parse_qs(post_data.decode("utf-8"))
        print(body_post)


if __name__ == "__main__":
    server_address: Tuple[str, int] = (hostName, serverPort)
    webServer = HTTPServer(server_address, MyServer)  # type: ignore[arg-type]
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
