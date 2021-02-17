import asyncio
import logging

from blog_app.store.accessors.queue import Message
from blog_app.store.store import Store
from blog_app.worker.routes import routes

logger = logging.getLogger(__name__)


class MessageWorker:
    def __init__(self):
        self.store = Store()

    async def handle_message(self, msg: Message):
        try:
            await routes[msg.type](msg, self.store).handle()
        except Exception as e:
            logger.exception(str(e))

    async def run(self):
        await self.store.connect()
        await self.store.queue.consume(self.handle_message)
        logger.info("START CONSUME QUEUE")


def run_worker():
    loop = asyncio.get_event_loop()
    worker = MessageWorker()
    loop.create_task(worker.run())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("EXIT")
