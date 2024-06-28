# sqs-sns-implementation

## TASK

- Create an API which pushes a certain message to SNS which should have 3 SQS consumers of 
following structure shown in diagram.
- Create another set APIs which reads from a consumer and returns the data published.
- Add support for following event types: 
- broadcast : should be listened by all consumers
- communication : should be listened only email & sms consumer
- entity : should be listened only by entity consumer

you can try using localstack (https://www.localstack.cloud) for simulating SNS and SQS locall

![design image](https://github.com/flow6979/sqs-sns-implementation/blob/main/design.png)


## STEPS

1. start localstack
2. setup AWS cli with LocalStack
3. start app server with `python3 main.py`
4. Test the code wit following curl -
   - Publish a broadcast message:
      </br>
     `curl -X POST -H "Content-Type: application/json" -d '{"event_type": "broadcast", "message": "This is a broadcast message"}' http://localhost:5000/publish`
   - Read messages from the broadcast queue:
      </br>
     `curl http://localhost:5000/read/broadcast`
