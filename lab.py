import sqlite3, json, random
from flask import Flask, render_template, send_from_directory, request, make_response, redirect

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/home', methods=['get', 'post'])
def home():

    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('''
        SELECT username, password from users where username=? and password=? ;
    ''', (request.cookies.get('username'), request.cookies.get('password')))
    rows = cur.fetchall()
    if len(list(rows))==0:
        login_successful=False
    else:
        login_successful=True


    cur.execute('''
        SELECT sender_id, message, created_at, id from messages;
    ''')
    rows = cur.fetchall()
    messages = []
    for row in rows:
        messages.append({'username': row[0], 'text': row[1], 'created_at':row[2], 'id':row[3]})
    messages.reverse()

    #if request.method == 'GET':
    if request.form.get('delete'):
        print('success!!!!!!!!!!!!!!!')

    if login_successful:
        return render_template('home.html',username=request.cookies.get('username'), password=request.cookies.get('password'), messages=messages)
    else:
        return render_template('home.html', messages=messages)


@app.route('/home.json')
def home_json():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('''
        SELECT sender_id, message, created_at, id from messages;
    ''')
    rows = cur.fetchall()
    messages = []
    for row in rows:
        messages.append({'username': row[0], 'text': row[1], 'created_at':row[2], 'id':row[3]})
    messages.reverse()

    return json.dumps(messages)


@app.route('/login', methods=['get', 'post'])
def login():

    if request.form.get('username'):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('''
            SELECT username, password from users where username=? and password=? ;
        ''', (request.form.get('username'), request.form.get('password')))
        rows = cur.fetchall()
        if len(list(rows))==0:
            login_successful=False
        else:
            login_successful =True

        if login_successful:
            res = make_response(render_template('login.html', login_successful = True, username=request.form.get('username'), password=request.form.get('password')))
            res.set_cookie('username', request.form.get('username'))
            res.set_cookie('password', request.form.get('password'))
            return res
        else:
            return render_template('login.html', login_unsuccessful = True)
    else:
        return render_template('login.html', login_default=True)


@app.route('/logout')
def logout():
    res = make_response(render_template('logout.html'))
    res.set_cookie('username', '', expires=0)
    res.set_cookie('password', '', expires=0)
    return res

@app.route('/create_message', methods=['get', 'post'])
def create_message():
    if(request.cookies.get('username') and request.cookies.get('password')):
        if request.form.get('newMessage'):
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute('''
                INSERT INTO messages (sender_id, message) values (?, ?);
            ''', (request.cookies.get('username'), request.form.get('newMessage')))
            con.commit()
            return make_response(render_template('create_message.html', created=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
        else:
            return make_response(render_template('create_message.html', created=False, username=request.cookies.get('username'), password=request.cookies.get('password')))
    else:
        return login()

@app.route('/sign_up', methods=['get', 'post'])
def sign_up():
    try:
        if request.form.get('username'):
            if request.form.get('password1') == request.form.get('password2'):
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                cur.execute('''
                    INSERT INTO users (username, password) values (?, ?);
                ''', (request.form.get('username'), request.form.get('password1')))
                con.commit()
                return make_response(render_template('sign_up.html', successful = True))

            else:
                return make_response(render_template('sign_up.html', successful = False, wrongPass = True))
        else:
            return make_response(render_template('sign_up.html'))
    except sqlite3.IntegrityError:
        return render_template('sign_up.html', taken=True, username=request.form.get('username'))


@app.route('/user')
def user():
    if(request.cookies.get('username') and request.cookies.get('password')):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('''
            SELECT message, created_at, id from messages where sender_id=?;
        ''', (request.cookies.get('username'),))
        rows = cur.fetchall()
        messages = []
        for row in rows:
            messages.append({'text': row[0], 'created_at': row[1], 'id':row[2]})
        messages.reverse()
        return make_response(render_template('user.html', messages=messages, username=request.cookies.get('username'), password=request.cookies.get('password')))
    else: 
        return login()


@app.route('/delete_message/<id>', methods=['GET'])
def delete_message(id):

    con = sqlite3.connect('database.db') 
    cur = con.cursor()
    cur.execute('''
        SELECT sender_id from messages where id=?;
    ''', (id,))
    rows = cur.fetchall()
    if rows[0][0] == request.cookies.get('username'):
        cur.execute('''
            DELETE from messages where id=?;
        ''', (id,))
        con.commit()
    else:
        return make_response(render_template('delete_message.html', not_your_message=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
    return make_response(render_template('delete_message.html', username=request.cookies.get('username'), password=request.cookies.get('password')))

@app.route('/edit_message/<id>', methods=['POST', 'GET'])
def edit_message(id):
    if request.form.get('newMessage'):
        con = sqlite3.connect('database.db') 
        cur = con.cursor()
        cur.execute('''
            SELECT sender_id, message from messages where id=?;
        ''', (id,))
        rows = cur.fetchall()
        if rows[0][0] == request.cookies.get('username'):
            cur.execute('''
                UPDATE messages
                SET message = ?
                WHERE id = ?
            ''', (request.form.get('newMessage'),id))
            con.commit()
            return make_response(render_template('edit_message.html',allGood=True, id=id, username=request.cookies.get('username'), password=request.cookies.get('password')))
        else:
            return make_response(render_template('edit_message.html',not_your=True, id=id, username=request.cookies.get('username'), password=request.cookies.get('password')))
    else:
        return make_response(render_template('edit_message.html',default=True, id=id, username=request.cookies.get('username'), password=request.cookies.get('password')))

@app.route('/delete_account/<username>')
def delete_account(username):
    if request.cookies.get('username') == username:
        con = sqlite3.connect('database.db') 
        cur = con.cursor()
        cur.execute('''
            DELETE from users where username=?;
        ''', (username,))
        con.commit()
        return make_response(render_template('delete_account.html', not_your_username=False, username=request.cookies.get('username'), password=request.cookies.get('password')))
    else:
        return make_response(render_template('delete_account.html', not_your_username=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
    

@app.route('/change_password/<username>', methods=['post', 'get'])
def change_password(username):
    if request.form.get('oldPassword'):
        if request.cookies.get('username') == username:
            con = sqlite3.connect('database.db') 
            cur = con.cursor()
            cur.execute('''
                SELECT password from users where username=?;
            ''', (username,))
            rows = cur.fetchall()
            oldPassword = rows[0][0]
            
            if request.form.get('oldPassword') == oldPassword:
                if request.form.get('password1') == request.form.get('password2'):
                    cur.execute('''
                        UPDATE users
                        SET password = ?
                        WHERE username = ?
                    ''', (request.form.get('password1'), request.cookies.get('username')))
                    con.commit()
                    return make_response(render_template('change_password.html', allGood=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
                else: 
                    return make_response(render_template('change_password.html', repeatPass=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
            else: 
                return make_response(render_template('change_password.html', wrongPass=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
        else: 
            return make_response(render_template('change_password.html', not_your_username=True, username=request.cookies.get('username'), password=request.cookies.get('password')))
    else: return make_response(render_template('change_password.html', username=request.cookies.get('username'), password=request.cookies.get('password')))


@app.route('/search_message', methods=['POST', 'GET'])
def search_message():
    if request.form.get('search'):
        con = sqlite3.connect('database.db') 
        cur = con.cursor()
        cur.execute('''
            SELECT sender_id, message, created_at, id from messages;
        ''')
        rows = cur.fetchall()
        messages = []
        for row in rows:
            if request.form.get('search') in row[1]:
                messages.append({'username': row[0], 'text': row[1], 'created_at':row[2], 'id':row[3]})
        messages.reverse()
        return render_template('search_message.html', messages=messages, username=request.cookies.get('username'), password=request.cookies.get('password'))
    else:
        return render_template('search_message.html', default=True, username=request.cookies.get('username'), password=request.cookies.get('password'))
    

@app.route('/static/<path>' )
def static_directory(path):
    return send_from_directory('static', path)


    
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
  return render_template('500.html'), 500



def populate():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for i in range(20):
        username = 'user_' + str(random.randint(1, 100)) + '_' + str(random.randint(1, 100)) + '_' + str(random.randint(1, 100))
        password = 'pass_' + str(random.randint(1, 100)) + '_' + str(random.randint(1, 100))
        cur.execute('''INSERT INTO users (username, password) values (?, ?);''', (username, password))
        con.commit()
        for k in range(20):
            post =  random.choice([generate_comment_5(), generate_comment_4(), generate_comment_3(), generate_comment_2(), generate_comment_1(), generate_comment_0()])
            cur.execute('''INSERT INTO messages (sender_id, message) values (?, ?);''', (username, post))
            con.commit()
    print('done')



def generate_comment_0():
    whoList = ["Many people", "A lot of Americans", "People around the world", "Most citizens"]
    who = random.choice(whoList)
    nameList = ["Biden", "Joe Biden", "Daddy Biden", "Joseph Biden"]
    name = random.choice(nameList)
    jobList = ["president", "head of the USA", "supreme ruler of America", "white supremacy destroyer"]
    job = random.choice(jobList)
    exampleList = ["For example", "For instance", "To illustrate", "In particular"]
    example = random.choice(exampleList)
    planList = ["plans", "strategy", "commitment", "determination"]
    plan = random.choice(planList)
    text = who + " support " + name + " as a " + job + " because he has real plans fo the future. " + example + ", look at " + name + "'s " + plan + " to fight the climate change."
    return text
def generate_comment_1():
    nameList = ["Biden", "Joe Biden", "Daddy Biden", "Joseph Biden"]
    name = random.choice(nameList)
    whatList = ["decent human being", "respectful person", "thoughtful man", "rational guy"]
    what = random.choice(whatList)
    whoList = ["people of any background", "citizens of different countries", "people of varying cultures", "aliens"]
    who = random.choice(whoList)
    jobList = ["president", "head of the USA", "supreme ruler of America", "white supremacy destroyer"]
    job = random.choice(jobList)
    actionList = ["respect", "be considerate to", "understanding of", "patient with"]
    action = random.choice(actionList)
    text = name + " continues proving that he is a " + what + " being by carying about " + who + ". It is important for the " + job + " to " + action + " others."
    return text
def generate_comment_2():
    nameList = ["Biden", "Joe Biden", "Daddy Biden", "Joseph Biden"]
    name = random.choice(nameList)
    whatList = ["a depp background", "a lot of knowledge", "interesting thoughts", "a lot of experience"]
    what = random.choice(whatList)
    whereList = ["foreign policy", "foreign affairs", "international relations", "diplomatic policy"]
    where = random.choice(whereList)
    whoList = ["foreign leaders", "representatives from other countries", "international communities", "presidents of many countries"]
    who = random.choice(whoList)
    whichList = ["multi-cultural", "diverse", "broad-based", "multiethnic"]
    which = random.choice(whichList)
    text = name + " has " + what + " in " + where + " and understands the importance of cultivating relationships with " + who + " He will help create a " + which + " America!"
    return text
def generate_comment_3():
    nameList = ["Donald Trump", "Trump", "Orange Man", "The Racist Guy"]
    name = random.choice(nameList)
    whereList = ["America", "the United States", "the US", "USA"]
    where = random.choice(whereList)
    insultList = ["stupid", "unintelligent", "uneducated", "brainless"]
    insult = random.choice(insultList)
    text = name + " is the worst thing that happened to " + where + ". He is much more " + insult + " than he thinks."
    return text
def generate_comment_4():
    nameList = ["Donald Trump", "Trump", "Orange Man", "The Racist Guy"]
    name = random.choice(nameList)
    actionList = ["disregarded", "ignored", "neglected", "shut down"]
    action = random.choice(actionList)
    whatList = ["president", "head of the country", "politican", "authority figure"]
    what = random.choice(whatList)
    problemList = ["systematic racism", "police brutality", "white supremacy", "COVID-19"]
    problem = random.choice(problemList)
    text = name + " has completely " + action + " current problems such as " + problem + ", climate change and homelessness. He has no business being a " + what
    return text
def generate_comment_5():
    nameList = ["Donald Trump", "Trump", "Orange Man", "The Racist Guy"]
    name = random.choice(nameList)
    whoList = ["ordinary Americans", "normal citizens", "regualar humans", "American citizens"]
    who = random.choice(whoList)
    whenList = ["first 100 days", "first few months", "first few weeks", "first few hours (lol)"]
    when = random.choice(whenList)
    whichList = ["corporations and the wealthiest few", "big companies", "rich people", "billionairs"]
    which = random.choice(whichList)
    which2List = ["everyone else", "poor people", "middle class workers", "regular citizens"]
    which2 = random.choice(which2List)
    text = "After months of campaign promises to help " + who + ", " + name + "'s " + when + " have revealed that his true policy priorities are benefitting " + which + "at the expense of " + which2 + "!"
    return text

#populate()

app.run(host= '0.0.0.0')