from flask import Flask, render_template, request
import convert
app = Flask(__name__)

@app.route('/', methods=["GET"])
def mainPage():
	return render_template('index.html')

@app.route('/', methods=["POST"])
def serveGIF():
	try :
		gifname = convert.convert(request.form.getlist('url')[0])
	except IndexError as e :
		return render_template('index.html')
	else :
		return render_template('return.html', gif = gifname)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000')
