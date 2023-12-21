from flask import Flask, Response, request
from flask_cors import CORS
import json
from requests_futures.sessions import FuturesSession
import requests
import random
import time
import threading



session = FuturesSession()

# microservices URLs
MICROSERVICE_URLS = [
    "http://ec2-54-234-99-178.compute-1.amazonaws.com:8012/",
    "http://ec2-54-234-99-178.compute-1.amazonaws.com:8012/"

]


def synchronous_call():
    start_time = time.time()
    responses = []
    for url in MICROSERVICE_URLS:
        response = requests.get(url)
        if response.status_code == 200:
            responses.append(response.json())
    end_time = time.time()
    return end_time - start_time

def asynchronous_call():
    start_time = time.time()
    futures = [session.get(url) for url in MICROSERVICE_URLS]
    for future in futures:
        response = future.result()
        if response.status_code != 200:
            pass  # Handle error
    end_time = time.time()
    return end_time - start_time


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

    # Printing the result in four lines
    print("Synchronous Times:", sync_times)
    print("Asynchronous Times:", async_times)
    print("Average Synchronous Time:", sum(sync_times) / len(sync_times))
    print("Average Asynchronous Time:", sum(async_times) / len(async_times))

    return json.dumps(result)

compare_calls()