from http.server import HTTPServer, BaseHTTPRequestHandler

class NeuralHTTP(BaseHTTPRequestHandler):
    number_request = 0
#this below function is used to handle the GET request from the client
    def do_GET(self):
        self.send_response(200)                                  #this will send the responce code 200 to the client that says server is ok
        self.send_header('content-type', 'text/html')            #this will send the header to the client that says content type is text/html
        self.send_header('Access-Control-Allow-Origin', '*')     #this will allow CORS and will allow the client to access the server from any our frontend
        self.end_headers()                                       #this will end the header and send it to the client
        NeuralHTTP.number_request += 1                           
        responce_message = f"Hello from server 3 You are the {NeuralHTTP.number_request}th visitor to this server."
        self.wfile.write(responce_message.encode())                     

#It's a method that handles preflight requests. When the browser sees: You're requesting from a different port Or you're using certain headers (like Content-Type) Then before making the actual GET/POST, it sends an OPTIONS request to ask: “Hey server, is it okay if I send a GET request from a different origin?”
#This is called a preflight request. And Python’s default HTTP server doesn’t handle it unless we write do_OPTIONS ourselves.

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')         # here the * mean what we allow request from any origin to contact us 
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


    def do_HEAD(self):
        self.send_response(200)                                  #this will send the responce code 200 to the client that says server is ok
        self.send_header('content-type', 'text/html')            #this will send the header to the client that says content type is text/html
        self.end_headers()  

    #the following code will ensure that the server will run only if this file is run directly and not imported as a module
if __name__ == '__main__':
    server = HTTPServer(("localhost" , 8003), NeuralHTTP)                #this will create a server object that will listen to the localhost and port number
    print("Server is running at http://localhost:8003")          #this will print the message that server is running at localhost and port number
    server.serve_forever()                                   #this will run the server forever until it is stopped manually