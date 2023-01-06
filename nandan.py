from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import HTTPException
import pymysql

app = FastAPI()

# Set up MySQL connection
connection = pymysql.connect(
    host='localhost',
    user='user',
    password='password',
    db='todolist',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# To-do list item model
class Item(BaseModel):
    title: str
    description: str = None
    done: bool = None

# Authentication decorator
def authenticate(username: str, password: str):
    with connection.cursor() as cursor:
        # Check if user exists
        sql = 'SELECT * FROM users WHERE username=%s AND password=%s'
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=401, detail='Incorrect username or password')
        # Create JWT token
        # ...

# Get list of all to-do list
@app.get('/items')
def read_items(username: str, password: str):
    authenticate(username, password)
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM items'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

# Add new to-do list
@app.post('/items')
def create_item(item: Item, username: str, password: str):
    authenticate(username, password)
    with connection.cursor() as cursor:
        sql = 'INSERT INTO items (title, description, done) VALUES (%s, %s, %s)'
        cursor.execute(sql, (item.title, item.description, item.done))
        connection.commit()
        return {'id': cursor.lastrowid, **item.dict()}

# Update existing to-do
@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item, username: str, password: str):
    authenticate(username, password)
    with connection.cursor() as cursor:
        sql = 'UPDATE items SET title=%s, description=%s, done=%s WHERE id=%s'
        cursor.execute(sql, (item.title, item.description, item.done, item_id))
        connection.commit()
        return {'id': item_id, **item.dict()}

# Delete to-do list
@app.delete('/items/{item_id}')
def delete_item(item_id: int, username: str, password: str):
    authenticate(username, password)
    with connection.cursor() as cursor:
        sql = 'DELETE FROM items WHERE id=%s'
        cursor.execute(sql, (item_id))
        connection.commit()
        return {'id': item_id}