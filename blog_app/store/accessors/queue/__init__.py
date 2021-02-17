import json
import logging

from aio_pika import connect, IncomingMessage

from blog_app.settings import config
from blog_app.store.accessors.queue.messages import Message, MESSAGE_MAP


class QueueAccessor:
    ROUTING_KEY = "blog_app_queue"

    def __init__(self):
        self.connection = None
        self.logger = logging.getLogger(self.__class__.__name__)

    async def connect(self):
        self.connection = await connect(config["queue"]["url"])

    async def publish(self, message: Message):
        if not self.connection:
            raise ConnectionError
        channel = await self.connection.channel()
        await channel.default_exchange.publish(
            message.to_payload(), routing_key=self.ROUTING_KEY
        )

    def make_handler(self, handler):
        async def handle(incoming: IncomingMessage):
            async with incoming.process():
                try:
                    print(incoming.body)
                    data = json.loads(incoming.body.decode())
                    msg_cls = MESSAGE_MAP.get(data["type"])
                    data.pop("type")
                    message = msg_cls(**data)
                except Exception as e:
                    self.logger.exception(str(e))
                else:
                    await handler(message)

        return handle

    async def consume(self, handler):
        if not self.connection:
            raise ConnectionError

        channel = await self.connection.channel()
        queue = await channel.declare_queue(self.ROUTING_KEY, auto_delete=True)
        await queue.consume(self.make_handler(handler))

    async def disconnect(self):
        await self.connection.close()
