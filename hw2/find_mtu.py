import argparse
import socket
import subprocess

HEADER = 28
MAX_VALUE = 9200 # for Ethernet jumbo frames

parser = argparse.ArgumentParser()
parser.add_argument("host", nargs="?",default="")
args = parser.parse_args()
host = args.host

print("Checking hostname...")
if host == "":
    print("No hostname")
    exit(1)

try:
    socket.gethostbyname(host)
except socket.error:
    print("Bad hostname")
    exit(1)

print("Checking icmp is not blocked..")
answer = subprocess.run(["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
if answer.stdout == 1:
    print("Icmp is blocked")
    exit(1)
print("Icmp is not blocked")

def request(mtu):
    command = ["ping", host, "-s", str(mtu), "-c", "5"]
    answer = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if answer.returncode != 0 and answer.returncode != 1:
        print("Handle error: ", answer.stderr)
        exit(answer.returncode)
    return answer.returncode

print("Finding mtu...")
left = 0
right = MAX_VALUE + 1 - HEADER
while right - left > 1:
    middle = (right + left) // 2
    returncode = request(middle)
    if returncode == 0:
        left = middle
    elif returncode == 1:
        right = middle

print("Finded MTU is", left + HEADER)
