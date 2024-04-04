# Пакеты для работы с Flask и SQLAlchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

# Математические пакеты
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np

import random

# Создание проекта
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Здесь использую объектно - ориентированное программирование и ORM для создания модели БД.
# ("Чтобы меньше мучиться с нативным SQL")
class User(db.Model):
    """Создание пользователей, таблица будет называться user"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    gr_b = db.Column(db.String(5))
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True)


def create_fake_users():
    """Generate fake users."""
    faker = Faker()
    number_of_donors = 1000
    for i in range(number_of_donors):
        user = User(name=faker.name(),
                    age=random.randint(20, 80),
                    gr_b=random.choice(["I+", "I-", "II+", "II-",
                                               "III+", "III-", "IV+", "IV-"]),
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
    """Получение графика соотношения количества доноров и их возраста"""
    DF_pandas = pd.read_sql("SELECT age, count(age) as count FROM user GROUP BY age", db.session.connection().connection)
    # print(DF_pandas)

    fig = go.Figure(data=[go.Bar(x=DF_pandas["age"], y=DF_pandas["count"])])

    tickvals = np.arange(0, max(DF_pandas["age"])+1)
    fig.update_layout(title="График соотношения количества доноров и возраста доноров",
                      title_x=0.5,
                      barmode='overlay',
                      margin=dict(l=0, r=0, t=30, b=0),
                      xaxis=dict(title="Years",
                                 tickmode='array',
                                 tickvals=tickvals,
                                 ticktext=[f"{i}" for i in tickvals]),
                      yaxis_title="Count",
                      )

    graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
    return graph_div


# создание файла БД
db.create_all()
create_fake_users()
#take_graf()


# Декораторы для отлова запросов
@app.route('/')
def index():
    users = User.query
    return render_template('basic_table.html', graph_div=take_graf(), title='База данных доноров крови',
                           users=users)


if __name__ == '__main__':
    app.run()


