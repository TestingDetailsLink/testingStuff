
## Deploy instructions.

See https://github.com/TattiQ/dockerized_kafka for deployment.

## Code requirements

- requires python3.6
- requires docker host IP  specificed in the code -  see bootstrap_servers in kafka_client_sf.py
- requires salesforce creds and token

## Dependencies 

pip install -r requirements.txt

## How to run the app

Usage: kaf.py  --incoming_topic=<incoming_kafka_topic> --sf_username=<salesforce_user> --sf_pass=<salesforce_password> --sf_token=<salesforce_security_token> --outgoing_topic=<outgoing_kafka_topic>


Here is how you can get a security token in salesforce :
 - Login to your orgnistaion and Navigate to At the top navigation bar go to <your name > My Settings > Personal  >  Reset My Security Token.
 - And click on "Reset Security Token".Clicking the button invalidates your existing token. After resetting your token, It will be mail to the user mai ID
     
