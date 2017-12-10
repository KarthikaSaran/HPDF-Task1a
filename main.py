
import urllib2




import requests

from flask import Flask, render_template, jsonify, send_from_directory, send_file, request, current_app
from werkzeug.utils import redirect

app = Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/authors')
def authors():
    r = requests.get('https://jsonplaceholder.typicode.com/users')
    val = r.json()
    usernames=[]
    ids={}
    for item in val:
        usernames.append(item["username"])
        ids[item["username"]]=item["id"]
    return jsonify(usernames)

@app.route('/posts')
def posts():
    r = requests.get('https://jsonplaceholder.typicode.com/posts')
    val = r.json()
    return jsonify(val)

@app.route('/count')
def count():
    post = requests.get('https://jsonplaceholder.typicode.com/posts')
    post = post.json()
    users = requests.get('https://jsonplaceholder.typicode.com/users')
    users = users.json()
    user=[]
    count={}
    for item in post:
        if item["userId"] not in user:
            user.append(item["userId"])
            count[item["userId"]] = 1
        else:
            count[item["userId"]] = count[item["userId"]]+1
    for item in users:
        count[item["username"]] = count.pop(item["id"])

    return jsonify(count)

@app.route('/setcookie')
def setcookie():

    redirect_to_index = redirect('/')
    response = current_app.make_response(redirect_to_index)
    response.set_cookie('name', value='karthika')
    response.set_cookie('age', value='29')
    return "Success !! Cookie Set"

@app.route('/getcookies')
def getcookies():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    print name
    print age
    return jsonify(name,age)


@app.route('/robots.txt')
def opentxt():
    data = urllib2.urlopen('https://httpbin.org/deny')
    f=open("deny.txt","w")
    for lines in data.readlines():
        f.write(lines)
    f.close()
    return send_from_directory('.', 'deny.txt')



@app.route('/html')
def htmlpage():
    return render_template('page1.html')

@app.route('/image')
def image():
    return send_file('succ.jpg', mimetype='image/gif')

@app.route('/input')
def input():
    return render_template('form.html')

@app.route('/result',methods=['POST'])
def result():
    input = request.form['input']
    print input
    return "Your input is "+input

if __name__ == '__main__':
    app.run(debug=True)


