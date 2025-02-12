import os
import sys
import signal
import subprocess
import time
import threading
import random
from collections import deque

# Job management data structures
jobs = {}
job_counter = 1

import random  # Add this import
# User credentials (username -> password)
user_credentials = {
    "user1": "password123",
    "admin": "adminpass"
}

# Function to handle user login
def login():
    username = input("Username: ")
    password = input("Password: ")
    
    if username in user_credentials and user_credentials[username] == password:
        print("Access granted.")
        return username  # Return logged-in user
    else:
        print("Access denied.")
        return None

# Authentication before starting shell
current_user = None
while current_user is None:
    current_user = login()

# Start the shell loop after successful login
def shell():
    while True:
        try:
            command = input(f"{current_user}@shell> ")
            if command.strip() == "exit":
                break
            elif command.startswith("cat "):
                _, filename = command.split(maxsplit=1)
                if current_user == "admin" or filename == "public.txt":
                    execute_foreground(command)
                else:
                    print("Permission Denied.")
            else:
                execute_foreground(command)
        except Exception as e:
            print(f"Error: {e}")

# Function to execute commands
def execute_foreground(command):
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
    except Exception as e:
        print(f"Error executing command: {e}")

def test_round_robin():
    print("Running Round-Robin Scheduling Test...")
    round_robin_scheduling([101, 102, 103, 104], 2)
# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\nUse 'exit' to quit the shell.")
    return
def test_fifo():
    print("Running FIFO Page Replacement Test...")
    fifo_page_replacement([1, 2, 3, 1, 4, 5, 2, 3, 6], 3)

signal.signal(signal.SIGINT, signal_handler)

# Function to execute foreground commands
def execute_foreground(command):
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
    except Exception as e:
        print(f"Error executing command: {e}")

# Function to execute background commands
def execute_background(command):
    global job_counter
    process = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    jobs[job_counter] = process
    print(f"[{job_counter}] {process.pid}")
    job_counter += 1

# Function to list jobs
def list_jobs():
    for job_id, process in jobs.items():
        status = "Running" if process.poll() is None else "Stopped"
        print(f"[{job_id}] {process.pid} {status}")

# Function to bring a job to foreground
def foreground_job(job_id):
    if job_id in jobs:
        process = jobs.pop(job_id)
        os.waitpid(process.pid, 0)
    else:
        print(f"Job {job_id} not found.")

# Function to move a job to background
def background_job(job_id):
    if job_id in jobs:
        process = jobs[job_id]
        os.killpg(os.getpgid(process.pid), signal.SIGCONT)
        print(f"Job {job_id} resumed in background.")
    else:
        print(f"Job {job_id} not found.")

# Round-Robin Scheduling Simulation
def round_robin_scheduling(processes, quantum):
    queue = deque(processes)
    while queue:
        pid = queue.popleft()
        print(f"Executing process {pid} for {quantum} seconds")
        time.sleep(quantum)
        if random.choice([True, False]):
            queue.append(pid)

# Page Replacement (FIFO)
def fifo_page_replacement(pages, capacity):
    page_set = set()
    queue = deque()
    faults = 0
    
    for page in pages:
        if page not in page_set:
            if len(page_set) == capacity:
                removed = queue.popleft()
                page_set.remove(removed)
            page_set.add(page)
            queue.append(page)
            faults += 1
    print(f"Total Page Faults: {faults}")

# Shell main loop
def shell():
    while True:
        try:
            command = input("shell> ")
            if command.strip() == "exit":
                break
            elif command.startswith("bg "):
                _, job_id = command.split()
                background_job(int(job_id))
            elif command.startswith("fg "):
                _, job_id = command.split()
                foreground_job(int(job_id))
            elif command.strip() == "jobs":
                list_jobs()
            elif "&" in command:
                execute_background(command.replace("&", "").strip())
            elif command.strip() == "test_rr":
                print("Running Round-Robin Scheduling Test...")
                round_robin_scheduling([101, 102, 103, 104], 2)
            elif command.strip() == "test_fifo":
                print("Running FIFO Page Replacement Test...")
                fifo_page_replacement([1, 2, 3, 1, 4, 5, 6, 2, 1, 3], 3)
            else:
                execute_foreground(command)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    shell()
