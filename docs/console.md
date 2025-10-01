# Console (CLI)

Interactive command interpreter defined in `console.py` (`HBNBCommand`). Start it with:

```bash
python3 console.py
```

## Commands
- `create <Class> [attr=value ...]`: create instance; prints id
- `show <Class> <id>`: display instance
- `destroy <Class> <id>`: delete instance
- `all [Class]`: list all or all of Class
- `update <Class> <id> <attr> <value>`: set attribute
- `<Class>.all()`, `<Class>.count()`, `<Class>.show("id")`, `<Class>.destroy("id")`, `<Class>.update("id", {dict})` supported

Examples
```bash
(hbnb) create User email="me@example.com" password="pass123"
(hbnb) all User
(hbnb) show User 1234-5678
(hbnb) update User 1234-5678 first_name "Ada"
(hbnb) User.all()
```