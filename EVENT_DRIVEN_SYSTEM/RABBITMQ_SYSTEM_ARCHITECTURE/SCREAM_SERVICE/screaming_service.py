import pika

def scream_out_the_message(ch, method, properties, body):
	user, content = body.decode().split('~', 1)
	screamed_out_message = f'{user}~{content.upper()}'
	push_to_filtered_screamed_out_messages(screamed_out_message)
	
def push_to_filtered_screamed_out_messages(message):
	connection_params = pika.ConnectionParameters('localhost')
	connection = pika.BlockingConnection(connection_params)
	channel = connection.channel()
	channel.queue_declare(queue='filtered_screamed_out_messages') # the filtered messages queue
	channel.basic_publish(exchange='', routing_key='filtered_screamed_out_messages', body=message) # exchange will be 'direct' by default
	connection.close()
	
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='filtered_messages')
channel.basic_consume(queue='filtered_messages', on_message_callback=scream_out_the_message, auto_ack=True)

print('screaming-out service is running...')
channel.start_consuming()
