from flask import Flask, render_template, redirect, url_for,flash
from flask_bootstrap import Bootstrap
from flask_login import login_required
from flask_restplus import reqparse

from forms import LoginForm,Register_Form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
bootstrap = Bootstrap(app)

@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data is not None and form.password.data is not None:
            flash('login successfully')
            global name
            name = form.username.data
            return redirect(url_for('main'))
        else:
            flash('login failed')
            return render_template('login.html', form=form)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = Register_Form()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('signup.html',form=form)




if __name__ == '__main__':
    app.run(debug=True)
