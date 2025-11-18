## Como rodar?
```bash
git clone <repo-url>
cd code/server
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned (se precisar)
./venv/Scripts/activate ou source venv/bin/activate
pip install -r requirements.txt
python -m src.app.main
```

Sempre lembrar de deletar o database quando forem feitas modificações na modelagem