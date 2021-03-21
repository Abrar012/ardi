from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def add_save_to_db(db):

    def save(model):
        try:
            db.session.add(model)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            db.session.close()
            return False, 'Duplicate ID'
        return True, 'Created'
    db.Model.save = save

add_save_to_db(db)


@app.route("/", methods=["GET"])
def Home():
    return render_template("home.html")

@app.route('/index')
def main():
	return render_template('index.html')

@app.route('/game')
def game():
	return render_template('game.html')

@app.route('/saveTime', methods = ['GET', 'POST'])
def saveTime():
    if request.method == 'POST':
        from models import User
        result = request.form.to_dict()
        task = User(**result)
        task.save()
        return render_template('saveTime.html')
    else:
        pass

@app.route('/score', methods = ['GET','POST'])
def score():
	if request.method == 'POST':
		from models import UserDetails
		result = request.form.to_dict()
		task = UserDetails(**result)
		task.save()

	if request.method == 'POST':
		global userName
		userName = request.form['userName']
		userName = userName.upper()
		print (userName)
		global endTime
		to_insert = ((userName),(endTime),) # because this needs to be a tuple
		conn = sqlite3.connect('gameTimeDatabase.db')
		c = conn.cursor()
		c.execute("INSERT INTO times VALUES (?,?)", to_insert)
		conn.commit()
		allTimes = c.execute("SELECT * FROM times ORDER BY time")
		conn.commit()

		def from_sqlite_Row_to_dict(list_with_rows):
	    # '''Turn a list with sqlite3.Row objects into a dictionary'''
		    d = {} # the dictionary to be filled with the row data and to be returned

		    for i, row in enumerate(list_with_rows): # iterate throw the sqlite3.Row objects            
		        l = {} # for each Row use a separate list
		        l['name'] = str(row[0])
		        l['time'] = str(row[1])
		        d[i] = l   
		    return d

		timeDict = from_sqlite_Row_to_dict(allTimes)

	return render_template('score.html', times = timeDict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)