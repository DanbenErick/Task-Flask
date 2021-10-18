import sqlite3
from flask import Flask, render_template, request


app = Flask(__name__)
DATABASE = 'database.db'

#Database functions
def connect_database():
  global con
  global cur
  con = sqlite3.connect('database.db', check_same_thread=False)
  cur = con.cursor()

#Operations Database
def get_data():
  connect_database()
  sql = 'SELECT * FROM tasks'
  cur.execute(sql)
  con.commit()
  data = cur.fetchall()
  con.close()
  return data
  
def end_task(id):
  connect_database()
  sql = "UPDATE tasks SET state = 'Terminado' WHERE id = ?"
  cur.execute(sql, (id, ))
  con.commit()
  con.close()
  return "Tarea terminada"

#Routes
@app.route('/')
def Index():
  data = get_data()  
  return render_template('pagina.html', data= data)

@app.route('/edit/<id>')
def edit_task(id):
  resp = end_task(id)
  return resp

@app.route('/delete/<id>')
def delete_task(id):
  connect_database()
  sql = "DELETE FROM tasks WHERE id = ?"
  cur.execute(sql, (id,))
  con.commit()
  con.close()
  return "tarea eliminada"

@app.route('/save', methods=['POST'])
def save_task():
  title = request.form['title']
  description = request.form['description']
  state = 'Pendiente'
  connect_database()
  sql = "INSERT INTO tasks (title, description, state) VALUES (?,?,?)"
  cur.execute(sql, (title, description, state))
  con.commit()
  con.close()
  return f'Estos son los datos registrados {title} {description} {state}'

if __name__ == '__main__':
  app.run(port = 3000, debug = True)



