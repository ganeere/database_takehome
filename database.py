import sqlite3
db = sqlite3.connect('usda_foods.db')

cur = db.cursor()
cur.execute("DROP TABLE IF EXISTS 'food'")
cur.execute("""CREATE TABLE 'food'(
  id int PRIMARY KEY NOT NULL,
  food_group_id int REFERENCES food_group(id) NOT NULL,
  long_desc text NOT NULL DEFAULT '',
  short_desc text NOT NULL DEFAULT '',
  common_names text NOT NULL DEFAULT '',
  manufac_name text NOT NULL DEFAULT '',
  survey text NOT NULL DEFAULT '',
  ref_desc text NOT NULL DEFAULT '',
  refuse int NOT NULL,
  sci_name text NOT NULL DEFAULT '',
  nitrogen_factor float NOT NULL,
  protein_factor float NOT  NULL,
  fat_factor float NOT NULL,
  calorie_factor float NOT NULL
);""")
f = open('text/FOOD_DES.txt', 'r')
cont = f.read()
f.close()

rows = cont.split('\n')
#rows = rows[1:]   delete first row with captions
formatteds = [tuple(x.split('^')) for x in rows]

for i in range(0,len(formatteds)-1):
  cur.execute("""INSERT INTO food (id, food_group_id, long_desc,short_desc,common_names,manufac_name,survey
  ,ref_desc,refuse,sci_name,nitrogen_factor,protein_factor,fat_factor,calorie_factor) 
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",formatteds[i])
  
db.commit()
#for FD_GROUP

cur1 = db.cursor()
cur1.execute("DROP TABLE IF EXISTS 'food_group'")
cur1.execute("""CREATE TABLE 'food_group'(
  id int PRIMARY KEY NOT NULL,
  name text NOT NULL
);""")

f = open('text/FD_GROUP.txt', 'r')
cont1 = f.read()
f.close()

rows = cont1.split('\n')
#rows = rows[1:]   delete first row with captions
formatteds1 = [tuple(x.split('^')) for x in rows]
for i in range(0,len(formatteds1)-1):
  cur1.execute("""INSERT INTO food_group (id, name) 
  VALUES (?,?)""",formatteds1[i])

db.commit()
#for Nut_Data

cur2 = db.cursor()
cur2.execute("DROP TABLE IF EXISTS `nutrition`")
cur2.execute("""CREATE TABLE `nutrition` (
  food_id int REFERENCES food(id) NOT NULL,
  nutrient_id int REFERENCES nutrient(id) NOT NULL,
  amount float NOT NULL,
  num_data_points int NOT NULL,
  std_error float,
  source_code text NOT NULL,
  derivation_code text,
  reference_food_id REFERENCES food(id),
  added_nutrient text,
  num_studients int,
  min float,
  max float,
  degrees_freedom int,
  lower_error_bound float,
  upper_error_bound float,
  comments text,
  modification_date text,
  confidence_code text,
  PRIMARY KEY(food_id, nutrient_id)
);""")

f = open('text/NUT_DATA.txt', 'r')
cont2 = f.read()
f.close()

rows = cont2.split('\n')

formatteds2 = [tuple(x.split('^')) for x in rows]
for i in range(0,len(formatteds2)-1):
  cur2.execute("""INSERT INTO nutrition (food_id, nutrient_id,amount,num_data_points,std_error,source_code,
  derivation_code,reference_food_id,added_nutrient,num_studients,min,max,degrees_freedom,lower_error_bound
  ,upper_error_bound,comments,modification_date,confidence_code) 
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",formatteds2[i])

db.commit()

#for weight
cur3 = db.cursor()
cur3.execute("DROP TABLE IF EXISTS `weight`")
cur3.execute("""CREATE TABLE 'weight'(
    food_id int REFERENCES food(id) NOT NULL,
    sequence_num int NOT NULL,
    amount float NOT NULL,
    description text NOT NULL,
    gm_weight float NOT NULL,
    num_data_pts int,
    std_dev float,
    PRIMARY KEY(food_id, sequence_num)
);""")

f = open('text/WEIGHT.txt', 'r')
cont3 = f.read()
f.close()

rows = cont3.split('\n')
#rows = rows[1:]   delete first row with captions
formatteds3 = [tuple(x.split('^')) for x in rows]
for i in range(0,len(formatteds3)-1):
  cur1.execute("""INSERT INTO weight (food_id, sequence_num,amount,description,gm_weight,num_data_pts
  ,std_dev) 
  VALUES (?,?,?,?,?,?,?)""",formatteds3[i])

db.commit()







db.close()
