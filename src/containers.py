from dependency_injector import containers, providers

from src.brokers import kafka_producer
from src.services import user_activity_service


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.api.v1.endpoints.view_progress"]
    )

    kafka_producer = providers.Factory(kafka_producer.KafkaProducer)

    user_activity_service = providers.Factory(
        user_activity_service.UserActivityService,
        producer=kafka_producer,
    )
