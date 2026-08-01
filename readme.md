# Flaxon FFD


 <p align="center">
  <img src="https://raw.githubusercontent.com/aldanedev-create/Flaxon-Backend-Framework/main/assets/flaxon.png" alt="flaxon Logo"
   width="200"/>
</p>


  
  <p align="center">
  <a href="https://pypi.org/project/flaxon/"><img src="https://img.shields.io/pypi/v/flaxon.svg" alt="PyPI version"></a>
  <a href="https://github.com/aldanedev-create/Flaxon-Backend-Framework/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/code%20style-ruff-000000.svg" alt="Code style: ruff"></a>
</p>



**Bridge FastAPI, Flask, and Django apps into a single Flaxon application via ASGI mounting.**

Flaxon FFD is a [Flaxon](https://github.com/aldanedev-create/Flaxon-Backend-Framework) plugin that lets you run real, unmodified FastAPI, Flask, or Django apps side-by-side with your Flaxon app in the same process — useful for gradual migrations, reusing an existing service, or pulling in a framework-specific tool (like Django's admin, or FastAPI's auto-generated docs) without rewriting it.

```python
from flaxon import Flaxon
from flaxon_ffd import FFDPlugin
from fastapi import FastAPI

fastapi_app = FastAPI()

@fastapi_app.get("/hello")
def hello():
    return {"hello": "world"}

app = Flaxon("main")
await app.plugins.load_plugin(FFDPlugin(mounts={"/fastapi": fastapi_app}))
```

`GET /fastapi/hello` now hits your real FastAPI route — including FastAPI's own path converters, dependency injection, and auto-generated `/fastapi/docs` Swagger UI, completely unmodified.

## How it works

Under the hood this uses `app.mount_asgi(path, foreign_app)` — for any request under that path prefix, Flaxon hands the raw ASGI call straight to the mounted app's own `__call__`, bypassing Flaxon's routing and middleware for that subtree entirely. The mounted app handles everything itself, exactly as if it were running on its own.

**What this is:** running multiple independent apps together in one process, each on its own URL prefix.
**What this isn't:** a way to use Flask/FastAPI/Django *extensions* as if they were native Flaxon plugins. A Flask extension mounted this way still only works inside that mounted Flask app — it doesn't become available to your Flaxon routes.

## Installation

```bash
pip install flaxon-ffd[fastapi]      # for FastAPI
pip install flaxon-ffd[flask]        # for Flask (includes a2wsgi)
pip install flaxon-ffd[django]       # for Django
pip install flaxon-ffd[all]          # all three
```

## Mounting Flask or older Django (WSGI apps)

FastAPI and Django's `get_asgi_application()` are already ASGI — mount them directly. Flask (and WSGI-only Django setups) need translating first, via [a2wsgi](https://pypi.org/project/a2wsgi/):

```python
from flask import Flask
from a2wsgi import WSGIMiddleware

flask_app = Flask(__name__)

@flask_app.route("/hello")
def hello():
    return {"hello": "world"}

app.plugins.load_plugin(FFDPlugin(mounts={
    "/flask": WSGIMiddleware(flask_app),
}))
```

## Mounting Django

```python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
from django.core.asgi import get_asgi_application

django_app = get_asgi_application()

app.plugins.load_plugin(FFDPlugin(mounts={
    "/django": django_app,
}))
```

## Multiple mounts at once

```python
app.plugins.load_plugin(FFDPlugin(mounts={
    "/fastapi": fastapi_app,
    "/flask": WSGIMiddleware(flask_app),
    "/django": django_app,
}))
```

## Requirements

- Flaxon >= 0.1.9
- Python >= 3.11

## License

MIT