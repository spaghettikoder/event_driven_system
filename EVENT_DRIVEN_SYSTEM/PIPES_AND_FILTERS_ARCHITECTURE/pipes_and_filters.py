from flask import Flask, request
from multiprocessing import Queue, Process
import smtplib

SENDER = ''
RECEIVER = ''
PASSWORD = ''

# queues for inter-process communication
messages_queue = Queue()
filtered_queue = Queue()
screamed_queue = Queue()

# API Service
def api_server(queue):
    server = Flask(__name__)

    @server.route('/send', methods=['POST'])
    def publish_message():
        data = request.json
        user = data['user']
        message = data['message']
        queue.put(f'{user}~{message}')
        return 'message has been published\n'

    server.run(port=5555)

# Filter Service
def filter_service(input_queue, output_queue):
    stop_words = ['mango', 'bird-watching', 'ailurophobia'] # mango first because it's delicious
    while True:
        message = input_queue.get()
        if message is None:
            break
        user, content = message.split('~', 1)
        if not any(word in content for word in stop_words):
            output_queue.put(message)

# Scream Service
def scream_service(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if message is None:
            break
        user, content = message.split('~', 1)
        screamed_message = f'{user}~{content.upper()}'
        output_queue.put(screamed_message)

# Email Service

def email_service(input_queue):
    while True:
        message = input_queue.get()
        if message is None:
            break
        user, content = message.split('~', 1)
        send_email(user, content)

def send_email(user, message):
    email_body = f"Subject: Event-Driven System\n\nFrom user: {user}\n\nMessage: {message}"
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, email_body)

# Shutdown Management
def stop_all_processes(processes, queues):
    for queue in queues:
        queue.put(None)
    for process in processes:
        process.join()

if __name__ == '__main__':
    # start all the processes
    api_process = Process(target=api_server, args=(messages_queue,))
    filter_process = Process(target=filter_service, args=(messages_queue, filtered_queue))
    scream_process = Process(target=scream_service, args=(filtered_queue, screamed_queue))
    email_process = Process(target=email_service, args=(screamed_queue,))

    processes = [api_process, filter_process, scream_process, email_process]
    queues = [messages_queue, filtered_queue, screamed_queue]

    for process in processes:
        process.start()

    print("pipeline system is running...")

    # graceful shutdown
    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("\nshutting down...")
        stop_all_processes(processes, queues)
        print("system has been stopped\n")

