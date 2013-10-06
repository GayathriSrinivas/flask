from flask import render_template
from flask import request
import urllib2
import json

from flask import Flask
app = Flask(__name__)


@app.route('/login')
def input_page():
	return render_template('login.html') 

@app.route('/callback')
def callback():
	return render_template('callback.html')


@app.route('/access_token')
def fb_accessToken():
	token = request.args.get('token','')
	raw_data = urllib2.urlopen("https://graph.facebook.com/me?access_token=%s" % token).read()
	data = json.loads(raw_data)
	image_url = "https://graph.facebook.com/%s/picture" % data["id"]
	return render_template('page.html',user=data["name"],img_url=image_url)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
