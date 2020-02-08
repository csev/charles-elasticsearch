# Charles Elasticsearch

## Variables

`CHARLES_POSTGRES_HOST`
- Defaults to localhost.

`CHARLES_POSTGRES_PORT`
- Defaults to 5432.

`CHARLES_POSTGRES_USER`
- The Postgres user used to connect to *CHARLES_POSTGRES_HOST*.

`CHARLES_POSTGRES_PASSWORD`
- The Postgres password used to connect to *CHARLES_POSTGRES_HOST*.

`CHARLES_AUTH_SECRET`
- The secret used to generate HTTP passwords.

`CHARLES_ELASTICSEARCH_URI`
- The Elasticsearch host URI.

## Usage

```python
from sanic import Sanic
from charles_elasticsearch import Elasticsearch

app = Sanic('elasticsearch-proxy')
app.blueprint(Elasticsearch.resource())

app.run()

```
