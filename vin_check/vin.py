import requests
import re
from flask import Flask, render_template, request, send_from_directory
from bs4 import BeautifulSoup
from pandas import DataFrame
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

def split_vin(vin_str):
	vin_list = vin_str.split(",")
	return vin_list

def check_vin(vin):
	v_info=[]
	crash_data=[]
	url = 'http://cmvid.nisrinc.com/CMV_ID/CMV_ID.asp'
	post_data = {
	    'inputVIN':vin,
	    'x':'31'
	    #'y':'16'
	    #'displayType':'NONE'
	}
	# 提交并获取返回数据
	post_html = requests.post(url,data=post_data)
	#print (post_html.text)
	#对返回数据进行分析
	soup = BeautifulSoup(post_html.content,'html.parser')
	p=soup.find_all("table", class_ ='block2')
	content_list=p[0].find_all("td")
	#找到表格内容
	#print("table info : ",content_list)
	for i in range(len(content_list)):
		if i%2 == 0:
			v_info.append(str(content_list[i])[4:-5])
		else:
			crash_data.append(str(content_list[i])[4:-5])
#	print("v-info : ",v_info, len(v_info))
#	print("crash-data : ",crash_data,len(crash_data))
	return (v_info + crash_data)

def search_vin(vin_list):
	#make a dataframe
	header = ['VIN','WMI','MAKE','MODEL','AXLES','TYPE','GVWR1','Config1','Config2','Config3','Config4','Config5','Config6','GVWR2']
	df =  DataFrame(columns=header)
	print (vin_list)
	for i in vin_list:
		df.loc[len(df)] = check_vin(i)
	df.to_csv("result.csv")
	return (df)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/check/',methods=['POST'])
def check():
	if request.method == 'POST':
		if request.form['vin'] != '0':
			vin_list = split_vin(request.form['vin'])
			l = search_vin(vin_list)
			print (type(l))
			return render_template("index.html",error="CSV Generate Success")
			#return render_template("index.html",error=request.form['vin'])
		else:
			return render_template("index.html",error="bad input")
	else:
		return render_template("index.html")

@app.route("/download/")
def download_file():
	directory=os.getcwd()
	return send_from_directory(directory, 'result.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9000,debug=app.debug)

#split_vin("1M8TRMPAXZP060950,1M8TRMPAXZP060950")
#check_vin("1M8TRMPAXZP060950")

