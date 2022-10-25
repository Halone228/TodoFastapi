from peewee import (
    SqliteDatabase,
    AutoField,
    Model,
    TextField,
    ForeignKeyField,
    DateField,
    BooleanField
)

db = SqliteDatabase('main.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField(primary_key=True)
    username = TextField(unique=True)
    password = TextField()
    email = TextField(unique=True)


class Group(BaseModel):
    id = AutoField(primary_key=True)
    group_title = TextField()
    background_color = TextField()
    title_color = TextField()
    user = ForeignKeyField(User, field='id', on_delete="CASCADE")
    text_shadow = BooleanField(default=False)


class Todos(BaseModel):
    id = AutoField(primary_key=True)
    group = ForeignKeyField(Group, field='id', on_delete='CASCADE')
    title = TextField()
    text = TextField()
    deadline_date = DateField()
    status = TextField()
