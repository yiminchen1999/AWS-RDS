from flask import Flask, Response, request
from flask_cors import CORS
import json
from requests_futures.sessions import FuturesSession
import requests
import random
import time
import threading

app = Flask(__name__)
CORS(app)

session = FuturesSession()

MICROSERVICE_URLS = [
    "http://ec2-54-234-99-178.compute-1.amazonaws.com:8012/",
    "http://ec2-54-234-99-178.compute-1.amazonaws.com:8012/"

]
def synchronous_call():
    start_time = time.time()
    responses = []
    for url in MICROSERVICE_URLS:
        response_start_time = time.time()
        response = requests.get(url)
        response_end_time = time.time()
        if response.status_code == 200:
            responses.append(response.json())
            print(f"Synchronous: Received response from {url} in {response_end_time - response_start_time} seconds")
        else:
            print(f"Synchronous: Error from {url}: {response.status_code}")
    end_time = time.time()
    return end_time - start_time

def asynchronous_call():
    start_time = time.time()
    futures = [session.get(url) for url in MICROSERVICE_URLS]
    for future in futures:
        response_start_time = time.time()
        response = future.result()
        response_end_time = time.time()
        if response.status_code == 200:
            print(f"Asynchronous: Received response from {response.url} in {response_end_time - response_start_time} seconds")
        else:
            print(f"Asynchronous: Error from {response.url}: {response.status_code}")
    end_time = time.time()
    return end_time - start_time

@app.route('/compare', methods=['GET'])
def compare_calls():
    sync_times = []
    async_times = []
    for _ in range(10):
        sync_thread = threading.Thread(target=synchronous_call)
        async_thread = threading.Thread(target=asynchronous_call)

        sync_thread.start()
        async_thread.start()

        sync_thread.join()
        async_thread.join()

        sync_times.append(synchronous_call())
        async_times.append(asynchronous_call())

    result = {
        'synchronous_times': sync_times,
        'asynchronous_times': async_times,
        'average_sync_time': sum(sync_times) / len(sync_times),
        'average_async_time': sum(async_times) / len(async_times)
    }

    #  in four lines
    print("Synchronous Times:", sync_times)
    print("Asynchronous Times:", async_times)
    print("Average Synchronous Time:", sum(sync_times) / len(sync_times))
    print("Average Asynchronous Time:", sum(async_times) / len(async_times))

    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)

