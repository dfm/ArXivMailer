For development, [install postgres locally](https://www.postgresql.org/),
launch postgres, and run

```
createdb arxivmail
```

to create the database.

Start a virtualenv or conda environment and install the requirements using

```
pip install -r requirements.txt
```

To create the tables, run:

```
python manage.py create
```
