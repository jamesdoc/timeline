import tornado.ioloop
import tornado.web
import tornado.autoreload

import json

from os import path, environ, walk
from tornado.options import define, options, parse_command_line
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

define("port", default=8080, help="run on the given port", type=int)

settings = { 'autoreload': True }


class TemplateRendering(object):

    def render_template(self, template_name, variables):
        template_dirs = []
        template_dirs.append(path.join(path.dirname(__file__), 'templates')) # added a default for fail over.
        env = Environment(loader = FileSystemLoader(template_dirs))
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(variables)
        return content


class IndexHandler(tornado.web.RequestHandler, TemplateRendering):
    def get(self):
        
        json_data=open('assets/shoes.json')
        shoes_data = json.load(json_data)
        json_data.close()
        
        data = {
            'shoes':shoes_data
        }
        
        content = self.render_template('index.html', data)
        self.write(content)


app = tornado.web.Application([
    (r'/', IndexHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

    tornado.autoreload.start()
    
    for dir, _, files in walk('templates'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
    for dir, _, files in walk('assets'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
        
    tornado.ioloop.IOLoop.instance().start()