from sqlalchemy.engine.url import URL

from blog_app.store.accessors.queue import QueueAccessor
from blog_app.store.database import db
from blog_app.settings import config


class Store:
    async def _db_connect(self):
        await self.db.set_bind(
            URL(
                drivername="asyncpg",
                username=config["database"]["username"],
                password=config["database"]["password"],
                host=config["database"]["host"],
                port=config["database"]["port"],
                database=config["database"]["name"],
            ),
            min_size=1,
            max_size=1,
        )

    async def _db_disconnect(self):
        await self.db.pop_bind().close()

    def __init__(self):
        self.db = db
        if config["queue"]["enabled"]:
            self.queue = QueueAccessor()
        else:
            self.queue = None

    async def connect(self, *args):
        await self._db_connect()
        if config["queue"]["enabled"]:
            await self.queue.connect()

    async def disconnect(self, *args):
        await self._db_disconnect()
        if config["queue"]["enabled"]:
            await self.queue.disconnect()
