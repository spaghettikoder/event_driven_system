import pika
import smtplib

SENDER = ''
RECEIVER = ''
PASSWORD = ''

def send_email(ch, method, properties, body):
	user, content = body.decode().split('~', 1)
	send_smtp_request(user, content)
	
def send_smtp_request(user, message):
	sender = SENDER
	receiver = RECEIVER
	email_body = f"Subject: Event-Driven System\n\nFrom user: {user}\n\nMessage: {message}"

	with smtplib.SMTP('smtp.gmail.com', 587) as server:
		server.starttls()
		server.login(sender, PASSWORD)
		server.sendmail(sender, receiver, email_body)
	

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='filtered_screamed_out_messages')
channel.basic_consume(queue='filtered_screamed_out_messages', on_message_callback=send_email, auto_ack=True)

print('publishing service is running...')
channel.start_consuming()
