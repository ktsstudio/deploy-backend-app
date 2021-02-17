from aiohttp import web

from blog_app.store.store import Store


class BaseView(web.View):
    @property
    def store(self) -> Store:
        return self.request.app["store"]
