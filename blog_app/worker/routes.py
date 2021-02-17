from blog_app.store.accessors.queue.messages import CreatePostMessage
from blog_app.worker.handlers import CreatePostHandler

routes = {CreatePostMessage: CreatePostHandler}
