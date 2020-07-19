from flask import Flask,redirect, url_for, render_template
import sqlite3

app= Flask(__name__)

app.config['SECRET_KEY'] = 'alican secret key'

@app.route("/")
def foodgroups():

    db = sqlite3.connect('usda_foods.db')
    d = db.cursor()
    d.execute('SELECT * FROM food_group')

    return render_template('foodgroups.html',groups=d.fetchall())

@app.route("/FOOD/<int:group_id>",methods=['GET','POST'])
def food(group_id):

    db = sqlite3.connect('usda_foods.db')
    d = db.cursor()
    d.execute('SELECT * FROM food WHERE food_group_id=?',[group_id])

    return render_template('food.html',foods=d.fetchall())
    


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080, debug=True)