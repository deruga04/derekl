from socket import *
from datetime import datetime
import sys
import urllib
import traceback
import random


port_number = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#server_socket.bind(('', port_number))
server_socket.bind(('', port_number))

server_socket.listen(1) # allows max of 1 connection

def get_http_response_header():
    response  = 'HTTP/1.1 200 OK\n'
    response += 'Connection: close\n'
    response += 'Date: {}\n'.format(str(datetime.now()))

    return response

def get_dir(data):
    return data.split('\n')[0].split(' ')[1].split('?')[0].replace('/', '')

def send(socket, msg):
    msg_utf = str(msg).encode('utf-8')
    socket.send(msg_utf)

def send_encoded(socket, msg):
    socket.send(msg)

def fun_home(html):
    greetings = ["Hello MTV, welcome to my crib!", "ようこそ！", "Nice to meet 'cha", "Welcome", 'Nobody expects the Spanish inquisition!']
    return html.replace('random_as_fuck_title_name', random.choice(greetings))

while True:
    print("Server is ready to receive...")
    try:
        connection_socket, addr = server_socket.accept()
        #print(connection_socket.recvfrom(1024))
        message_utf, return_address = connection_socket.recvfrom(1024)
        req = message_utf.decode('utf-8')

        dir = get_dir(req)

        if dir  == '':
            dir = 'index.html'

        print(dir)

        open_type = 'r'

        try:
            if dir.endswith('.jpg'):
                mimetype = 'image/jpg'
                open_type = 'rb'
            elif dir.endswith('.css'):
                mimetype = 'text/css'
            elif dir.endswith('.js'):
                minetype = 'application/javascript'
            elif dir.endswith('.pdf'):
                mimetype = 'application/pdf'
                open_type = 'rb'
            else:
                mimetype = 'text/html'

            myfile = open(dir, open_type)

            
            file = myfile.read()

            myfile.close()

            if dir == 'index.html':
                file = fun_home(file)

            send(connection_socket, get_http_response_header())
            send(connection_socket, 'Content-Type: ' + str(mimetype) + '\n\n')

            if dir.endswith('.pdf'):
                send_encoded(connection_socket, file)
            else:
                send(connection_socket, file)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            file = open('not_found.html', 'r')
            not_found_page = file.read()
            file.close()
            send(connection_socket, 'HTTP/1.1 404 Not Found\n\n')
            send(connection_socket, not_found_page)

        # send(connection_socket, "HTTP/1.1 200 OK")
        # send(connection_socket,'Connection: close')
        # send(connection_socket, 'Date: daskjdjkas')
        # send(connection_socket,'Content-Type: text/html; encoding=utf8')
        # send(connection_socket, '\n\n')
        # send(connection_socket, '<p>bold and brash</p>')
        connection_socket.close()
    except: 
        server_socket.close()
        print('Fucking noob')
        traceback.print_exc()
        sys.exit(0)