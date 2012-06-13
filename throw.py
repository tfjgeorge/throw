from daemon import Daemon
import sys
import os
import urllib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

def conf_file(mode):
	return open(os.path.expanduser('~/.throw'),mode)

class ThrowServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == "/":
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

			files_raw = conf_file('r').read()
			
			for mfile in files_raw.split('\n'):
				if mfile:
					self.wfile.write('<a href="%s">%s</a>\n'%(urllib.quote(mfile),mfile))
		else:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

			f = open(self.path,'r')
			self.wfile.write(f.read())
			self.wfile.close()

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
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        elif len(sys.argv) == 3:
        	if 'add' == sys.argv[1]:
        		daemon.add_file(sys.argv[2])
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)