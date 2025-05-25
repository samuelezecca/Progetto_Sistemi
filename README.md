## Progetto Sistemi – Applicazione Client/Server con Raccolta Dati Meteo in Tempo Reale.
Questa applicazione è basata su un'architettura client/server. Il client, scritto in Python, genera in tempo reale dati meteo (temperatura, umidità e pressione) per una città scelta casualmente e li invia al server, anch'esso in Python, che li memorizza in un database SQLite.
L'interfaccia web permette di esplorare questi dati attraverso grafici, mappe e tabella storica.

Architettura:Client (client.py): genera dati meteo casuali per una città tra un elenco predefinito, e li invia periodicamente al server.
Server (server.py): riceve i dati e li salva nel database SQLite (database.db).
Frontend (HTML/JS): permette la visualizzazione dei dati tramite varie pagine:
index.html: pagina introduttiva,
dashboard.html: panoramica dei dati raccolti,
mappa.html: visualizzazione delle città su mappa,
storico.html: tabella cronologica,
grafici.js: gestione grafici in tempo reale.

Dati generati:
Il client invia al server ogni pochi secondi dati come:
Temperatura (°C),
Umidità (%),
Pressione (hPa),
Città selezionata casualmente.

Come eseguire il progetto:
1. Unzippare la cartella scaricata da GitHub
2. Verifica presenza di Python:
Apri un terminale (Prompt dei comandi).
Digita: python --version
Se Python non è installato, vai su https://www.python.org/downloads/ e scaricalo.
Durante l’installazione, spunta l’opzione "Add Python to PATH".
Dopo l’installazione, ripeti il comando: python --version
per verificare che sia tutto a posto.
3. Apri la cartella del progetto:
Vai nella cartella del progetto (Progetto_Sistemi-master).
Clicca nella barra degli indirizzi in alto (di Esplora Risorse).
Scrivi cmd e premi Invio: si aprirà il terminale nel percorso giusto.
4. Avvia il server:
Nel primo terminale, scrivi: python server.py.
5. Avvia il client:
Apri un secondo terminale (ripeti i passi precedenti) e scrivi: python client.py.
6. Esplora il progetto:
Apri il browser e vai all’indirizzo: http://localhost:8080
Da qui puoi accedere a tutte le funzionalità dell’interfaccia web.

Struttura dei file:
Progetto_Sistemi-master/
├── client.py
├── server.py
├── database.db
├── index.html
├── dashboard.html
├── mappa.html
├── storico.html
├── grafici.js

Requisiti:
Windows con Python 3.x
Librerie Python standard (http.server, sqlite3, requests)
Un browser moderno (Chrome, Firefox, Edge...)
