#!/usr/bin/env python
from flask import (Flask, url_for, session, request, redirect,
                   Response, render_template)
from inbox import APIClient

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'

app = Flask(__name__)
app.secret_key = 'secret'

def get_client():
    return APIClient(APP_ID, APP_SECRET, session['access_token']).namespaces[0]

def create_todo_tag():
    c = get_client()
    t = c.tags.create(name='todo')
    try:
        t.save()
    except:
        pass


@app.before_request
def login():
    if request.endpoint != 'login_callback':
        if 'access_token' not in session:
            redirect_uri = url_for('.login_callback', _external=True)
            client = APIClient(APP_ID, APP_SECRET)
            return redirect(client.authentication_url(redirect_uri))
        else:
            create_todo_tag()

@app.route('/')
def index():
    client = get_client()
    try:
        todos = client.threads.where({'tag': 'todo'}).all()
    except Exception as e:
        print(e.message)
    return render_template('todo.html', todos=todos)

@app.route('/add')
def add():
    c = get_client()
    draft = c.drafts.create(subject=request.args['text'])
    draft.save()
    thread = c.threads.where(thread=draft.thread).first()
    thread.add_tags(['todo'])
    return index()

@app.route('/delete/<id>')
def delete(id):
    thread = get_client().threads.where(thread=id).first()
    thread.remove_tags(['todo'])
    return index()

@app.route('/update/<id>')
def update(id):
    delete(id)

    c = get_client()
    draft = c.drafts.create()
    draft.subject = request.args['text']
    draft.save()
    thread = c.threads.where(thread=draft.thread).first()
    thread.add_tags(['todo'])
    return index()

@app.route('/login_callback')
def login_callback():
    if 'error' in request.args:
        return "Login error: {0}".format(request.args['error'])

    client = APIClient(APP_ID, APP_SECRET)
    code = request.args.get('code')
    session['access_token'] = client.token_for_code(code)
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
