# Event-Driven System

## Architecture

### Using RabbitMQ
This is an event-driven messaging system built with Flask, RabbitMQ, and SMTP. The system consists of four separate services that communicate via RabbitMQ queues: an API service that accepts messages, a filter service that filters messages, a scream service that capitalize messages, and a publishing service that sends the processed messages via email.


The system is composed of four components:
1. **API Service (`api.py`)**: A RESTful API that accepts messages and pushes them to the `messages` queue in RabbitMQ.
2. **Filter Service (`filter_service.py`)**: Consumes messages from the `messages` queue, filters out messages containing specific stop words, and pushes the valid messages to the `filtered_messages` queue.
3. **Scream Service (`screaming_service.py`)**: Consumes messages from the `filtered_messages` queue, transforms the message content to uppercase, and pushes the transformed messages to the `filtered_screamed_out_messages` queue.
4. **Publishing Service (`publish_service.py`)**: Consumes messages from the `filtered_screamed_out_messages` queue and sends them via email using SMTP.

The services work in parallel, processing messages in stages.

#### Prerequisites
- Python 3.x
- RabbitMQ server installed and running locally (`localhost` on port 15672)
- Flask for the API
- SMTP configuration (Gmail used in the example)
- `pika` for RabbitMQ messaging
- `smtplib` for email sending

#### Setup and Run

##### 1. Install Dependencies:

First, install the required Python libraries:

```bash
pip install Flask pika
```
##### 2. Configure the Email Service:

In publish_service.py, set up your own Gmail credentials in the following variables:
```
SENDER = 'your_email@gmail.com'
RECEIVER = 'receiver_email@example.com'
PASSWORD = 'your_email_password'
```

##### 3. Start RabbitMQ:

Make sure RabbitMQ is running on your local machine

##### 4. Start the services:

start the API Service:
```
python api.py
```

start the Filter Service:
```
python filter_service.py
```

start the Scream Service:
```
python screaming_service.py
```

start the Publishing Service:
```
python publish_service.py
```

##### 5. Test the System:

Make a POST request to test the system using the following command (port 5555 is assumed in the implementation)
```
curl -X POST -H "Content-Type: application/json" -d '{"user": "alias", "message": "type your message here}' http://localhost:5555/send
```


### Using Pipes-and-Filters

This is an event-driven pipeline system that processes messages in multiple stages using Flask, multiprocessing, and inter-process communication via queues. The system simulates a message publishing, filtering, transformation, and email notification workflow

#### Features
- **API Service**: Exposes a REST API to receive messages via HTTP POST.
- **Filter Service**: Filters out messages containing specific stop words.
- **Scream Service**: Transforms the filtered message to uppercase.
- **Email Service**: Sends the processed message via email.
- **Multiprocessing**: Uses Python's `multiprocessing` module for parallel processing.
  
#### Architecture

The system has the following components:
1. **API Server**: Receives incoming messages and pushes them to the message queue.
2. **Filter Service**: Filters messages based on predefined stop words.
3. **Scream Service**: Converts the message content to uppercase.
4. **Email Service**: Sends the transformed message to a predefined email address.

The services communicate through queues, with each service processing messages in parallel.

#### Prerequisites
- Python 3.x
- `Flask` for the web server
- `smtplib` for email notifications
- `multiprocessing` for concurrent execution

#### Setup and Run

##### 1. Install Dependencies:

First, install Flask using pip

```bash
pip install Flask 
```

##### 2. Configure the Email Service:

Set up the required environment variables or modify the email credentials in the code 
```
SENDER = 'your_email@gmail.com'
RECEIVER = 'receiver_email@example.com'
PASSWORD = 'your_email_password'
```

##### 3. Launch the System:

Run the following script:
```
python pipeline_system.py
```

##### 4. Test the System:

Make a POST request to test the system using the following command (port 5555 is assumed in the implementation)
```
curl -X POST -H "Content-Type: application/json" -d '{"user": "alias", "message": "type your message here}' http://localhost:5555/send
```








