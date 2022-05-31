from importlib.resources import contents
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import sqlalchemy
from send_email import send_mail
import sqlite3

app= Flask(__name__)

db=SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///lexus-form/feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False 

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer= request.form['customer']
        dealer= request.form['dealer']
        rating= request.form['rating']
        comments= request.form['comments']
        print(customer, dealer, rating, comments)  
        #db.session.add()
        #db.session.commit()      
    if customer == '' or dealer =='':
        return render_template('index.html', message='Please enter required fields')             
    try:
        banco= sqlite3.connect('feedback.db')
        cursor= banco.cursor()
        cursor.execute("INSERT INTO feedback VALUES ('"+str(customer)+"', '"+str(dealer)+"', '"+int(rating)+"','"+str(comments)+"')")
        banco.commit()
        banco.close()
    except:
        print('ERROR')
    return render_template('success.html') 

if __name__ == '__main__':
    app.run(debug=True)
