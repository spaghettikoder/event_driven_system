import pika
from flask import Flask, request

server = Flask(__name__)

def push_to_messages_queue(message):
	connection_params = pika.ConnectionParameters('localhost')
	connection = pika.BlockingConnection(connection_params)
	channel = connection.channel()
	channel.queue_declare(queue='messages') # the messages queue
	channel.basic_publish(exchange='', routing_key='messages', body=message) # exchange will be 'direct' by default
	connection.close()
	
@server.route('/send', methods=['POST'])
def publish_message():
	data = request.json
	user = data['user']
	message = data['message']
	push_to_messages_queue(f'{user}~{message}')
	response = 'message has been published\n'
	return response
	
if __name__ == '__main__':
	server.run(port=5555)
	

