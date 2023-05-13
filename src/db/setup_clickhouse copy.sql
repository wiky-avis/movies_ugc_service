create database if not exists video on cluster company_cluster;

create table if not exists video.user_progress_queue on cluster company_cluster ( user_id UUID, film_id UUID, viewed_frame Int64, ts DateTime) engine=Kafka() settings kafka_broker_list = 'broker:9092', kafka_topic_list = 'progress-topic', kafka_group_name = 'test-consumer-group', kafka_format = 'JSONEachRow', kafka_num_consumers = 1;

create table if not exists video.user_progress on cluster company_cluster (user_id UUID, film_id UUID, viewed_frame Int64, ts DateTime) engine=MergeTree partition by toYYYYMMDD(ts) order by (user_id, viewed_frame);

create materialized view if not exists video.user_progress_mv to video.user_progress as select * from video.user_progress_queue;