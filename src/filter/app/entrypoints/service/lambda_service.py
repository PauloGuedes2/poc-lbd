import logging

from adapters.sqs_publisher import SQSPublisher
from usecases.process_event_if_0202 import ProcessEventIf0202

logger = logging.getLogger()


class LambdaService:
    def __init__(self, publisher=None):
        self.publisher = publisher or SQSPublisher()

    def entry_process(self, event, context):
        logger.info("Iniciando processamento...")
        self._validate_event(event)

        for record in event.get("records", {}).values():
            self._process_records(record)

    @staticmethod
    def _validate_event(event):
        if not event.get("records"):
            raise ValueError("Evento sem dados!")

    def _process_records(self, records):
        for payload in records:
            if not payload.get("value"):
                logger.warning("Payload inválido ignorado.")
                continue
            ProcessEventIf0202(self.publisher).process_event(payload["value"])
