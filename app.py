from flask import Flask,request,redirect,url_for,render_template,session,send_from_directory
import os
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
import requests
from bs4 import BeautifulSoup

app=Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
csrf = CSRFProtect(app)


def check_login(sid,cid,bir):
    res = requests.get('http://www.yphs.tp.edu.tw/tea/tu2.aspx')
    soup = BeautifulSoup(res.text, "lxml")
    VIEWSTATE=soup.find(id="__VIEWSTATE")
    VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")
    EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")
    res=requests.post('http://www.yphs.tp.edu.tw/tea/tu2.aspx', allow_redirects=False, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),'chk_id':'學生／家長','tbx_sno':sid,'tbx_sid':cid,'tbx_sbir':bir,'but_login_stud':'登　　入'})
    cook=res.cookies['ASP.NET_SessionId']
    return

@app.route('/flask/')
def index():
	if(session.get('sid')==None):
		return redirect(url_for('login'))
	return "you auth了,學號{}<br>登入到競賽系統的密碼:<br>帳: {}<br>密: {}".format(str(session['sid']),"還沒拿到","就沒拿到齁")

@app.route('/flask/login',methods=["GET","POST"])
def login():
	if(request.method=='GET'):
		if(session.get('username')!=None):
			return redirect(url_for('index'))
		return render_template('login.html')
	elif(request.method=='POST'):
		sid=request.form.get('sid')
		cid=request.form.get('cid')
		bir=request.form.get('bir')
		try:
			check_login(sid,cid,bir)
			session.clear()
			session['sid']=request.form.get('sid')
			session.permanent = True
			return redirect(url_for('index'))
		except:
			return '你輸入的登入資料有誤qq<a href="./login">重新登入</a>'

if __name__=="__main__":
	app.run(port=6000)
