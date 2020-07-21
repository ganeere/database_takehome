from flask import Flask,redirect, url_for, render_template, flash
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Update(FlaskForm):
    long_desc = StringField('Long Description:',
                           validators=[DataRequired(), Length(min=2, max=200)])
    short_desc = StringField('Short Description:',
                           validators=[DataRequired(), Length(min=2, max=60)])
    manufac = StringField('Manufacturer Name:',
                           validators=[DataRequired(), Length(min=2, max=65)])
    scien = StringField('Scientific Name:',
                           validators=[DataRequired(), Length(min=2, max=60)])

    submit = SubmitField('Update Food')

app= Flask(__name__)

app.config['SECRET_KEY'] = 'Alican secret key'

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
    
@app.route("/view/<int:food_id>",methods=['GET','POST'])
def viewfoods(food_id):

    db = sqlite3.connect('usda_foods.db')
    d = db.cursor()
    d.execute('''SELECT * FROM food JOIN food_group ON  
    food.food_group_id=food_group.id
    JOIN weight ON food.id=weight.food_id
    JOIN nutrition ON food.id=nutrition.food_id;''')

   
    

    group_name = d.fetchall()

    

    for i in range(0,len(group_name)-1):
        if group_name[i][0] == food_id:
            find = group_name[i]

    return render_template('viewfoods.html',foods=find)

@app.route("/update/<int:food_id>/<int:group_id>",methods=['GET','POST'])
def updatefood(food_id,group_id):

    db = sqlite3.connect('usda_foods.db')
    d = db.cursor()
    d.execute('''SELECT * FROM food WHERE id=?;''',[food_id])

    form = Update()

    if (form.validate_on_submit()):
        kursor = db.cursor()
        kursor.execute('''UPDATE food SET
            long_desc=?, short_desc=?, manufac_name=?, sci_name=?  
            WHERE id=?''',(form.long_desc.data,form.short_desc.data,
            form.manufac.data,form.scien.data,food_id))
        db.commit()

    m = db.cursor()
    m.execute('SELECT * FROM food_group')

    kursor = db.cursor()
    kursor.execute('''UPDATE food SET
            food_group_id=? WHERE id=?''',(group_id,food_id))
    print(group_id)
    db.commit()

    
    return render_template('updatefoods.html',form=form, foods=d.fetchall(), groups=m.fetchall()) 

    
 
    

     
 
  
  




if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080, debug=True)

    