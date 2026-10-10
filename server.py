"""
Запуск трекера на компьютере.

    python server.py

Откроется браузер с приложением. Чтобы открыть его с телефона,
подключите телефон к тому же Wi-Fi и введите адрес, который
появится в консоли (http://192.168.x.x:8000).
Остановить сервер: Ctrl + C.
"""
import http.server
import os
import socket
import socketserver
import webbrowser

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".js": "application/javascript",
        ".mjs": "application/javascript",
        ".svg": "image/svg+xml",
    }

    def end_headers(self):
        # чтобы после обновления файлов браузер подхватывал новую версию
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, *args):
        pass  # не засоряем консоль


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with Server(("0.0.0.0", PORT), Handler) as httpd:
        print("Трекер запущен.")
        print(f"  На этом компьютере:  http://localhost:{PORT}")
        print(f"  С телефона (тот же Wi-Fi):  http://{lan_ip()}:{PORT}")
        print("Остановить: Ctrl + C")
        webbrowser.open(f"http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nОстановлено.")
