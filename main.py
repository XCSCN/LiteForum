from flask import Flask, request, Response
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app = Flask('app')
topics = {}
topicidx = []
from random import random
from flask_cors import CORS

CORS(app)
usrs = {}
tokens = {}

with open("usrs", "r") as a:
	usrs = eval(a.read())
with open("topics", "r") as b:
	topics = eval(b.read())
with open("topicidx", "r") as c:
	topicidx = eval(c.read())

@app.route('/lo')
def los():
	if request.cookies.get("token") in tokens:
		return "True"
	else:
		return '<form action="/login" method="GET">Name:<input name="name" required></input><br>Password:<input name="pwd" required></input><br><button type="submit">Login</button></form><br><a href="/signupfront">I don\'t have an account!</a>'


@app.route('/login')
def login():
	if usrs.get(request.args.get("name")) == request.args.get("pwd"):
		res = Response("True")
		rd = str(random())
		tokens[rd] = request.args.get("name")
		res.set_cookie("token", rd, 86400 * 30)
		return res
	else:
		return '<script>location.href="https://LiteFourmPython.xiaocai12345.repl.co/lo"</script>'


@app.route('/signupfront')
def suf():
	return '<form action="/signup" method="GET">Name:<input name="name" required></input><br>Password:<input name="pwd" required></input><br><button type="submit">Signup</button></form><br><a href="/lo">I have an account!</a>'


@app.route('/signup')
def signup():
	if request.args.get("name") and usrs.get(request.args.get("name")) == None:
		usrs[request.args.get("name")] = request.args.get("pwd")
		dump()
		res = Response("True")
		rd = str(random())
		tokens[rd] = request.args.get("name")
		res.set_cookie("token", rd, 86400 * 30)
		return res
	else:
		return '<script>location.href="https://LiteFourmPython.xiaocai12345.repl.co/signupfront"</script>'


@app.route('/load')
def load():
	global usrs, topics, topicidx
	with open("usrs", "r") as a:
		usrs = eval(a.read())
	with open("topics", "r") as b:
		topics = eval(b.read())
	with open("topicidx", "r") as c:
		topicidx = eval(c.read())
	return 'load'


@app.route('/dump')
def dump():
	global usrs
	with open("usrs", "w") as a:
		a.write(repr(usrs))
	with open("topics", "w") as b:
		b.write(repr(topics))
	with open("topicidx", "w") as c:
		c.write(repr(topicidx))
	return 'dump'


@app.route('/api')
def api():
	if request.cookies.get("token") in tokens:
		return tokens[request.cookies.get("token")]
	else:
		return 'False'


def header():
	login = api()
	if login == "False":
		return '<a href="/lo">login or signup</a>'
	else:
		return "hello," + login + "<hr>"


@app.route('/')
def home():
	return header(
	) + '<form method="GET" action="/topic"><input name="name" required><br><select name="type" required><option value ="uncategorized">Uncategorized</option><option value ="help request">help request</option><option value ="tutorials">tutorials</option></select><br><textarea name="content" required></textarea><button type="submit">Post</button></form>'


@app.route('/topic')
def topic():
	if api() == "False":
		return "Not logged in!"
	if request.args["name"] in topicidx:
		return "Duplicate topic name!"
	topics[request.args["name"]+'-'+request.args["type"]] = [
		request.args["content"].lower().replace("<", "&lt;").replace(
			">",
			"&gt;").replace("(i", '<img src="').replace(")/i", '">').replace(
				"onerror", "******").replace("javascript:", "***********")
	]
	topicidx.append(request.args["name"]+'-'+request.args["type"])
	dump()
	return header(
	) + 'Redirecting...<script>location.href="https://LiteFourmPython.xiaocai12345.repl.co/topic/' + str(
		len(topicidx) - 1) + '";</script>'


@app.route('/topic/<num>')
def topicfront(num):
	res = header() + '<h1>' + topicidx[int(num)] + '</h1><hr><p>'
	for i in topics[topicidx[int(num)]]:
		res += i + '</p><hr>'
	res += '<form method="GET" action="/reply">reply to topic <input name="name" value=' + num + '>:<textarea name="content"></textarea><button type="submit">Post</button>'
	return res


@app.route('/reply')
def reply():
	if api() == "False":
		return "Not logged in!"
	topics[topicidx[int(request.args["name"])]].append(
		api()+":"+request.args["content"].lower().replace("<", "&lt;").replace(
			">",
			"&gt;"))
	dump()
	return header(
	) + 'Redirecting...<script>location.href="https://LiteFourmPython.xiaocai12345.repl.co/topic/' + request.args[
		"name"] + '";</script>'


app.run(host='0.0.0.0', port=8080)