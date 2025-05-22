import socket
import threading
import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

db_path = 'database.db'
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS meteo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperatura REAL,
        umidita REAL,
        pressione REAL,
        orario TEXT,
        citta TEXT
    )
''')
conn.commit()

def gestisci_client(sock, addr):
    print(f"[TCP] Connessione da {addr}")
    with sock:
        while True:
            dati = sock.recv(1024)
            if not dati:
                break
            try:
                testo = dati.decode()
                temperatura, umidita, pressione, orario, citta = testo.split(',')
                cursor.execute('''
                    INSERT INTO meteo (temperatura, umidita, pressione, orario, citta)
                    VALUES (?, ?, ?, ?, ?)
                ''', (float(temperatura), float(umidita), float(pressione), orario, citta))
                conn.commit()
                print(f"[TCP] Salvati: {testo}")
            except Exception as e:
                print(f"[ERRORE] Dati non validi: {e}")

def avvia_server_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 65432))
        s.listen()
        print("[TCP] In ascolto su 127.0.0.1:65432")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=gestisci_client, args=(conn, addr), daemon=True).start()

class RichiestaHandler(BaseHTTPRequestHandler):
    
    
    
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            params = parse_qs(parsed.query)

            if path == '/':
                self.serve_file("index.html", "text/html")
            elif path in ['/dashboard', '/storico', '/mappa']:
                self.serve_file(f"{path.strip('/')}.html", "text/html")
            elif path == '/dati':
                self.serve_json_data(params)
            elif path == '/grafici':
                self.serve_graph_data(params)
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print(f"Errore durante l'elaborazione della richiesta: {e}")

    def serve_file(self, filename, content_type):
        try:
            with open(filename, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print(f"Errore durante il servizio del file: {e}")

    def serve_json_data(self, params):
        try:
            citta = params.get("citta", [""])[0]
            ordina = params.get("ordina", ["id"])[0]

            parsed = urlparse(self.path)

            if (
                parsed.path == '/dati' 
                and (not citta or citta == "")
                and ordina in ["", "id"]
            ):
                    query = "SELECT * FROM meteo ORDER BY orario DESC"
                    cursor.execute(query)
            else:
                valid_orders = ["temperatura", "umidita", "pressione", "orario", "citta", "id"]
                ordina = ordina if ordina in valid_orders else "id"

                if params.get("ultimi_per_citta", ["false"])[0].lower() == "true":
                    query = """
                        SELECT meteo.*
                        FROM meteo
                        WHERE meteo.orario = (
                            SELECT MAX(meteo_sub.orario)
                            FROM meteo AS meteo_sub
                            WHERE meteo_sub.citta = meteo.citta
                        )
                    """
                    cursor.execute(query)
                else:
                    query = "SELECT * FROM meteo WHERE 1 = 1"
                    val = []

                    if citta:
                        query += " AND citta = ?"
                        val.append(citta)

                    query += f" ORDER BY {ordina} DESC"
                    cursor.execute(query, val)

            righe = cursor.fetchall()
            dati = [{
                "temperatura": r[1],
                "umidita": r[2],
                "pressione": r[3],
                "orario": r[4],
                "citta": r[5]
            } for r in righe]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(dati).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print(f"Errore durante il servizio dei dati JSON: {e}")

    def serve_graph_data(self, params):
        try:
            citta = params.get("citta", [""])[0]
            query = "SELECT orario, temperatura FROM meteo"
            val = []

            if citta:
                query += " WHERE citta = ?"
                val.append(citta)

            query += " ORDER BY orario ASC"
            cursor.execute(query, val)

            righe = cursor.fetchall()
            dati = {
                "labels": [r[0] for r in righe],
                "temperatura": [r[1] for r in righe]
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(dati).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print(f"Errore durante il servizio dei dati grafico: {e}")

def avvia_server_http():
    httpd = HTTPServer(('', 8080), RichiestaHandler)
    print("[HTTP] Server web attivo su http://localhost:8080")
    httpd.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=avvia_server_tcp, daemon=True).start()
    avvia_server_http()