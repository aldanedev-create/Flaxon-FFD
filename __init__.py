"""
Flaxon FFD -- a Flaxon plugin that bridges FastAPI, Flask, and Django apps
into a single Flaxon application via genuine ASGI-level mounting.
"""

from __future__ import annotations

from typing import Any

from flaxon.plugins import Plugin

__version__ = "0.1.0"
__all__ = ["FFDPlugin", "__version__"]


class FFDPlugin(Plugin):
    """
    Mounts one or more foreign framework apps under a running Flaxon app.

    Example:
```python
        from flaxon import Flaxon
        from flaxon_ffd import FFDPlugin
        from fastapi import FastAPI

        fastapi_app = FastAPI()

        app = Flaxon("main")
        await app.plugins.load_plugin(
            FFDPlugin(mounts={"/fastapi": fastapi_app})
        )
```

    `mounts` maps a URL prefix to any ASGI-compatible app: a FastAPI app,
    Django's `get_asgi_application()` result, or a WSGI app (Flask, older
    Django) wrapped with `a2wsgi.WSGIMiddleware`.
    """

    name = "flaxon-ffd"
    version = "0.1.0"
    description = "Bridge FastAPI, Flask, and Django apps into Flaxon via ASGI mounting."
    author = "you"
    provides = ["asgi-bridge"]

    def __init__(self, mounts: dict[str, Any]) -> None:
        self.mounts = mounts

    def setup(self, app: Any) -> None:
        for path, foreign_app in self.mounts.items():
            app.mount_asgi(path, foreign_app)

    def on_load(self) -> None:
        print(f"[flaxon-ffd] mounted: {', '.join(self.mounts.keys())}")