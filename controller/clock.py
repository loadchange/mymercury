# coding=utf-8
from tornado.gen import coroutine
from base import BaseHandler
from saksha import sakshat


class DefaultHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        self.finish({'success': 'ok'})
