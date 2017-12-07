"""
Used for benchmarking nodes.
Run using nohup via ssh.
"""
while true; 
do ./stress -s 20 -M 256 -m 2; 
sleep 2; done
