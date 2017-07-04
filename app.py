from flask import Flask, render_template, request, url_for, session, redirect
from flask_pymongo import PyMongo
app = Flask(__name__)

import webbrowser as wb

app.config['MONGO_DBNAME'] = 'hackon_db'
app.config['MONGO_URI'] = 'mongodb://dipjal:dipjal123@ds145952.mlab.com:45952/hackon_db'

ADMINS = ['dipjal@hackerrank.com' , 'rishabh.jain@hackerrank.com']


mongo = PyMongo(app)

if mongo is not None :
	print 'Connection Successful'
else :
	print 'Connection Failed'

@app.route('/start_contest' , methods = ['GET' , 'POST'])
def start_contest():
    if request.method == 'POST':
        db = mongo.db.contests
        contest_id = request.form['data_id2']
        contest = db.find_one({'contest_id': contest_id})
        cnt = 0
        for tup in contest['participants']:
            if tup[1] == 1:
                cnt += 1
        if cnt > 1:
            db.update(contest , {"$set": {'status': 'Started'}})
            url = 'https://www.hackerrank.com/challenges/a-very-big-sum'
            wb.open(url)
            return 'Contest Started !! '
        else:
            return 'Sorry, contest cannot be started. There should be atleast two users participating.'


@app.route('/create' , methods = ['GET' , 'POST'])
def create():
	if request.method == 'POST':
		db = mongo.db.contests
		contest_name = request.form['contest_name']
		team_size = request.form['dropdown']
		team_size = int(team_size)
		users = [0] * team_size
		user_tuple = []
		if 'username' in session:
			print session['username']
		for i in xrange(team_size):
			user_name = 'user_';
			user_name += str(i + 1);
			users[i] = request.form[user_name]
			if users[i] == session['username']:
				tup1 = (users[i] , 1)
			else:
				tup1 = (users[i] , 0)
			user_tuple.append(tup1)

		db.insert(
			{'contest_name' : contest_name , 
			'contest_id' : request.form['contest_id'],
			'participants' : user_tuple,
			'contest_creator': session['username']})

		db = mongo.db.users
	
		for user in users:

			user_found = db.find_one({'username' : user})
			if user_found is not None:
				contest_list = user_found['contest_list']
				if user == session['username']:
					tup1 = (request.form['contest_id'],1)
				else:
					tup1 = (request.form['contest_id'],0)	
				contest_list.append(tup1)
				db.update({'username':user} , {'$set' : {'contest_list' : contest_list}})
			else:
				contest_list = []
				if user == session['username']:
					tup1 = (request.form['contest_id'] , 1)
				else :
					tup1 = (request.form['contest_id'] , 0)

				contest_list.append(tup1)
				db.insert({'username': user, 'contest_list' : contest_list})  

		return render_template('participants.html')




@app.route('/accept_request', methods = ['GET', 'POST'])
def req():
	cid = 0
	if(request.method != 'POST'):
		if 'username' in session:
			session.pop('username' , None)
		return render_template('home.html')
	cid = request.form['data_id']
	db = mongo.db.users
	user = db.find_one({'username': session['username']})
	contest_list = user['contest_list']
	for tup in contest_list:
		if tup[0] == cid:
			tup[1] = 1

	db.update({'username':user['username']} , {'$set' : {'contest_list' : contest_list}})
	active_contest = []
	pending_contest = []
	contest_hosted = []

	db2 = mongo.db.contests
	contest = db2.find_one({'contest_id' : cid})
	
	#Check status here

	part = contest['participants']
	for tup in part:
		if(tup[0] == session['username']):
			print "here"
			tup[1] = 1;

	db2.update({'contest_id':cid} , {'$set' : {'participants' : part}})
	

	for tup in user['contest_list']:
		if tup[1] == 1:
			active_contest.append(tup[0])
			contest = db2.find_one({'contest_id': tup[0]})
			host = contest['contest_creator']
			if session['username'] == host:
				contest_hosted.append(tup[0])
		else:
			pending_contest.append(tup[0])
	
	return render_template('menu.html' , login_user = session['username'] , active = active_contest , pending = pending_contest , contest_hosted = contest_hosted)


@app.route('/contest')
def transfer():
	return render_template('create_contest.html' , user = session['username'])


@app.route('/create_contest' , methods = ['GET' , 'POST'])
def create_contest():
	if(request.method == 'POST') :
		return render_template('create_contest.html' , user = request.form['contest_creator'])

@app.route('/menu' , methods = ['GET' , 'POST'])
def menu():
    if request.method == 'POST':
        session['username'] = request.form['contest_creator']
        db = mongo.db.users
        user = db.find_one({'username': session['username']})
        if user is None:
            db.insert({
                'username' : session['username'],
                'contest_list' : []
                })
        user = db.find_one({'username': session['username']})
        
        active_contest = []
        pending_contest = []
        contest_hosted = []

        db2 = mongo.db.contests

        for tup in user['contest_list']:
                if tup[1] == 1:
                    active_contest.append(tup[0])
                    contest = db2.find_one({'contest_id': tup[0]})
                    host = contest['contest_creator']
                    if session['username'] == host:
                        contest_hosted.append(tup[0])
                else:
                    pending_contest.append(tup[0])

        session['username'] = request.form['contest_creator']
    	return render_template('menu.html' , login_user = session['username'] , active = active_contest , pending = pending_contest , contest_hosted = contest_hosted)
    return "true"

@app.route('/')
def home():
	if 'username' in session:
		session.pop('username' , None)
	return render_template('home.html')


if __name__ == "__main__":
	app.secret_key = 'hackOn2017'
	app.run(debug = True)
	