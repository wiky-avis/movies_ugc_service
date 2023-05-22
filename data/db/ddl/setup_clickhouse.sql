create database if not exists ugc on cluster company_cluster;


-- Данные по просмотренным фреймам
create table if not exists ugc.user_progress_queue on cluster company_cluster 
( 
    user_id UUID, 
    film_id UUID, 
    viewed_frame Int64, 
    ts DateTime
) engine=Kafka() 
settings 
    kafka_broker_list = 'broker:9092', 
    kafka_topic_list = 'progress-topic', 
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSONEachRow', 
    kafka_num_consumers = 1;


create table if not exists ugc.user_progress on cluster company_cluster 
(
    user_id UUID, 
    film_id UUID, 
    viewed_frame Int64, 
    ts DateTime
) engine=MergeTree 
partition by toYYYYMMDD(ts) 
order by ts desc;


create materialized view if not exists ugc.user_progress_mv to ugc.user_progress as 
select * 
from ugc.user_progress_queue;


-- Добавление или удаление фильма из закладок
create table if not exists ugc.user_bookmarks_queue on cluster company_cluster 
( 
    user_id UUID, 
    film_id UUID, 
    event_type FixedString(10), -- add, delete
    ts DateTime
) engine=Kafka() 
settings 
    kafka_broker_list = 'broker:9092', 
    kafka_topic_list = 'bookmarks-topic', 
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSONEachRow', 
    kafka_num_consumers = 1;


create table if not exists ugc.user_bookmarks on cluster company_cluster 
(
    user_id UUID, 
    film_id UUID, 
    event_type FixedString(10), -- add, delete
    ts DateTime
) engine=MergeTree 
partition by toYYYYMMDD(ts) 
order by ts desc;


create materialized view if not exists ugc.user_bookmarks_mv to ugc.user_bookmarks as 
select * 
from ugc.user_bookmarks_queue;


-- Оценки фильмов от пользователей
create table if not exists ugc.user_film_rating_queue on cluster company_cluster 
( 
    user_id UUID, 
    film_id UUID, 
    rating Int8, --1 to 10
    ts DateTime
) engine=Kafka() 
settings 
    kafka_broker_list = 'broker:9092', 
    kafka_topic_list = 'film-rating-topic', 
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSONEachRow', 
    kafka_num_consumers = 1;


create table if not exists ugc.user_film_rating on cluster company_cluster 
(
    user_id UUID, 
    film_id UUID, 
    rating Int8, --1 to 10
    ts DateTime
) engine=MergeTree 
partition by toYYYYMMDD(ts) 
order by ts desc;

create materialized view if not exists ugc.user_film_rating_mv to ugc.user_film_rating as 
select * 
from ugc.user_film_rating_queue;


-- Отзывы/обзоры фильмов от пользователей
create table if not exists ugc.user_film_reviews_queue on cluster company_cluster 
( 
    user_id UUID, 
    film_id UUID, 
    review_id UUID,
    review_title String, --Заголовок
    review_body String, --Текст отзыва
    ts DateTime
) engine=Kafka() 
settings 
    kafka_broker_list = 'broker:9092', 
    kafka_topic_list = 'film-reviews-topic', 
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSONEachRow', 
    kafka_num_consumers = 1;


create table if not exists ugc.user_film_reviews on cluster company_cluster 
(
    user_id UUID, 
    film_id UUID, 
    review_id UUID,
    review_title String, --Заголовок
    review_body String, --Текст отзыва
    ts DateTime
) engine=MergeTree 
partition by toYYYYMMDD(ts) 
order by ts desc;


create materialized view if not exists ugc.user_film_reviews_mv to ugc.user_film_reviews as 
select * 
from ugc.user_film_reviews_queue;


-- Оценки отзывов/обзоров от пользователей
create table if not exists ugc.user_film_reviews_likes_queue on cluster company_cluster 
( 
    user_id UUID, 
    review_id UUID,
    action FixedString(20), -- like, dislike, remove_like, remove_dislike
    ts DateTime
) engine=Kafka() 
settings 
    kafka_broker_list = 'broker:9092', 
    kafka_topic_list = 'film-reviews-likes-topic', 
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSONEachRow', 
    kafka_num_consumers = 1;


create table if not exists ugc.user_film_reviews_likes on cluster company_cluster 
(
    user_id UUID, 
    review_id UUID,
    action FixedString(20), -- like, dislike, remove_like, remove_dislike
    ts DateTime
) engine=MergeTree 
partition by toYYYYMMDD(ts) 
order by ts desc;


create materialized view if not exists ugc.user_film_reviews_likes_mv to ugc.user_film_reviews_likes as 
select * 
from ugc.user_film_reviews_likes_queue;