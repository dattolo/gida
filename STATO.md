# Stato del progetto gida

Ultimo aggiornamento: 15/10/2026

## Cos'è
Gestionale acquisti/vendite (ex pagina HTML singola che salvava su Excel) portato su
Django 5.2 + Django REST Framework. Accesso solo con login; utenti creati dall'admin.
Ogni utente vede solo i propri dati.

## Ambienti
| | Locale | Produzione |
|---|---|---|
| Dove | `~/gestionale-Ida/app` | https://gida.pythonanywhere.com (account `gida`, piano free) |
| Python | 3.12.15 (pyenv), venv `.venv` | virtualenv `~/.virtualenvs/gida` |
| Database | SQLite `db.sqlite3` | SQLite `~/gida/db.sqlite3` |
| Config | `.env` (non versionato, modello in `.env.example`) | `~/gida/.env` con `DJANGO_DEBUG=0` |

- Repo: `github.com/dattolo/gida` (privato). Push locale via SSH; PythonAnywhere clona via HTTPS con token in sola lettura.
- Deploy: in console Bash su PythonAnywhere `cd ~/gida && ./deploy.sh` (pull, pip, migrate, collectstatic, reload).

## Fatto
- [x] Scheletro Django + DRF, settings da `.env` (SQLite o MySQL con `DB_ENGINE`)
- [x] Login/logout (`/accounts/login/`), pagina principale protetta
- [x] Model `Item` con `owner`; API `/api/items/` (CRUD) + `vendi/`, `annulla_vendita/`, `import/`
- [x] Pagina salva tutto via API nel DB; import Excel (aggiungi o sostituisci, tutto o niente); download Excel come backup
- [x] Deploy su PythonAnywhere funzionante
- [x] Test: `python manage.py test` (10 test)

## Da fare
- [ ] Deploy del commit "Store items in the database…" su PythonAnywhere (`git pull && chmod +x deploy.sh && ./deploy.sh`) e prova nel browser (Importa, Vendi)
- [ ] Importare `gestionale_2026-10-14_21-49.xlsx` con l'utente di Ida
- [ ] Tailwind compilato al posto del CDN
- [ ] Modifica di un acquisto esistente (descrizione, prezzo, data)
- [ ] Backup del DB: il piano free non ha task programmati → oggi solo download manuale di `db.sqlite3` o "Scarica Excel"
- [ ] HSTS (`SECURE_HSTS_SECONDS`) dopo verifica HTTPS stabile

## Limiti noti
- Piano free: niente MySQL (solo account creati prima del 15/01/2026), niente task programmati, web app da rinnovare ogni mese.
- SQLite su PythonAnywhere può dare "database is locked"; mitigato con `timeout` e `transaction_mode=IMMEDIATE`. Se succede: piano a pagamento + MySQL (`DB_ENGINE=mysql` nel `.env`).
- `~/.ssh/known_hosts` locale ha una vecchia chiave GitHub per l'IP 140.82.121.3 (`ssh-keygen -R 140.82.121.3`).
