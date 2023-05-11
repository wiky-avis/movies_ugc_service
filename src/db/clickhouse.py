import logging

import sys

sys.path.insert(0, '/home/tirax/movies_ugc_service')

from src.db.base import AbstractDatabase
# from src.db.exceptions import DatabaseError
# from src.settings.database import DatabaseSettings
import clickhouse_connect


logger = logging.getLogger(__name__)

crate_database_request = '''
create database if not exists video on cluster company_cluster
'''

create_table_request = '''
create table if not exists video.user_progress_queue on cluster company_cluster
(
    user_id UUID,
    film_id UUID,
    viewed_frame Int64,
    ts UInt64
) ENGINE=Kafka()
SETTINGS
    kafka_broker_list = 'broker:9092',
    kafka_topic_list = 'progress-topic',
    kafka_group_name = 'progress-group',
    kafka_format = 'JSONEachRow'
    
'''


class ClickRepository(AbstractDatabase):
    client = None
    
    def __init__(self) -> None:
        self.client = clickhouse_connect.get_client(host='localhost', 
                                                    port=8123)
        self._create_tables()
        
    def _create_tables(self):
        self.client.command(crate_database_request)
        self.client.command(create_table_request)
    
    def get(self):
        print('\n get request')
        # result = self.client.command('drop table if exists video.user_progress_queue')
        result = self.client.query('SELECT * FROM video.user_progress_queue')
        print(result.result_rows)
        pass


click = ClickRepository()

click.get()

# client = clickhouse_connect.get_client(host='localhost', 
#                                                     port=8123, 
#                                                     username='default', 
#                                                     password='123')