from dependency_injector import containers, providers

from src.brokers import kafka_producer
from src.common import db
from src.repositories import user_activity
from src.services import user_bookmarks, user_view_history


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.view_progress",
            "src.api.v1.endpoints.bookmarks",
        ]
    )

    kafka_producer = providers.Factory(kafka_producer.KafkaProducer)
    db_client = providers.Factory(db.MongoDbConnector)
    user_activity_repository = providers.Factory(
        user_activity.UserActivityRepository,
        client=db_client,
    )

    user_view_history_service = providers.Factory(
        user_view_history.UserViewHistoryService,
        producer=kafka_producer,
        repository=user_activity_repository,
    )

    user_bookmarks_service = providers.Factory(
        user_bookmarks.UserBookmarksService,
        producer=kafka_producer,
        repository=user_activity_repository,
    )
