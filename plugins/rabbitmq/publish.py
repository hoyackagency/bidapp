import json
import pika
from django.conf import settings


class RabbitMQPublisher:
    
    def __init__(self):
        print ("RabbtMQ : ", settings.MQ_HOST, settings.MQ_USER, settings.MQ_PASS)
        try:
            credentials = pika.PlainCredentials(settings.MQ_USER, settings.MQ_PASS)
            parameters = pika.ConnectionParameters(settings.MQ_HOST, credentials=credentials)        
            self.connection = pika.BlockingConnection(parameters)
            
            run_channel = self.connection.channel()
            run_channel.queue_declare(
                queue=settings.RUN_QUEUE,
                durable=True)
            self.run_channel = run_channel

            kill_channel = self.connection.channel()
            kill_channel.exchange_declare(
                exchange=settings.EXCHANGE_KILL,
                exchange_type="direct",
                passive=False,
                durable=True,
                auto_delete=False)
            self.kill_channel = kill_channel
            print ("RabbitMQ connected :", settings.MQ_HOST, settings.MQ_USER)
        except:
            print ("Failed to connect RabbitMQ :", settings.MQ_HOST, settings.MQ_USER)
            pass

        
    def __del__(self): 
        self.connection.close()
        

    def publish_run_command(self, command):
        if settings.DEBUG:
            print ("Sending run message :", command)
            
        sent = False
        
        try:
            self.run_channel.basic_publish(
                exchange='',
                routing_key=settings.RUN_QUEUE,
                body=json.dumps(command),
                properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)
            )
            sent = True
        except:
            pass


    def publish_control_command(self, command):
        if settings.DEBUG:
            print ("Sending control message :", command)
        
        sent = False
        
        try:
            self.kill_channel.basic_publish(
                exchange=settings.EXCHANGE_KILL,
                routing_key=settings.EXCHANGE_KILL_KEY,
                body=json.dumps(command),
                properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)
            )
            sent = True
        except:
            pass

    
if __name__ == "__main__":
    publisher = RabbitMQPublisher()
    
    for i in range(20):
        publisher.publish_run_command()
        publisher.publish_control_command()
