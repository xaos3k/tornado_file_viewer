# -*- coding: utf-8 -*-
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sys

#from subprocess import call
from tornado import autoreload

from tornado.options import define, options
define("port", default=8081, help="run on the given port", type=int)

filefolder = './files/'


class IndexHandler(tornado.web.RequestHandler):

    def get(self):

        filelist = []
        filesizelist = []
        files = [f for f in os.listdir(filefolder)]
#        files = [f for f in os.listdir(filefolder) if os.path.isfile(f)]
        for f in files:
            filelist.append(f)

        for item in files:
            filesize = (os.path.getsize(filefolder + item) / 1024) / 1024
            filesizelist.append(filesize)

        st = os.statvfs('/')
        freediskspace = ((st.f_bavail * st.f_frsize) / 1024) / 1024
        self.render('index.html', fili=filelist, fisili=filesizelist,
            free=freediskspace, )

    def post(self):
        delfile = self.request.arguments['file']
        for item in delfile:
            os.remove(filefolder + item)
            print "deleted file: " + item
        self.render('delete.html', delfile=delfile)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(

        handlers=[(r'/', IndexHandler)],

        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    ioloop.start()
