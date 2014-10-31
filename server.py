import tornado.ioloop
import tornado.web
import tornado.autoreload
import os
from tornado.options import define, options, parse_command_line

define("port", default=8080, help="run on the given port", type=int)

settings = { 'autoreload': True }

clients = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


app = tornado.web.Application([
    (r'/', IndexHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

    tornado.autoreload.start()
    for dir, _, files in os.walk('templates'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]

    tornado.ioloop.IOLoop.instance().start()