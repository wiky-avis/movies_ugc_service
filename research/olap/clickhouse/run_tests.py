import time
import uuid

from clickhouse_driver import Client
from faker import Faker


batch_size = 10000

client: Client = Client("localhost")
client.execute(
    """
    CREATE TABLE IF NOT EXISTS test_user_progress
    (
        user_id UUID,
        film_id UUID,
        viewed_frame Int64,
        ts DateTime
    ) engine=MergeTree()
    ORDER BY (user_id, film_id, viewed_frame);
    """
)

fake: Faker = Faker()


def insert_data(num_batches: int) -> None:
    """
    Функция для вставки данных в ClickHouse
    :param num_batches: количество пачек данных
    """
    total_records = batch_size * num_batches

    start_time = time.time()

    for batch in range(num_batches):
        data = []
        for _ in range(batch_size):
            user_id = uuid.uuid4()
            film_id = uuid.uuid4()
            viewed_frame = fake.random_int(min=0, max=1000)
            ts = fake.date_time_between(start_date="-1y", end_date="now")
            data.append((user_id, film_id, viewed_frame, ts))

        client.execute(
            "INSERT INTO test_user_progress (user_id, film_id, viewed_frame, ts) VALUES",
            data,
        )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Вставка %s записей заняла %s сек" % (total_records, elapsed_time))
    insertion_speed = total_records / elapsed_time
    print("Скорость вставки: %s записей/сек" % insertion_speed)


def read_data() -> None:
    """
    Функция для чтения данных из ClickHouse
    """
    start_time = time.time()

    result = client.execute(
        """
        SELECT
            user_id,
            sum(viewed_frame),
            max(viewed_frame)
        FROM test_user_progress
        WHERE ts > '2022-12-01 00:00:00'
        GROUP by user_id
        """
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Агрегация {len(result)} записей заняло {elapsed_time} сек")
    read_speed = len(result) / elapsed_time
    print(f"Скорость: {read_speed} записей/сек")


if __name__ == "__main__":
    insert_data(1000)
    read_data()
