from blog_app.store.accessors.queue.messages import MessageType
from blog_app.worker.handlers import CreatePostHandler

routes = {MessageType.create_post: CreatePostHandler}
