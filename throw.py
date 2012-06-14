from daemon import Daemon
import sys
import os
import urllib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler

PORT = 8000

def conf_file(mode):
	return open(os.path.expanduser('~/.throw'),mode)

class ThrowServerHandler(SimpleHTTPRequestHandler):

	def do_GET(self):
		files_raw = conf_file('r').read()
		if self.path == "/":
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

			template = open('list.html','r').read()
			content = ''
			for mfile in files_raw.split('\n'):
				if mfile:
					content += '<a href="%s"><li>%s</li></a>\n'%(urllib.quote(mfile),mfile)
			self.wfile.write(template.replace('%%content%%',content))


		elif self.path in files_raw.split('\n'):
			return SimpleHTTPRequestHandler.do_GET(self)
		else:
			self.send_response(404)
			self.send_header("Content-type", "text/html")
			self.end_headers()



class ServerDaemon(Daemon):

	def run(self):
		server_address = ('',8000)
		httpd = HTTPServer(server_address,ThrowServerHandler)
		httpd.serve_forever()

	def add_file(self,path):
		w = conf_file('a')
		w.write('%s/%s\n'%(os.getcwd(),path))
		w.close()

if __name__ == "__main__":
	daemon = ServerDaemon('/tmp/throw.pid')
        if len(sys.argv) == 2:
                if '--start' == sys.argv[1]:
                        daemon.start()
                elif '--stop' == sys.argv[1]:
                        daemon.stop()
                elif '--restart' == sys.argv[1]:
                        daemon.restart()
                elif os.path.exists(sys.argv[1]):
					daemon.add_file(sys.argv[1])
					if not daemon.is_launched():
						daemon.start()
                else:
                        print "Unknown command or file not found"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s --start|--stop|--restart" % sys.argv[0]
                sys.exit(2)