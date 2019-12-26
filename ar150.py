#!/usr/bin/env python

import requests
import sys
import socket
import threading
import time
import traceback

TARGET_IP = "192.168.1.1"
UDP_PORT = 6666

class ReceiverThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.bind(("0.0.0.0", UDP_PORT))
        self.sock.settimeout(5)
        self.running = True
        self.in_buffer = ""

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                self.in_buffer += data.decode("utf-8") 
            except socket.timeout:
                pass

rx = ReceiverThread()
rx.start()

try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    while True:
        print("Waiting for node to boot into uboot console...")
        
        while rx.in_buffer[-7:] != "uboot> ":
            sock.sendto("\r\n".encode(), (TARGET_IP, UDP_PORT))
            time.sleep(1)
            sys.stdout.write(".")
            sys.stdout.flush()

        rx.in_buffer = ""

        print("")
        sock.sendto("httpd\r\n".encode(), (TARGET_IP, UDP_PORT))

        # HTTPD starts
        print("Starting HTTPD...")
        time.sleep(1)

        # POST the firmware file to it
        requests.post("http://192.168.1.1/", files={ "firmware": open(sys.argv[1],"rb") })

        print("Flashing the node...")
        idx = 0
        while True:
            x = len(rx.in_buffer)
            #sys.stdout.write(rx.in_buffer[idx:x])
            #sys.stdout.flush()
            idx = x
            if rx.in_buffer.find("Resetting the board...") > -1:
                break
        print("Resetting the node...")
        print("==== NEXT NODE PLEASE! ====")
except:
    traceback.print_exc()
    rx.stop()
