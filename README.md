# qpid-python-mre
Minimal Reproducible Example for the Qpid Python disconnection issue.

Two examples provided, in both getting the on_connection_error with remote_condition: `Condition('amqp:resource-limit-exceeded', 'local-idle-timeout expired')`.

Also, in both cases, even though messages get succesfully processed, they are not auto accepted.

## setup
1. create env `$ pipenv --python 3.6`
1. install dependencies `$ pipenv install --dev`
1. lift a local ActiveMQ broker running `$ docker-compose up -d`

## example 1
_Push 1 message and consume it with a 60 seconds sleep. This fails immediately after processing the message_

`$ pipenv run python main1.py`

## example 2
_Push 5 messages and consume it with 40 seconds sleeps. This fails after a few messages processed_

`$ pipenv run python main2.py`
