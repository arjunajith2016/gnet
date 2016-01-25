# all the imports
import os
import datetime
from flask import Flask, jsonify, request, session, redirect, url_for, render_template, flash, send_from_directory, abort, make_response
from flask.ext.triangle import Triangle

chatbox = [{'message' : 'Hi! Try sending a message.'},{'message' : 'This is hard indeed.'}]

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
Triangle(app)
app.config.from_object(__name__)

# functions
def debugdb():
    cur = g.db.execute('select * from users')
    print cur.fetchall()
    cur = g.db.execute('select * from entries')
    print cur.fetchall()

# database connection

# setting up views

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat',methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        chatbox.append(request.json['payload'])
    return jsonify({'message' : chatbox})

@app.route('/add', methods=['POST'])
def add_entry():
    t=datetime.datetime.now()
    current_date=str(getattr(t,'day'))+'-'+str(getattr(t,'month'))+'-'+str(getattr(t,'year'))
    if getattr(t,'hour') < 12:
        current_time=str(getattr(t,'hour'))+':'+str(getattr(t,'minute'))+' AM'
    elif getattr(t,'hour') == 12:
        current_time=str(getattr(t,'hour'))+':'+str(getattr(t,'minute'))+' PM'
    elif getattr(t,'hour') > 12:
        current_time=str(getattr(t,'hour')-12)+':'+str(getattr(t,'minute'))+' PM'

    if not session.get('logged_in'):
        abort(401)
    if not request.json or not 'title' in request.json:
        abort(400)
    else:
        g.db.execute('insert into entries (title, text, date, time, user) values (?, ?, ?, ?, ?)', [request.json['title'], request.json['text'], current_date, current_time, session['user']])
        g.db.commit()
        flash('New entry was successfully posted')
    return redirect(url_for('home'))

@app.route('/del', methods=['DELETE'])
def del_entry():
    g.db.execute('delete from entries where id=(?)', [request.json['del']])
    g.db.commit()
    flash('Post deleted')
    return jsonify({'result': True})

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users where username=(?)', [request.json['username']])
        users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]

        flag2=0
        for item in users:
            if request.json['username'] == item['username']:
                flag2=1
        
        if request.json['name']=='':
            flash('Name cannot be empty')
        elif request.json['username']=='':
            flash('Username cannot be empty')
        elif request.json['password']=='':
            flash('password cannot be empty')
        elif flag2 == 0:
            g.db.execute('insert into users (name, username, password) values (?, ?, ?)', [request.json['name'], request.json['username'], request.json['password']])
            g.db.commit()
            flash('You have been registered')
            return jsonify({'result': True})
        else:
            flash('Username already exists')
            return jsonify({'result': False})

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password, name from users where username=(?)', [request.json['username']])
        users = [dict(username=row[0], password=row[1], name=row[2]) for row in cur.fetchall()]

        flag2=0
        for item in users:
            if request.json['username'] == item['username']:
                flag2=1
                if request.json['password'] == item['password']:
                    session['logged_in'] = True
                    session['user'] = item['name']
                    flash(str('Welcome back, %s' %item['name']))
                    return jsonify({'result': True})

        if flag2==0:
            error = 'Invalid username'
            return jsonify({'result': False})
        elif flag2==1:
            error = 'Invalid password'
            return jsonify({'result': False})
    return render_template('login.html', flag=True, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# to start the server
if __name__ == '__main__':
    #init_db()
    app.run()