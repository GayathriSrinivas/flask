from flask import render_template
from flask import request

from flask import Flask
app = Flask(__name__)


@app.route('/form')
def input_page():
	return render_template('input.html') 


@app.route('/sum', methods=['POST'])
def sum():
	a = request.form['a']
	b = request.form['b']
	output = int(a) + int(b)
	return render_template('input.html',a=a,b=b,output=output)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
