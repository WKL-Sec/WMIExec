#To generate the required files, execute the following commands
#openssl genpkey -algorithm RSA -out server.key
#openssl req -new -key server.key -out server.csr
#openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Decode the received data
        received_data = post_data.decode('utf-8')

        # Process the received data as needed
        print(f'[+] Received data:\n{received_data}')

        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_message = 'Data received successfully'
        self.wfile.write(response_message.encode('utf-8'))

def run_server():
    host = '0.0.0.0'
    port = 8080
    server_address = (host, port)

    # Create an SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # Create the HTTPS server with the SSL context
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print(f'Starting HTTPS server on {host}:{port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

