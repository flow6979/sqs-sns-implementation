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

  Copy curl from here - [doc url](https://docs.google.com/document/d/1QFIxUMpJYaDGxsjEDK_fWagJu5huBdS2mo8wcO_TmSA/edit?usp=sharing)

- Case 1: Broadcast type:
   - Publish a broadcast message:
   - Consumer messages from the email queue:
      `Message recieved`
     
   - Consumer messages from the sms queue:
      `Message recieved`
     
   - Consumer messages from the entity queue:
      `Message recieved`
 
- Case 1: Communication type:
   - Publish a communiaction message:
   - Consumer messages from the email queue:
      `Message recieved`
     
   - Consumer messages from the sms queue:
      `Message recieved`
     
   - Consumer messages from the entity queue:
      `NO Message recieved`
 
- Case 1: Entity type:
   - Publish a entity message:
   - Consumer messages from the email queue:
      `NO Message recieved`
     
   - Consumer messages from the sms queue:
      `NO Message recieved`
     
   - Consumer messages from the entity queue:
      `Message recieved`
     

## Application flow - 

![flow](https://github.com/flow6979/sqs-sns-implementation/blob/main/flow.png)
