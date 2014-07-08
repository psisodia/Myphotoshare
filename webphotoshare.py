from flask import Flask, render_template, redirect, request, flash, session
import photoapp
import jinja2

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/sign_up")
def sign_up():
    return render_template("Sign_up.html")

@app.route("/sign_up", methods=["POST"])
def process_signup():
    username = request.form.get('username')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    email = request.form.get('email')
    print username
    user_object = photoapp.User(username=username,
                            password=password,
                            age=age, 
                            zipcode=zipcode,
                            email=email)
    dbusername = photoapp.dbsession.query(photoapp.User).filter_by(username=username).all()
    if dbusername:
        flash("Username already exist, please try different username")
        return render_template("/Sign_up.html")
    else:
        user_object.add_user()
        print user_object.age
        session['userid'] = user_object.id
        flash("user successfully registered")
        return redirect("/upload_album")
   
    

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/upload_album")
def album():
    return render_template("upload_album.html")

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get('username')
    row = photoapp.dbsession.query(photoapp.User).filter_by(username=username).all()
    print row
    if row:
        flash("Log in successful")
        session['userid'] = row[0].id
        print session['userid']
        print row[0].id  
        return redirect("upload_album")
    else:
        flash("Sorry we could not find your record")
        return render_template("login.html")
        
        
    


if __name__ == "__main__":
    app.run(debug = True)