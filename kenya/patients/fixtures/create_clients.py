import json,random,string,sys

def client(i,f,l,n):
	return {
        "pk": i, 
        "model": "patients.client", 
        "fields": {
            "phone_number": "", 
            "due_date": due_date(), 
            "first_name": f, 
            "last_name": l, 
            "relationship_status": "Married", 
            "last_msg": None, 
            "next_visit":None,
            "partner_name": ' ', 
            "nickname": n, 
            "years_of_education": 1, 
            "living_children": 0, 
            "send_day": random.randint(0,6), 
            "id": i*1000, 
            "urgent": False, 
            "sent_messages": [], 
            "birth_date": birth_date(), 
            "send_time": 13, 
            "previous_pregnacies": 0, 
            "pregnancy_status": "Pregnant", 
            "conditions": [], 
            "study_group": random.randint(0,2), 
            "pending": 0
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
