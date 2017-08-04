from simple_salesforce import Salesforce
from kafka import KafkaConsumer
from kafka import KafkaProducer
import requests
import sys
import getopt
import datetime
from functools import reduce


def consume_mes(incoming_topic_name):
    """
    :param incoming_topic_name:
    :return:
    """
    consumer = KafkaConsumer(incoming_topic_name, bootstrap_servers=['172.17.13.27:9092'], auto_offset_reset='earliest',
                             enable_auto_commit=False, consumer_timeout_ms=1000)
    lst = []
    for message in consumer:
        lst.append(f"{message.value.decode('utf-8')}")
    #print(lst)
    return lst


def sf_query(lst, creds):
    session = requests.Session()
    sf = Salesforce(username=creds.get("username"), password=creds.get("password"),
                    security_token=creds.get("security_token"),
                    sandbox=False, session=session)
    force_out = []
    list_results = []
    for i in lst:
        res = sf.query("SELECT Account.Name, CaseNumber FROM Case WHERE CaseNumber = '%s'" % i)
        if res:
            list_results = [[record['Account']['Name'], record['CaseNumber']] for record in res['records']]
        force_out.append(list_results)
    #print(force_out)
    return force_out


def kafka_prod(force_out, outgoing_topic_name):
    producer = KafkaProducer(bootstrap_servers=['172.17.13.27:9092'])
    res = reduce(lambda x, y: x + y, force_out)
    for i in res:
        print(i)
        producer.send(outgoing_topic_name, key=i[1].encode(), value=i[0].encode())

    producer.flush()


def main(argv):
    args_keys = ["incoming_topic=", "sf_username=", "sf_pass=", "sf_token=", "outgoing_topic="]
    args_usage_message = "Usage: kaf.py " \
                         " --incoming_topic=<incoming_kafka_topic> " \
                         "--sf_username=<salesforce_user> " \
                         "--sf_pass=<salesforce_password> " \
                         "--sf_token=<salesforce_security_token> " \
                         "--outgoing_topic=<outgoing_kafka_topic>"

    try:
        opts, args = getopt.getopt(argv, None, args_keys)
    except getopt.GetoptError:
        print(args_usage_message)
        sys.exit(2)

    if len(opts) <= 1:
        print(args_usage_message)
        sys.exit(2)

    safe_args = {k: v for k, v in opts}
    print("[{0}] kaf.py: Started with arguments {1}".format(datetime.time(), safe_args))
    creds = {'username': safe_args.get("--sf_username"), 'password': safe_args.get("--sf_pass"),
             'security_token': safe_args.get("--sf_token")}

    cases_to_lookup = consume_mes(incoming_topic_name=safe_args.get("--incoming_topic", "sf_kaf_in"))
    sf_acc_name_list = sf_query(lst=cases_to_lookup, creds=creds)

    kafka_prod(force_out=sf_acc_name_list, outgoing_topic_name=safe_args.get("--outgoing_topic", "sf_kaf_out"))


if __name__ == '__main__':
    main(sys.argv[1:])
