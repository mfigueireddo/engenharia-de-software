## Como rodar?
```bash
cd code/server
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned # Caso necessário
./venv/Scripts/activate # ou source venv/bin/activate
pip install -r requirements.txt
python -m src.app.main
```