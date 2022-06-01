from flask import Flask, render_template, request
from models.feedback import Feedback
from send_email import send_mail

app= Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///lexus-form/feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False 


@app.before_first_request   #função criada para ter a segurança de que sempre um banco de dados será inicializado
def create_db():
    db.create_all()


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
        if customer == '' or dealer =='':
            return render_template('index.html', message='Please enter required fields')     
        if db.session.query(Feedback).filter(Feedback.customer==customer).count() == 0:
            data= Feedback(customer, dealer, rating, comments)  #dados do banco de dados no qual serar introduzido os falores
            db.session.add(data)                                #adiciona os dados no banco de dados
            db.session.commit()                                 #fazendo um commit para fazer a confirmação do envio do dados
            return render_template('success.html') 
        return render_template('index.html', message='You have alredy submitted feedback')

if __name__ == '__main__':
    from db import db
    app.init_app(app)                #inicialização do banco de dados
    app.run(debug=True)
