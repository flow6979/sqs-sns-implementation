import json
import boto3
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# AWS clients
sns = boto3.client('sns', endpoint_url='http://localhost:4566')
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
accountId = '000000000000'

# subscriptions
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:my-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:broadcast-queue')
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:my-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:communication-queue')
sns.subscribe(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:my-topic', Protocol='sqs', Endpoint=f'arn:aws:sqs:us-east-1:{accountId}:entity-queue')

# API endpoint to publish messages to SNS:
@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    event_type = data['event_type']
    message = data['message']

    response = sns.publish(TopicArn=f'arn:aws:sns:us-east-1:{accountId}:my-topic', Message=json.dumps({'default': json.dumps(message)}), MessageStructure='json')
    print(f"Published message to '{event_type}' topic: {response}")

    return jsonify({'message': 'Message published successfully'}), 200

# API endpoints to read messages from the SQS queues:
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

@app.route('/read/broadcast', methods=['GET'])
def read_broadcast_queue():
    return read_queue('broadcast-queue')

@app.route('/read/communication', methods=['GET'])
def read_communication_queue():
    return read_queue('communication-queue')

@app.route('/read/entity', methods=['GET'])
def read_entity_queue():
    return read_queue('entity-queue')

if __name__ == '__main__':
    app.run(debug=True)
