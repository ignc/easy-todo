import sqlite3
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)
DATABASE = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'database'
		)

class Connection:

	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.conn = sqlite3.connect(self.path)
		return self.conn.cursor()

	def __exit__(self, type, value, traceback):
		self.conn.commit()
		self.conn.close()

connection = Connection(DATABASE)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
	with connection as c:
		c.execute('INSERT INTO todos (title, password) VALUES (NULL, NULL)')
		list_id = c.lastrowid
	return redirect(url_for('todo', list_id=list_id))

@app.route('/todo/<list_id>')
def todo(list_id):
	with connection as c:
		c.execute('SELECT title, password FROM todos WHERE list_id=?', (list_id,))
		list_data = c.fetchone()
		print(list_data)
		c.execute('SELECT todo, done, item_id FROM items WHERE list_id=?', (list_id,))
		todo = c.fetchall()
		data = {
				'title': list_data[0],
				'password': list_data[1],
				'todo': todo,
				'list_id': list_id
				}
	return render_template('todo.html', **data)

@app.route('/add/<list_id>', methods=['POST'])
def add_item(list_id):
	text = request.form['todo']
	with connection as c:
		c.execute('INSERT INTO items (list_id, todo, done) VALUES (?, ?, 0)', (list_id, text,))
	return redirect(url_for('todo', list_id=list_id))

@app.route('/mark/<item_id>', methods=['POST'])
def mark(item_id):
	with connection as c:
		c.execute('UPDATE items SET done=1 WHERE item_id=?', item_id)

@app.route('/unmark/<item_id>', methods=['POST'])
def unmark(item_id):
	with connection as c:
		c.execute('UPDATE items SET done=0 WHERE item_id=?', item_id)

@app.route('/settitle/<list_id>', methods=['POST'])
def set_title(list_id):
	title = request.form['title']
	with connection as c:
		c.execute('UPDATE todos SET title=? WHERE list_id=?', (title, list_id,))
	return redirect(url_for('todo', list_id=list_id))

@app.route('/create/<list_id>', methods=['GET'])
def create_numbered(list_id):
	with connection as c:
		# TODO
		pass

if __name__ == '__main__':
	app.debug = True
	app.run()
