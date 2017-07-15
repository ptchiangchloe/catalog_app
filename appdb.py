import psycopg2, bleach
import psycopg2.extras

DBNAME = "myflaskapp"

def add_user(name, email, username, password):
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s,%s)",(name, email, username, password) )
  db.commit()
  db.close()


def get_user(username, password_candidate):
    db = psycopg2.connect(database=DBNAME)
    print username
    c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute("SELECT * FROM users WHERE username=(%s)",(username,))
    result = c.fetchone()
    print result
    db.commit()
    db.close()
    return result

def add_item_to_db(title, category, description):
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("INSERT INTO items(title, category, description) VALUES(%s, %s,%s)",(title, category, description) )
  db.commit()
  db.close()

def get_items():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
  c.execute("SELECT * FROM items" )
  result = c.fetchall()
  db.commit()
  db.close()
  return result

def get_latest_items():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
  c.execute("SELECT * FROM items ORDER BY create_date DESC LIMIT 10" )
  result = c.fetchall()
  db.commit()
  db.close()
  return result

def get_items_by_category(category):
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
  print category
  c.execute("SELECT * FROM items WHERE category='%s' ORDER BY create_date DESC LIMIT 10"%(category))
  result = c.fetchall()
  db.commit()
  db.close()
  return result

def get_item(id):
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
  c.execute("SELECT * FROM items WHERE id ='%s'"%(id))
  result = c.fetchone()
  db.commit()
  db.close()
  return result

def update_item_to_db(id, title, category, description):
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("UPDATE items SET title=%s, category=%s, description=%s WHERE id = %s",(title, category, description, id) )
  db.commit()
  db.close()

def delete_item_from_db(id):
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
  c.execute("DELETE FROM items WHERE id = (%s)",(id))
  db.commit()
  db.close()
