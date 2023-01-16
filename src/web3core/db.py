from peewee import SqliteDatabase

DB = SqliteDatabase(None, pragmas={"foreign_keys": 1})
