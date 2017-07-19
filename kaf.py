from simple_salesforce import Salesforce
import requests
from pykafka import *
from pykafka.common import OffsetType
import sys
import getopt
import time
import datetime


def consume_mes(incoming_topic_name, kafka_host_ip="10.13.0.4:9092"):
	"""
	:param incoming_topic_name:
	:param kafka_host_ip:
	:return:
	"""

	client = KafkaClient(kafka_host_ip)
	topic = client.topics[incoming_topic_name]

	consumer = topic.get_simple_consumer(
		auto_offset_reset=OffsetType.EARLIEST,
		reset_offset_on_start=True,
		consumer_timeout_ms=500
	)
	lst = []
	for message in consumer:
		i = ("% s" % message.value)
		lst.append(i)
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
	return force_out


def kafka_prod(force_out, outgoing_topic_name, kafka_host_ip="10.13.0.4:9092"):
	client = KafkaClient(hosts=kafka_host_ip, use_greenlets=True)
	topic = client.topics[outgoing_topic_name]
	res = reduce(lambda x, y: x + y, force_out)
	with topic.get_sync_producer() as producer:
		for i in res:
			print(i)
			producer.produce(str(i[1]) + ";" + str(i[0]))


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



