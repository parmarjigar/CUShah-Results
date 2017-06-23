import requests
from bs4 import BeautifulSoup
import csv
import re


results = "https://www.cushahuniversity.ac.in/show_results.php"
grades = "https://www.cushahuniversity.ac.in/show_gradesheet.php"
headers={
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate, sdch, br',
				'Accept-Language':'en-US,en;q=0.8',
				'Cache-Control':'max-age=0',
				'Connection':'keep-alive',
				'Host':'www.cushahuniversity.ac.in',
				'Referer':'https://www.cushahuniversity.ac.in/show_gradesheet.php',
				'Upgrade-Insecure-Requests':'1',
				# 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
			}
start="14te403001"
count=0
enrolls=[]

for i in range(0,5):
	c=start[:4]+ str(int(start[4:])+i)
	print c
	try:
		params= {
					'exam_session':'Winter Examination 2016',
					'exam_semester':'V',
					'txtENo':c,
					'cmdSubmit':'Show Result'
				}		
		r=requests.post(grades,headers=headers,data=params)
		soup=BeautifulSoup(r.content,'html.parser')
		
		
		
		trList=soup.findAll("tr")
		head=[4,8,10,42,43]
		points=[40,41]
		cpi=[]
		bl=[42,43]
		bg=[]
		finalhead=[]
		redefined=[]
		for tr in trList[0]:
			tdList = tr.find_all('td')
			for td in points:
				cpi.append(tdList[td].get_text())
		
		for tr in trList[0]:
			tdList = tr.find_all('td')
			for td in bl:
				bg.append(tdList[td].get_text())
		print bg		
		for tr in trList[0]:
			tdList = tr.find_all('td')
			for td in tdList:
				# print td.get_text()+"\n"
				redefined.append(td.get_text())
		for i in range(17,42):
			if "".join(re.split('\W+|-',redefined[i])).isalpha() and len(redefined[i].strip())>3:
				finalhead.append(i)
		# head.extend(finalhead)		
		head[3:3]=finalhead
		# print "jigar"
		# print head
		fieldnames=[]	
		for tr in trList[0]:
			tdList = tr.find_all('td')
			for td in head:
				fieldnames.append(tdList[td].get_text().encode('unicode_escape'))
			fieldnames[9]=(cpi[0].split(":")[0])
			fieldnames[10]=(cpi[1].split(":")[0])
			
		fieldnames.append("Result")
		fieldnames.append("Current Backlog")
		fieldnames.append("Total Backlog")
		
		# print fieldnames
		values=[5,9,11,16]		
		for i in range(17,42):
			if i not in head:
				values.append(i)
		# print values
		val=[]
		for tr in trList[0]:
			tdList = tr.find_all('td')
			for td in values:
				val.append(tdList[td].get_text().encode('unicode_escape'))
		val.append(cpi[0].split(":")[1])
		val.append(cpi[1].split(":")[1])
		print cpi[1].split(":")[1]
		if cpi[1].split(":")[1] > 4.0 and int(bg[0].split(":")[1])==0:
			res= "PASS"
		else:
			res="FAIL"
		
		# print len(val)
		if count==0:
				filetype="wb"
		else:
			filetype="ab"
		
		with open('result.csv', filetype) as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)		
			if count==0:
				writer.writeheader()
				count+=1
				
			writer.writerow({fieldnames[0] : val[0].split(" ")[1],fieldnames[1] : " ".join(val[1].split(" ")[1:]),fieldnames[2] : val[2].split(" ")[1],fieldnames[3] : val[4],fieldnames[4] : val[7],fieldnames[5] : val[10],fieldnames[6] : val[13],fieldnames[7] : val[16],fieldnames[8] : val[19],fieldnames[9] : val[23],fieldnames[10] : val[24],fieldnames[11] : res,fieldnames[12] : bg[0].split(":")[1],fieldnames[13] : bg[1].split(":")[1]})
	except Exception,e:
		print str(e)