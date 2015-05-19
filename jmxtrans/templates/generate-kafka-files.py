#!/usr/bin/env python

import json
from collections import OrderedDict

# obj, attr[0], resultAlias
metrics = [
  [
    "kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs",
    "Count",
    "sdkafka.log.LogFlushStats.LogFlush"
  ],
  [
    "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
    "Count",
    "sdkafka.server.BrokerTopicMetrics.AllTopicsBytesIn"
  ],
  [
    "kafka.server:type=BrokerTopicMetrics,name=FailedFetchRequestsPerSec",
    "Count",
    "sdkafka.server.BrokerTopicMetrics.AllTopicsFailedFetchRequests"
  ],
  [
    "kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec",
    "Count",
    "sdkafka.server.BrokerTopicMetrics.AllTopicsFailedProduceRequests"
  ],
  [
    "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec",
    "Count",
    "sdkafka.server.BrokerTopicMetrics.AllTopicsMessagesIn"
  ],
  [
    "kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec",
    "Count",
    "sdkafka.server.BrokerTopicMetrics.AllTopicsBytesOut"
  ],
  [
    "kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions",
    "Value",
    "sdkafka.server.ReplicaManager.UnderReplicatedPartitions"
  ],
  [
    "kafka.server:type=ReplicaManager,name=PartitionCount",
    "Value",
    "sdkafka.server.ReplicaManager.PartitionCount"
  ],
  [
    "kafka.server:type=ReplicaManager,name=LeaderCount",
    "Value",
    "sdkafka.server.ReplicaManager.LeaderCount"
  ],
  [
    "kafka.server:type=ReplicaManager,name=IsrShrinksPerSec",
    "Count",
    "sdkafka.server.ReplicaManager.ISRShrinks"
  ],
  [
    "kafka.server:type=ReplicaManager,name=IsrExpandsPerSec",
    "Count",
    "sdkafka.server.ReplicaManager.ISRExpands"
  ],
  [
    "kafka.server:type=ReplicaFetcherManager,name=MaxLag",
    "Value",
    "sdkafka.server.ReplicaFetcherManager.MaxLag"
  ],
  [
    "kafka.server:type=ReplicaFetcherManager,name=MinFetchRate",
    "Value",
    "sdkafka.server.ReplicaFetcherManager.MinFetchRate"
  ],
  [
    "kafka.server:type=ProducerRequestPurgatory,name=NumDelayedRequests",
    "Value",
    "sdkafka.server.ProducerRequestPurgatory.NumDelayedRequests"
  ],
  [
    "kafka.server:type=ProducerRequestPurgatory,name=PurgatorySize",
    "Value",
    "sdkafka.server.ProducerRequestPurgatory.PurgatorySize"
  ],
  [
    "kafka.server:type=FetchRequestPurgatory,name=NumDelayedRequests",
    "Value",
    "sdkafka.server.FetchRequestPurgatory.NumDelayedRequests"
  ],
  [
    "kafka.server:type=FetchRequestPurgatory,name=PurgatorySize",
    "Value",
    "sdkafka.server.FetchRequestPurgatory.PurgatorySize"
  ],
  [
    "kafka.network:type=RequestMetrics,name=Produce-RequestsPerSec",
    "Count",
    "sdkafka.network.RequestMetrics.ProduceRequests"
  ],
  [
    "kafka.network:type=RequestMetrics,name=Fetch-Follower-RequestsPerSec",
    "Count",
    "sdkafka.network.RequestMetrics.FetchFollowerRequests"
  ],
  [
    "kafka.network:type=RequestMetrics,name=Fetch-Consumer-RequestsPerSec",
    "Count",
    "sdkafka.network.RequestMetrics.FetchConsumerRequests"
  ],
  [
    "kafka.controller:type=KafkaController,name=ActiveControllerCount",
    "Value",
    "sdkafka.controller.KafkaController.ActiveControllerCount"
  ],
  [
    "kafka.controller:type=KafkaController,name=OfflinePartitionsCount",
    "Value",
    "sdkafka.controller.KafkaController.OfflinePartitionsCount"
  ],
  [
    "kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs",
    "Count",
    "sdkafka.controller.ControllerStats.LeaderElection"
  ],
  [
    "kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec",
    "Count",
    "sdkafka.controller.ControllerStats.UncleanLeaderElection"
  ],
  [
    "kafka.consumer:type=ConsumerFetcherManager,name=*-MaxLag",
    "Value",
    "sdkafka.consumer.ConsumerFetcherManager.MaxLag"
  ],
  [
    "kafka.consumer:type=ConsumerFetcherManager,name=*-MinFetchRate",
    "Value",
    "sdkafka.consumer.ConsumerFetcherManager.MinFetchRate"
  ],
  [
    "kafka.producer:type=ProducerRequestsMetrics,name=ProducerRequestSize",
    "Count",
    "sdkafka.producer.ProducerRequestsMetrics.AllBrokersProducerRequestSize"
  ],
  [
    "kafka.producer:type=ProducerRequestsMetrics,name=ProducerRequestRateAndTimeMs",
    "Count",
    "sdkafka.producer.ProducerRequestsMetrics.AllBrokersProducerRequestRate"
  ],
  [
    "kafka.producer:type=ProducerStats,name=FailedSendsPerSec",
    "Count",
    "sdkafka.producer.ProducerStats.FailedSendsPerSec"
  ],
  [
    "kafka.producer:type=ProducerTopicMetrics,name=BytesPerSec",
    "Count",
    "sdkafka.producer.ProducerTopicMetrics.AllTopicsBytes"
  ],
  [
    "kafka.producer:type=ProducerTopicMetrics,name=DroppedMessagesPerSec",
    "Count",
    "sdkafka.producer.ProducerTopicMetrics.AllTopicsDroppedMessages"
  ],
  [
    "kafka.producer:type=ProducerTopicMetrics,name=MessagesPerSec",
    "Count",
    "sdkafka.producer.ProducerTopicMetrics.AllTopicsMessages"
  ]
]

def write_config_file(filename, url, source, detectInstance):
  # Build from inside out. First the "settings" dictionary
  settingsDict = OrderedDict();
  settingsDict["token"] = "STACKDRIVER_API_KEY";
  settingsDict["url"] = url;
  if (source is not None):
    settingsDict["source"] = source;
  if (detectInstance is not None):
    settingsDict["detectInstance"] = detectInstance;

  # Now the outputWriters array, which contains only one element.
  outputWriters = [OrderedDict([
    ("@class", "com.googlecode.jmxtrans.model.output.StackdriverWriter"),
    ("settings", settingsDict)
    ])]

  # Now the queries array, derived from 'metrics'. Each element of the queries
  # array is a dict, derived from metrics. But the all have an (identical)
  # reference to outputWriters.
  queries = []
  for m in metrics:
    query = OrderedDict([
      ("obj", m[0]),
      ("attr", [m[1]]),
      ("resultAlias", m[2]),
      ("outputWriters", outputWriters)
      ])
    queries.append(query)

  # Now the server "array" (which contains only one element).
  servers = [OrderedDict([
    ("port", "KAFKA_JMX_PORT"),
    ("host", "KAFKA_JMX_HOST"),
    ("queries", queries)
    ])]

  # Now the config dictionary, whose only element is the server array.
  config = OrderedDict([("servers", servers)])

  # Write the file!
  with open(filename, 'w') as out:
    json.dump(config, out, indent=2, separators=(',', ': '))


def main():
  sdgw = 'https://jmx-gateway.stackdriver.com/v1/custom';
  gggw = 'https://jmx-gateway.google.stackdriver.com/v1/custom';
  file = 'kafka-082.json';
  write_config_file('../stackdriver/json-detect-instance/' + file, sdgw, None, 'AWS');
  write_config_file('../stackdriver/json-specify-instance/' + file, sdgw, 'AWS_INSTANCE_ID', None);
  write_config_file('../google-cloud-monitoring/json-detect-instance/' + file, gggw, None, 'GCE');
  write_config_file('../google-cloud-monitoring/json-specify-instance/' + file, gggw, 'GCE_INSTANCE_ID', None);

if __name__ == "__main__":
    main()
