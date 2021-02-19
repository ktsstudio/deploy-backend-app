from aiohttp import abc

from blog_app.post.models import Post
from blog_app.store.accessors.queue.messages import CreatePostMessage
from blog_app.store.store import Store
from blog_app.utils import now


class BaseHandler:
    def __init__(self, message, store: Store):
        self.message = message
        self.store = store

    @abc.abstractmethod
    async def handle(self):
        pass


class CreatePostHandler(BaseHandler):
    message: CreatePostMessage

    async def handle(self):
        await Post.create(
            user_id=self.message.user_id,
            created=now(),
            text=f"Created by queue: {self.message.text}",
        )

# API ---> rabbit <--> worker --> в pg создает сообщение
