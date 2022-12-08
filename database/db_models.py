from peewee import (
    SqliteDatabase,
    AutoField,
    Model,
    TextField,
    ForeignKeyField,
    DateTimeField,
    BooleanField,
    IntegerField
)

db = SqliteDatabase('main.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField(primary_key=True)
    username = TextField(unique=True)
    password = TextField()


class Group(BaseModel):
    id = AutoField(primary_key=True)
    title = TextField()
    user = ForeignKeyField(User, field='id', on_delete="CASCADE")
    color_scheme = IntegerField()


class Todos(BaseModel):
    id = AutoField(primary_key=True)
    group = ForeignKeyField(Group, field='id', on_delete='CASCADE')
    title = TextField()
    text = TextField()  

    deadline_date = TextField()
    deadline_time = TextField()

    start_date = TextField()
    start_time = TextField()

    status = TextField()


def init():
    User.create_table()
    Group.create_table()
    Todos.create_table()
