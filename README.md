
## Deploy instructions.

Search for any kafka docker:
```
docker search kafka 
```

Start the zookeeper container, give it a name, bind the container port 2181 to the host OS port so that we can access that port from the our host OS if needed:
```
docker run -d -p 2181:2181 --name zookeeper jplock/zookeeper
```

Start the Kafka Docker, name it: kafka, link it to the above Zookeeper container:
```
docker run -d --name kafka --link zookeeper:zookeeper ches/kafka
```

Get the IP addresses of the Zookeeper and the Kafka broker first. Note that these IP addresses are assigned for Docker container automatically when we started them:

```
ZK_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' zookeeper)
KAFKA_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' kafka)
```

We will issue the below command to create a topic “test” with 1 partition and replication factor 1:

```
docker run --rm ches/kafka \
> kafka-topics.sh --create --topic test --replication-factor 1 --partitions 1 --zookeeper $ZK_IP:2181
Created topic "test".
```

Issue below command to produce message to the “test” topic (The terminal will wait for our input.):
```
docker run --rm --interactive ches/kafka kafka-console-producer.sh --topic test0 --broker-list $KAFKA_IP:9092
02120152
```

## Code requirements

- requires python2.X
- requires KAFKA_IP specificed
- requires salesforce creds, in future the code will be changed to get them automatically 

## Dependencies 

 ```
 pip install simple_salesforce
 pip install pykafka
 pip install requests
 ```

## How to run the app

- Once you followed the deploy instructions mentioned above, you should have kafka and zookeeper containers vixible if you run 'docker ps' 
- 'echo ZK_IP' and 'echo KAFKA_IP' should show you the IP's of both containers assigned to them automatically
- fill in the IP of kafka container in the code in the consume_mes and kafka_prod methods e.g.  client = KafkaClient("10.13.0.4:9092")
- in sf_query method fill in the credentials and security token for salesforce  - sf = Salesforce(username='', password='', security_token='', sandbox=False, session=session)

Here is how you can get a security token in salesforce :
 - Login to your orgnistaion and Navigate to At the top navigation bar go to <your name > My Settings > Personal  >  Reset My Security Token.
 - And click on "Reset Security Token".Clicking the button invalidates your existing token. After resetting your token, It will be mail to the user mai ID
     
