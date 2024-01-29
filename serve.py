from flask import Flask, request, jsonify
from multiprocessing import Process, cpu_count, Pool
import subprocess
import socket
import time

app = Flask(__name__)

def stress_cpu():
    total = 0
    for i in range(110000000):
        total += i**2
    return total

def stress_cpu_task():
    start_time = time.time()
    processes = cpu_count()
    pool = Pool(processes)
    pool.map(stress_cpu, [110000000, 110000000])
    print("time cost: ", time.time() - start_time)

@app.route('/', methods=['POST', 'GET'])
def handle_requests():
    if request.method == 'POST':
        # Handle POST request to stress CPU
        process = Process(target=stress_cpu_task)
        process.start()
        return jsonify({'message': 'CPU stress task started successfully'})
    elif request.method == 'GET':
        # Handle GET request to get private IP address
        private_ip = socket.gethostbyname(socket.gethostname())
        return jsonify({'private_ip': private_ip})
    else:
        return jsonify({'error': 'Invalid request method'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# to copy: scp -i "C:\Users\azaan\OneDrive\Desktop\Cloud Computing HW\MP2\instanceAutoScaling.pem" serve.py ubuntu@ec2-18-222-17-240.us-east-2.compute.amazonaws.com:~
