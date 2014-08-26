import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import json


def cleanup(data):
	obj = json.loads(data)
	hir = obj[obj.keys()[0]]["dimension"]["id"][0]
	size = len(obj[obj.keys()[0]]["dimension"][hir]['category']['index'])
	obj[obj.keys()[0]]["dimension"]["size"][0] = size
	data = json.dumps(obj)
	return data
	
class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch("http://data.ons.gov.uk/"+self.request.uri, self._on_download)

	def _on_download(self, response):
		data = cleanup(response.body)
		self.content_type = response.headers['Content-Type']
		self.write(data)
		self.finish()


def main():
	application = tornado.web.Application([(r".*", MainHandler),])
	http_server = tornado.httpserver.HTTPServer(application)
	port = int(os.environ.get("PORT", 5000))
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
