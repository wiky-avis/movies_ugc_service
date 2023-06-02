import random
from datetime import datetime

import tqdm
from faker import Faker

from settings import research_settings


class DBDataGenerator:
    def __init__(self):
        self.faker = Faker()

    def generate_like_doc(
        self, user_id: str = None, film_id: str = None, rating: int = None
    ) -> dict:
        film_id = film_id or self.faker.uuid4()
        user_id = user_id or self.faker.uuid4()
        rating = rating or random.randint(1, 10)

        return {"film_id": film_id, "user_id": user_id, "rating": rating}

    def generate_review_doc(self):
        f_id = random.randint(0, research_settings.n_films)
        return {
            "film_id": f"film_{f_id}",
            "user_id": self.faker.uuid4(),
            "text": self.faker.sentence(),
            "created": datetime.now(),
        }

    def gen_ids(self, count: int) -> list:
        if count > research_settings.n_users:
            count = research_settings.n_users

        return [self.faker.uuid4() for _ in tqdm.tqdm(range(count))]
