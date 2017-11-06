# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf8")
import os
from tornado.ioloop import IOLoop
from tornado.log import app_log
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler
from controller import clock

define("port", default=8050, type=int, help="server listen port")
define("debug", default=True, type=bool, help="server run mode")
parse_command_line()


class IndexHandler(RequestHandler):
    def get(self):
        headers = self.request.headers
        for k, v in headers.items():
            print k, v
        greeting = self.get_argument('greeting', 'Hello')
        self.write('%s , friendly user! %s ' % (greeting, headers))

    def write_error(self, status_code, **kwargs):
        self.write('Holly Shit Error %s' % status_code)


def main():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=options.debug,
        autoescape=None
    )
    handlers = [
        (r"/", IndexHandler),
        (r"/clock", clock.DefaultHandler)
    ]

    application = Application(handlers, **settings)
    application.listen(options.port, xheaders=True)
    app_log.warning("my pi start at port: %s" % options.port)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
