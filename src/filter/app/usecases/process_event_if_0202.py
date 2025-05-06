import json
import logging
from adapters.publisher_contract import Publisher

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ProcessEventIf0202:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher

    def process_event(self, payload: str) -> None:
        event = self._parse_payload(payload)
        if not event:
            return

        if self._is_operacao_0202(event):
            self._publish_event(event)
        else:
            logger.info("Operação não é 0202. Evento descartado.")

    @staticmethod
    def _parse_payload(payload: str) -> dict | None:
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            logger.warning("Erro ao decodificar JSON. Ignorando payload.")
            return None

    @staticmethod
    def _is_operacao_0202(event: dict) -> bool:
        return event.get("codigo_modalidade_operacao") == "0202"

    def _publish_event(self, event: dict) -> None:
        logger.info("Operação 0202 detectada. Publicando no SQS...")
        self.publisher.publish(event)
