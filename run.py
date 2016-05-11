from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from gh_portfolio import app

app.logger.info("Starting server")
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8080)
app.logger.info("Listening on port: 8080")
IOLoop.instance().start()
