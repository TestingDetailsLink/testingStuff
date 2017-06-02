from simple_salesforce import Salesforce
import requests
from pykafka import *
from pykafka.common import OffsetType


def consume_mes():
	client = KafkaClient("10.13.0.4:9092")
	topic = client.topics['test0']

	consumer = topic.get_simple_consumer(
		consumer_group="my-group0",
		auto_offset_reset=OffsetType.EARLIEST,
		reset_offset_on_start=True,
		consumer_timeout_ms=500
		)
	lst = []
	for message in consumer:
		i = ("% s" % message.value)
		lst.append(i)
	return lst


def sf_query(lst):
	session = requests.Session()
	sf = Salesforce(username='clair.underwood@usgov.com', password='wintherace', security_token='WMQTuZyM8d',
					sandbox=False, session=session)
	for i in lst:
		res = sf.query("SELECT Account.Name, CaseNumber FROM Case WHERE CaseNumber = '%s'" % i)
		if res:
			list_results = [[record['Account']['Name'], record['CaseNumber']] for record in res['records']]
			return list_results


def kafka_prod(list_results):
	client = KafkaClient(hosts='10.13.0.4:9092', use_greenlets=True)
	topic = client.topics['SF_query_results']
	with topic.get_sync_producer() as producer:
		for i in list_results:
			producer.produce(str(i[1]) + ";" + str(i[0]))
