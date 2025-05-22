import socket
import time
import random
import sqlite3
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432
vetCitta = ['ROMA', 'NAPOLI', 'MILANO', 'TORINO', 'FIRENZE',
            'BOLOGNA', 'VENEZIA', 'BARI', 'PALERMO', 'ANCONA']

def inizializza_temperature():
    ultime_temperature = {}
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        for citta in vetCitta:
            cursor.execute('''
                SELECT temperatura FROM meteo 
                WHERE citta = ? 
                ORDER BY orario DESC 
            ''', (citta,))
            risultato = cursor.fetchone()
            if risultato:
                ultime_temperature[citta] = risultato[0]
                print(f"Caricata temperatura iniziale per {citta}: {risultato[0]}°C")
            else:
                temperatura = round(random.uniform(15.0, 35.0), 2)
                ultime_temperature[citta] = temperatura
                print(f"Generato valore iniziale per {citta}: {temperatura}°C")
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Errore database: {e}")
        for citta in vetCitta:
            ultime_temperature[citta] = round(random.uniform(15.0, 35.0), 2)
    
    return ultime_temperature

ultime_temperature = inizializza_temperature()
citta_index = 0

def genera_dati():
    global citta_index, ultime_temperature
    citta = vetCitta[citta_index]
    citta_index = (citta_index + 1) % len(vetCitta)

    ultima_temp = ultime_temperature[citta]
    
    delta = random.uniform(-2.0, 2.0)
    nuova_temp = round(ultima_temp + delta, 2)
    
    nuova_temp = max(15.0, min(nuova_temp, 35.0))
    
    ultime_temperature[citta] = nuova_temp
    
    umidita = round(random.uniform(30.0, 90.0), 2)
    pressione = round(random.uniform(990.0, 1025.0), 2)
    orario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return f"{nuova_temp},{umidita},{pressione},{orario},{citta}"

def invia_dati():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            dati = genera_dati()
            s.sendall(dati.encode())
            print(f"Dati inviati: {dati}")
            time.sleep(10)

if __name__ == '__main__':
    invia_dati()