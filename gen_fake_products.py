from app import db
from app.models import Product
from faker import Faker
from random import randint, uniform

fake = Faker()

def gen(count_of_posts, user_start, user_end):
    for _ in range(0, count_of_posts):
        post = Product(fake.sentence(nb_words=1), fake.paragraph(nb_sentences=50), randint(user_start, user_end), uniform(10, 2000), randint(0, 200), )
        post.save()
    return '{} posts are generated'.format(count_of_posts)