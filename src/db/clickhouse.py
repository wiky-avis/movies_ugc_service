import logging
import sys


sys.path.insert(0, "/home/tirax/movies_ugc_service")

# from src.db.exceptions import DatabaseError
# from src.settings.database import DatabaseSettings
import clickhouse_connect

from src.db.base import AbstractDatabase


logger = logging.getLogger(__name__)

crate_database_request = """
create database if not exists video on cluster company_cluster
"""

create_kafka_table_request = """
create table if not exists video.user_progress_queue on cluster company_cluster
(
    user_id UUID,
    film_id UUID,
    viewed_frame Int64,
    ts DateTime
) ENGINE=Kafka()
SETTINGS
    kafka_broker_list = 'broker:9092',
    kafka_topic_list = 'progress-topic',
    kafka_group_name = 'test-consumer-group',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1
"""

create_storage_table_request = """
create table if not exists video.user_progress on cluster company_cluster
(
    user_id UUID,
    film_id UUID,
    viewed_frame Int64,
    ts DateTime
) ENGINE=MergeTree
PARTITION BY toYYYYMMDD(ts)
order by (user_id, viewed_frame)
"""

create_kafka_materialized_view_request = """
CREATE MATERIALIZED VIEW if not exists video.user_progress_mv TO video.user_progress AS
SELECT *
FROM video.user_progress_queue
"""


class ClickRepository(AbstractDatabase):
    client = None

    def __init__(self) -> None:
        self.client = clickhouse_connect.get_client(
            host="localhost", port=8123
        )
        self._create_tables()

    def _create_tables(self):
        self.client.command(crate_database_request)
        self.client.command(create_kafka_table_request)
        self.client.command(create_storage_table_request)
        self.client.command(create_kafka_materialized_view_request)

    def _drop_tables(self):
        self.client.command("drop table if exists video.user_progress_queue")
        self.client.command("drop table if exists video.user_progress")
        self.client.command("drop table if exists video.user_progress_mv")

    def get(self):
        print("\n get request")
        # self._drop_tables()
        print("\n Kafka qeue \n")
        result = self.client.query("SELECT * FROM video.user_progress_queue")
        print(result.result_rows)
        print("\n Main table \n")
        result = self.client.query("SELECT * FROM video.user_progress")
        print(result.result_rows)
        pass


click = ClickRepository()

click.get()

# client = clickhouse_connect.get_client(host='localhost',
#                                                     port=8123,
#                                                     username='default',
#                                                     password='123')
