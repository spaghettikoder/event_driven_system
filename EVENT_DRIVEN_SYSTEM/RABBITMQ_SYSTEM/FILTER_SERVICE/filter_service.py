import pika

def filter_the_message(ch, method, properties, body):
	message = body.decode()
	user, content = message.split('~', 1)
	stop_words = ['mango', 'bird-watching', 'ailurophobia'] # mango first as it's delicious
	# if messages' content has any stop word, end the function
	for word in content:
		if word in stop_words:
			return
	push_to_filtered_messages_queue(message)
	
def push_to_filtered_messages_queue(message):
	connection_params = pika.ConnectionParameters('localhost')
	connection = pika.BlockingConnection(connection_params)
	channel = connection.channel()
	channel.queue_declare(queue='filtered_messages') # the filtered messages queue
	channel.basic_publish(exchange='', routing_key='filtered_messages', body=message) # exchange will be 'direct' by default
	connection.close()
	
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='messages')
channel.basic_consume(queue='messages', on_message_callback=filter_the_message, auto_ack=True)

print('filtering service is running...')
channel.start_consuming()
