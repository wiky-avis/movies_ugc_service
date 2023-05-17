from dependency_injector import containers, providers

from src.brokers import kafka_producer
from src.common import db
from src.repositories import user_activity
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

    db_client = providers.Factory(db.MongoDbConnector)

    user_activity_repository = providers.Factory(
        user_activity.UserActivityRepository,
        client=db_client,
    )
