![badge-img](https://img.shields.io/badge/Made%20at-%23dotastro-brightgreen.svg?style=flat)

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
