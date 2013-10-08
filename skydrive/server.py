from flask import *
import urllib2
import json

SECRET_KEY = 'synergy'
app = Flask(__name__)
app.config.from_object(__name__)

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

@app.route('/login')
def input_page():
	return render_template('login.html') 

@app.route('/callback')
def callback():
	return render_template('callback.html')


@app.route('/access_token')
def skydrive_access_token():
	session["token"] = request.args.get('token','')
	print session["token"]
	return redirect(url_for('list_files'))	

@app.route('/list_files')
def list_files():
	token = session["token"	]
	try:
		folder = request.args.get('folder')
	except KeyError:
		print "no folder variable"

	if(folder == None):
		raw_data = urllib2.urlopen("https://apis.live.net/v5.0/me/skydrive/files?access_token=%s" % token).read()
	else:
		raw_data = urllib2.urlopen("https://apis.live.net/v5.0/%s/files?access_token=%s" % (folder,token)).read()

	response = json.loads(raw_data)		
	listFiles = []
	
	for record in response["data"]:
		fileRecord = {}
		fileRecord["id"]=record["id"]
		fileRecord["name"]=record["name"]
		fileRecord["raw_link"]=record.get("source","")
		fileRecord["size"]=sizeof_fmt(int(record["size"]))
		listFiles.append(fileRecord)
	
	return render_template('list_files.html',listFiles=listFiles)
	#raw_data1 = urllib2.urlopen("https://apis.live.net/v5.0/me/skydrive/quota?access_token=%s" % token).read()
	#quota = json.loads(raw_data1)
	#quota_mb = sizeof_fmt(int(quota["available"]))
	#return render_template('page.html',response=response,quota=quota_mb)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
