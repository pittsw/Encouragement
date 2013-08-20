import json,random,string,sys
from datetime import *

def client(id,lname,fname,number,dd,visit,time,day,group,condition,status):
	return {
		"pk": id, 
		"model": "patients.client", 
		"fields": {
		  "last_name": lname, 
		  "first_name":fname, 
		  "phone_number": "254"+number, 
		  "due_date": dd.strftime("%Y-%m-%d"), 
		  "next_visit": visit.strftime("%Y-%m-%d"), 
		  "send_time": time, 
		  "send_day": day, 
		  "id": id, 
		  "study_group":group, 
		  "condition": condition,
		  "pregnancy_status": status,
		  
		  "relationship_status": "Married", 
		  "living_children": 0, 
		  "urgent": False, 
		  "validated": True, 
		  "last_msg": "2013-02-19", 
		  "sec_contact_name": "second contact", 
		  "pri_contact_name": "primary contact", 
		  "sec_contact_number": "2542", 
		  "pri_contact_number": "2541", 
		  "pending": 0, 
		  "previous_pregnacies": 1, 
		  "years_of_education": 1, 
		  "nickname": "Hello", 
		  "partner_first_name": "Partner Name", 
		  "signup_date": "2013-02-19", 
		  "language": 9, 
		  "partner_last_name": "", 
		  "birth_date": "1990-02-20", 
		  "phone_network": "safaricom"
		}
	}


study_groups = ((6,"One Way"),(7,"Two Way"))
status = ("Pregnant","Post-Partum")
send_day = (0,1,2,3,4,5,6)
send_time = (8,13,19)
conditions = (1,2,3)


clients = []
count = 1
day = date.today()
#(id,lname,fname,number,dd,visit,time,day,group,condition,status)
for g in study_groups:
	for s in status:
		for d in send_day:
			for t in send_time:
				for c in conditions:
					clients.append(
						client(count,"%s-%s"%(d,t),s,"%s%s%s%s"%(d,t,c,count),day+timedelta((count%25)*7),day+timedelta((count%7)*7),t,d,g[0],c,s)
						)
					count+=1

print json.dumps(clients,indent=4)
