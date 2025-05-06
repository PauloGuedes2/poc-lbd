import boto3
import json
import os
import logging
from adapters.publisher_contract import Publisher

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SQSPublisher(Publisher):
    def __init__(self):
        self._client = boto3.client("sqs")
        self._queue_url = os.getenv("SQS_QUEUE_URL")

        if not self._queue_url:
            raise EnvironmentError("SQS_QUEUE_URL is not set.")

    def publish(self, message: dict) -> None:
        logger.info("Publicando mensagem no SQS...")
        response = self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=json.dumps(message)
        )
        logger.info(f"Mensagem publicada com sucesso. MessageId: {response.get('MessageId')}")
