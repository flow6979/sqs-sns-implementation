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
     ![aws configurations](https://github.com/flow6979/sqs-sns-implementation/blob/main/awsConfigure.png)
4. start app server with `python3 main.py`
5. Test the code wit following curl -

- Case 1: Broadcast type:
   - Publish a broadcast message:
      </br>
     `curl -X POST \
       http://localhost:5000/appointment/event \
       -H 'Content-Type: application/json' \
       -d '{
         "event_type": "broadcast",
         "message": "This is a broadcast message."
       }'`
   - Consumer messages from the email queue:
      </br>
     `curl http://localhost:5000/consumer/email`
      </br>
      `Message recieved`
     
   - Consumer messages from the sms queue:
      </br>
     `curl http://localhost:5000/consumer/sms`
      </br>
      `Message recieved`
     
   - Consumer messages from the entity queue:
      </br>
     `curl http://localhost:5000/consumer/entity`
      </br>
      `Message recieved`
 
- Case 1: Communication type:
   - Publish a communiaction message:
      </br>
     `curl -X POST \
       http://localhost:5000/appointment/event \
       -H 'Content-Type: application/json' \
       -d '{
         "event_type": "communication",
         "message": "This is a communication message."
       }'`
     
   - Consumer messages from the email queue:
      </br>
     `curl http://localhost:5000/consumer/email`
      </br>
      `Message recieved`
     
   - Consumer messages from the sms queue:
      </br>
     `curl http://localhost:5000/consumer/sms`
      </br>
      `Message recieved`
     
   - Consumer messages from the entity queue:
      </br>
     `curl http://localhost:5000/consumer/entity`
      </br>
      `NO Message recieved`
 
- Case 1: Entity type:
   - Publish a entity message:
      </br>
     `curl -X POST \
       http://localhost:5000/appointment/event \
       -H 'Content-Type: application/json' \
       -d '{
         "event_type": "entity",
         "message": "This is a entity message."
       }'`
     
   - Consumer messages from the email queue:
      </br>
     `curl http://localhost:5000/consumer/email`
      </br>
      `NO Message recieved`
     
   - Consumer messages from the sms queue:
      </br>
     `curl http://localhost:5000/consumer/sms`
      </br>
      `NO Message recieved`
     
   - Consumer messages from the entity queue:
      </br>
     `curl http://localhost:5000/consumer/entity`
      </br>
      `Message recieved`
     

     ![curl Results](https://github.com/flow6979/sqs-sns-implementation/blob/main/curlResults.png)

## Application flow - 

![flow](https://github.com/flow6979/sqs-sns-implementation/blob/main/flow.png)
