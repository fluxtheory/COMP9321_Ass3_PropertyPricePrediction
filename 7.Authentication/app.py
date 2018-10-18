from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm,Register_Form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
bootstrap = Bootstrap(app)

@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('Login.html', title="Please Login", form=form)

@app.route('/Register',methods=['GET','POST'])
def signup():
    form = Register_Form()
    if form.validate_on_submit():
        return redirect(url_for('app.index'))
    return render_template('Register.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
