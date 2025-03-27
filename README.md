# [alterpy](https://alterpy.t.me/)

First launch:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp -r config_example config
vim config/config.toml
vim config/telethon.toml
```

Start:

```sh
source venv/bin/activate
python3 -m alterpy
```

Migrate from .toml-based user database:
```sh
source venv/bin/activate
MIGRATED=migrated.db python3 -m utils.migrate_to_sqlite
DATABASE=users.db REFERENCE=migrated.db python3 -m utils.merge_with_backup
```

