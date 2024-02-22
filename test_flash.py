from flask import Flask, flash, redirect, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret key'

@app.route('/')
def index():
    flash('Welcome to Flask!')
    return redirect(url_for('show_message'))

@app.route('/message')
def show_message():
    return render_template('message.html')

if __name__ == '__main__':
    app.run()
