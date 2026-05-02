from kafka import KafkaProducer
import json
import time
import datetime

BOOTSTRAP_SERVERS = [
    'b-2.mskdemocluster.eq1kwf.c24.kafka.us-east-1.amazonaws.com:9092',
    'b-1.mskdemocluster.eq1kwf.c24.kafka.us-east-1.amazonaws.com:9092'
]

TOPIC_NAME = 'demo-topic'

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda v: v.encode('utf-8') if v else None
)

print("Producer started")

count = 0
while True:
    message = {
        'id': count,
        'timestamp': str(datetime.datetime.utcnow()),
        'source': 'worker-ec2',
        'data': f'Sample event number {count}'
    }

    future = producer.send(
        TOPIC_NAME,
        key=f'key-{count}',
        value=message
    )

    record_metadata = future.get(timeout=10)

    print(f"Sent message {count} → partition {record_metadata.partition}, offset {record_metadata.offset}")

    count += 1
    time.sleep(2)
