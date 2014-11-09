import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import json
import urlparse



def cleanup(resp):
	obj = json.loads(resp)
	ds = obj.keys()[0]
	data = {}
	values  =  obj[ds]['value']
	index = obj[ds]['dimension'][obj[ds]['dimension']['id'][1]]['category']['index']
	labels = obj[ds]['dimension'][obj[ds]['dimension']['id'][1]]['category']['label']
	for l in labels:
		num = index[l]
		count = values[str(num)]
		data[labels[l]] = count
	return data
	
	
class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		url = "http://data.ons.gov.uk/"+self.request.uri
		http.fetch(url, self._on_download)

	def _on_download(self, response):
		print response.body
		data = cleanup(response.body)
		origin = self.request.headers.get_list('Origin')[0]
		self.set_header("Access-Control-Allow-Origin" , origin)
		self.set_header("Access-Control-Allow-Credentials", "true")
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
