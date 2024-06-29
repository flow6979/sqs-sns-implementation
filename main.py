import json
import boto3
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up AWS clients
sns = boto3.client('sns', endpoint_url='http://localhost:4566')
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
accountId = '000000000000'

# Create SNS topics
sns.create_topic(Name='broadcast-topic')
sns.create_topic(Name='communication-topic')
sns.create_topic(Name='entity-topic')

# Create SQS queues
sqs.create_queue(QueueName='email-queue')
sqs.create_queue(QueueName='sms-queue')
sqs.create_queue(QueueName='entity-queue')

# Create subscriptions
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:broadcast-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:email-queue')
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:broadcast-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:sms-queue')
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:broadcast-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:entity-queue')

sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:communication-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:email-queue')
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:communication-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:sms-queue')

sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:entity-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:entity-queue')


# API endpoint to publish messages to SNS:
@app.route('/appointment/event', methods=['POST'])
def publish_message():
    data = request.get_json()
    event_type = data['event_type']
    message = data['message']

    if event_type == 'broadcast':
        sns.publish(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:broadcast-topic', Message=json.dumps({'default': json.dumps(message)}), MessageStructure='json')
    elif event_type == 'communication':
        sns.publish(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:communication-topic', Message=json.dumps({'default': json.dumps(message)}), MessageStructure='json')
    elif event_type == 'entity':
        sns.publish(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:entity-topic', Message=json.dumps({'default': json.dumps(message)}), MessageStructure='json')
    else:
        return jsonify({'error': 'Invalid event type'}), 400

    return jsonify({'message': 'Message published successfully'}), 200


# API endpoints to read messages from the SQS queues:
@app.route('/consumer/email', methods=['GET'])
def read_email_queue():
    return read_queue('email-queue')

@app.route('/consumer/sms', methods=['GET'])
def read_sms_queue():
    return read_queue('sms-queue')

@app.route('/consumer/entity', methods=['GET'])
def read_entity_queue():
    return read_queue('entity-queue')

def read_queue(queue_name):
    response = sqs.receive_message(QueueUrl=f'http://localhost:4566/{accountId}/{queue_name}')
    print(f"Received messages from '{queue_name}' queue: {response}")
    if 'Messages' in response:
        for message in response['Messages']:
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(QueueUrl=f'http://localhost:4566/{accountId}/{queue_name}', ReceiptHandle=receipt_handle)
        return jsonify(response['Messages'])
    else:
        return jsonify({'message': 'No messages in the queue'}), 200

if __name__ == '__main__':
    app.run(debug=True)
