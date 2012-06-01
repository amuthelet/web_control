
import sys
import cgi
import urlparse
import commands
import shlex,subprocess
import BaseHTTPServer

DEBUG = True

class VirtualJoystickData():
    """
    Virtual Joystick data
    """

    def Init(self):
        self.deltaX = 0
        self.deltaY = 0



class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    HTTP handler performing custom GET and POST management
    """

    cgi_directories = ["./"]

    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.joystick_data = None

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)

        if parsed_path.geturl() == '/value':
            self.wfile.write(self.joystick_data.deltaX)
        else:
            f = open('.' + parsed_path.geturl())
            self.send_response(200)

            self.send_header('Content-type', 'text/html')

            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        return

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()

        self.joystick_data.deltaX = form['deltaX'].value
        self.joystick_data.deltaY = form['deltaY'].value

        # Send ack
        self.wfile.write('Server OK')
        return

class myHTTPServer(BaseHTTPServer.HTTPServer):
    """
    Custom HTTPServer
    """

    def __init__(self, server_address, RequestHandlerClass, joystick_data):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.RequestHandlerClass.joystick_data = joystick_data

def main():
    try:
        joystick_data = VirtualJoystickData()
        joystick_data.Init()
        # Start Web Server
        server = myHTTPServer(('', 8000), MyHandler, joystick_data)
        print 'Httpserver started, press <CTRL+C> to quit'
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

