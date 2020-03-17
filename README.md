


Setup virtual env:

```sh
pipenv --python 3.7
pipenv install python-dotenv psycopg2-binary
pipenv shell
```


Setup env vars in a ".env" file (using creds from ElephantSQL):

```sh
DB_NAME="____________"
DB_USER="abc123"
DB_PASSWORD="abc123"
DB_HOST="abc123"
```

Run:

```sh
python app/pg_queries.py
```