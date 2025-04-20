from http.server import HTTPServer , BaseHTTPRequestHandler
from round_robin import get_next_server, server_list
import http.client
import json


def is_server_healthy(host,port):
    try:
        connection = http.client.HTTPConnection(host, port, timeout=3) 
        connection.request('HEAD', '/') # Send a HEAD request to check if the server is up
        response= connection.getresponse()
        return response.status == 200 #Server is healthy if it respond with 200 OK
    except Exception as e:
        print(f"Health check failed for {host}:{port} - {e}")
        return False #Server is not healthy if it does not respond with 200 OK
 

class LoadBalancer(BaseHTTPRequestHandler):
    def do_GET(self):
        # here if the user use normal load balancer then we will go to else part but if in the url we have /server_status then we will run this below code , by this we can still use our lb and also use this specific url in our backend so that we get the real time health checkup of our servers
        if self.path == '/server_status':   # this part of code is used to check the status of the servers in real time 
            server_status = {}
            for server in server_list:
                host, port = server.split(":")
                port = int(port)
                status = "healthy" if is_server_healthy(host, port) else "unhealthy"
                server_status[server] = status
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")  # Set the content type to JSON 
            self.send_header("Access-Control-Allow-Origin", "*")  # Allow CORS
            self.end_headers()
            self.wfile.write(json.dumps(server_status).encode()) # Convert the server status dictionary to JSON and send it as a response since the client is expecting a json response according to the content type we have set above

        else:

            for _ in range(len(server_list)):   
                # Get the next backend server
                backend_host, backend_port = get_next_server().split(":")
                backend_port = int(backend_port)
            
                if is_server_healthy(backend_host, backend_port):
                    try:
                        # Forward the request to the backend server
                        connection = http.client.HTTPConnection(backend_host, backend_port)
                        connection.request("GET", self.path)
                        response = connection.getresponse()

                        # Send the backend server's response back to the client
                        self.send_response(response.status)
                        for header, value in response.getheaders():
                            self.send_header(header, value)
                        self.end_headers()
                        self.wfile.write(response.read()) # Read the response body and send it to the client
                        return # Exit the loop if the request was successfully forwarded
                    except Exception as e:
                        # Handle errors (e.g., backend server is down)
                        print(f"Error forwarding request to {backend_host}:{backend_port} - {e}")

                else:
                    print("Server is not healthy, trying next server...")

        # If no servers are healthy, return a 502 error
            self.send_response(502)
            self.end_headers()
            self.wfile.write(b"Error: No healthy backend servers available")


 
if __name__ == '__main__':
    server = HTTPServer(("localhost", 8080), LoadBalancer)
    print("Server started at localhost:8080")
    server.serve_forever()

    