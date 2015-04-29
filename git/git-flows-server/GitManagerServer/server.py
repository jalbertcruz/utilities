#
# Author José Albert Cruz Almaguer <jalbertcruz@gmail.com>
# Copyright 2015 by José Albert Cruz Almaguer.
#
# This program is licensed to you under the terms of version 3 of the
# GNU Affero General Public License. This program is distributed WITHOUT
# ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING THOSE OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. Please refer to the
# AGPL (http:www.gnu.org/licenses/agpl-3.0.txt) for more details.

import tornado

import json
import subprocess
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket as ws
from tornado.options import define, options


class TornadoGitControllerServer:
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.render(
                "index.html"
            )

    class CommandHandler(ws.WebSocketHandler):
        def open(self):
            print("WebSocket opened")

        def on_message(self, message):
            obj = json.loads(message)
            if obj["close"]:
                tornado.ioloop.IOLoop.instance().stop()
            else:
                cmd = obj['command']
                new_dir = obj['newDir']
                current_dir = os.getcwd()
                os.chdir(new_dir)
                cmd = eval(cmd)
                subprocess.call(cmd, stdout=open(current_dir + "/stdout", "w"),
                                stderr=open(current_dir + "/stderr", "w"), shell=True)
                ok = "\n".join(open(current_dir + "/stdout").readlines())
                error = "\n".join(open(current_dir + "/stderr").readlines())
                os.chdir(current_dir)
                os.remove("stdout")
                os.remove("stderr")
                self.write_message(json.dumps({"ok": ok, "err": error}))

        def on_close(self):
            print("WebSocket closed")

    def __init__(self):
        self.app = None

    def start(self, port):
        self.app = tornado.web.Application(
            handlers=[(r"/command", self.CommandHandler), (r"/", self.MainHandler)],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True
        )
        http_server = tornado.httpserver.HTTPServer(self.app)
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()

    @staticmethod
    def stop():
        tornado.ioloop.IOLoop.instance().stop()