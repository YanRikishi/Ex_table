import random
from faker import Faker
from basic_table import db, User
import pandas as pd


def create_fake_users():
    """Generate fake users."""
    faker = Faker()
    for i in range(15):
        user = User(name=faker.name(),
                    age=random.randint(20, 80),
                    address=faker.address().replace('\n', ', '),
                    phone=faker.phone_number(),
                    email=faker.email())
        db.session.add(user)
    db.session.commit()


def delete_fake_users():
    """Пример использования SQL - убираем из БД доноров,
    находящихся в группе людей старше 75 (группа риска)"""
    db.session.execute('DELETE FROM user WHERE age > 50;')
    db.session.commit()


def take_graf():
    mass = pd.read_sql_query("SELECT * FROM user", db.session.connection())
    print(mass)


create_fake_users()
# if __name__ == '__main__':
#     create_fake_users()
#     num_us = db.session.query(User).filter(User.address.contains("NY")).all()
#     print(num_us)
#     # delete_fake_users()
