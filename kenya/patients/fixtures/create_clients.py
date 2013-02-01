import json,random,string,sys

def client(i,f,l,n):
	return {
        "pk": i, 
        "model": "patients.client", 
        "fields": {
             "last_name": "Prrier", 
            "relationship_status": "Married", 
            "living_children": 0, 
            "urgent": False, 
            "sent_messages": [], 
            "send_time": 13, 
            "id": 2, 
            "next_visit": "2013-03-15", 
            "first_name": "Trevor", 
            "last_msg": None, 
            "sec_contact_name": "", 
            "send_day": 3, 
            "pri_contact_name": "LKjd", 
            "sec_contact_number": 254, 
            "pri_contact_number": 254, 
            "pending": 0, 
            "phone_number": "254", 
            "due_date": "2013-07-10", 
            "previous_pregnacies": 1, 
            "years_of_education": 1, 
            "nickname": "Siay", 
            "partner_first_name": "", 
            "signup_date": "2013-02-01", 
            "study_group": 1, 
            "conditions": [], 
            "partner_last_name": "", 
            "birth_date": "1990-07-03", 
            "pregnancy_status": "Pregnant", 
            "phone_network": "safaricom",
            "language":"English"
        }
    }
    
def due_date():
	return "2013-%02i-%02i"%(random.randint(1,12),random.randint(1,28))
	
def birth_date():
	return "19%i-%02i-%02i"%(random.randint(70,92),random.randint(1,12),random.randint(1,28))

def client_names(num):
	for n in range(1,num+1):
		name = name_from_num(n)
		yield (n,"%s_first"%name,"%s_last"%name,name)
	
letters = '1'+string.ascii_uppercase
def name_from_num(i):
	out = ''
	while i>0:
		r = i%26
		out = letters[r]+out
		i = i/26
	return out

clients = []
for c in client_names(int(sys.argv[1])):
	clients.append(client(*c))

pre = open("pre.txt")
for line in pre:
	print line
print json.dumps(clients,indent=4)[2:-2]
print "]" #post
