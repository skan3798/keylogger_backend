# keylogger_backend

# Initial setup

## Create virtual environment
```
python3 -m venv env
source env/bin/activate
(source env/Scripts/activate if windows)
pip install -r requirements.txt
```

## Create config file
Inside app/ directory
```
vim main_cfg.json
{
    "dbHost": "db.com",
    "port": "1234",
    "sqlUser": "username",
    "sqlPass": "password",
    "dbKeyTable": "tablenameforkeys",
    "dbWordTable": "tablenameforwords",
    "db": "databasename",
    "dbRows": "(row1,row2,row3,row4)",
    "dbWordRows": "(row1,row2,row3,row4)"
}
```

