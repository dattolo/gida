# gida

Gestionale acquisti/vendite per oggetti usati. Nato come pagina HTML singola che salvava su Excel,
ora è un'applicazione Django 5.2 + Django REST Framework con dati salvati nel database.

Produzione: https://gida.pythonanywhere.com

## Funzionalità

- **Accesso con login**: tutte le pagine e le API richiedono l'autenticazione. Gli utenti li crea
  l'amministratore da `/admin/`; non c'è registrazione pubblica.
- **Dati per utente**: ogni utente vede e modifica solo i propri oggetti.
- **Registro acquisti**: aggiunta di un acquisto con data, descrizione e prezzo; eliminazione.
- **Vendite**: "Vendi" registra data e prezzo di vendita; "↩" annulla la vendita e riporta
  l'oggetto in magazzino.
- **Filtri e ricerca**: per periodo, per stato (tutti / in magazzino / venduti) e per testo.
- **Indicatori**: riepilogo di spesa, incasso e utile per il periodo selezionato; utile per riga.
- **Importa Excel**: carica un file `.xlsx` aggiungendo gli oggetti a quelli esistenti oppure
  sostituendoli. L'import è tutto o niente: se una riga non è valida non viene importato nulla.
- **Scarica Excel**: backup in `.xlsx` con tre fogli: *Registro*, *Magazzino* (con giorni in
  magazzino) e *Riepilogo mensile* (acquistati, speso, venduti, incassato, utile, margine %).

### API

Tutte sotto `/api/`, autenticate con la sessione di login (CSRF richiesto).

| Metodo | Percorso | Azione |
|---|---|---|
| `GET`, `POST` | `/api/items/` | Elenco / creazione oggetti |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/api/items/<id>/` | Dettaglio / modifica / eliminazione |
| `POST` | `/api/items/<id>/vendi/` | Registra la vendita (`vendita_dt`, `prezzo_vendita`) |
| `POST` | `/api/items/<id>/annulla_vendita/` | Annulla la vendita |
| `POST` | `/api/items/import/` | Import massivo (`items`, `replace`) |

## Sviluppo locale

Requisiti: Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # imposta DJANGO_SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Test:

```bash
python manage.py test
```

### Configurazione (`.env`)

| Variabile | Descrizione |
|---|---|
| `DJANGO_SECRET_KEY` | Chiave segreta di Django |
| `DJANGO_DEBUG` | `1` in sviluppo, `0` in produzione |
| `DJANGO_ALLOWED_HOSTS` | Host ammessi, separati da virgola |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Solo produzione, es. `https://gida.pythonanywhere.com` |
| `DB_ENGINE` | `sqlite` (predefinito) o `mysql`; per MySQL anche `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_TEST_NAME` |

## Deploy (PythonAnywhere)

Da una console Bash su PythonAnywhere:

```bash
cd ~/gida && ./deploy.sh
```

Lo script esegue pull, installazione dipendenze, migrazioni, `collectstatic` e ricarica la web app.

Note sul piano gratuito: niente MySQL né task programmati, la web app va rinnovata ogni mese.
SQLite può dare "database is locked": è mitigato con `timeout` e `transaction_mode=IMMEDIATE`;
se il problema persiste, passare a un piano a pagamento con MySQL (`DB_ENGINE=mysql`).

## Changelog

### 2026-10-16
- Aggiunto questo README.

### 2026-10-15
- Aggiunte note sullo stato del progetto (`STATO.md`).
- Gli oggetti sono salvati nel database tramite API invece che nel file Excel locale; aggiunti
  import Excel (aggiungi o sostituisci, tutto o niente) e download Excel come backup.
- Script di deploy indipendente dalla regione di PythonAnywhere.
- Ottimizzazione dei lock SQLite e primo script di deploy per PythonAnywhere.
- Prima versione: scheletro Django + DRF con configurazione da `.env` e login.
