from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyBjVAFl-Zbw3eVMtbZFWm4fVverjIS0CqE",
  "authDomain": "personal-project---pigeons.firebaseapp.com",
  "projectId": "personal-project---pigeons",
  "storageBucket": "personal-project---pigeons.appspot.com",
  "messagingSenderId": "813577128186",
  "appId": "1:813577128186:web:94af2c599387ca136ea143",
  "measurementId": "G-0BTEVC0R8J",
  "databaseURL": "https://personal-project---pigeons-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():    
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('post'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")



@app.route('/login' , methods = ['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']

        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('post'))
        except:
            error = "Authentication failed"
            return render_template("login.html", error = error)
    else:
        return render_template("login.html")


@app.route('/post', methods = ['GET', 'POST'])
def post():
    error = ""
    if request.method == 'POST':
        name = request.form['name']
        pigeons_name = request.form['pigeons_name']
        your_story = request.form['your_story']
        try:
            story = {"name": request.form['name'], "pigeons_name":request.form['pigeons_name'], "your_story": request.form['your_story']}
            db.child("Stories").push(story)
            return redirect(url_for('all_posts'))
        except:
            error = "Authentication failed"
    else:
        return render_template("post.html")


@app.route('/all_posts')
def all_posts():
    return render_template ("all_posts.html",  stories = db.child("Stories").get().val().values() )





@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template ("about.html",)


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)