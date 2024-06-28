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

![design image]()
