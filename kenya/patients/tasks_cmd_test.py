#set up Django
import os,sys,datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

setup_environ(settings)

import backend.models as backend
import patients.tasks as tasks
import patients.models as patients


CON = {c.name:c for c in backend.Condition.objects.all()}
LANG = {l.name:l for l in backend.LanguageGroup.objects.all()}
STUD = {g.name:g for g in backend.StudyGroup.objects.all()}

def make_client(name="Default",condition=CON['adolescent'],language=LANG['kiswahili'],study_group = STUD['one_way'],week=20):
	return patients.Client(
		first_name = "%s %s"%(name,week),
		due_date=datetime.date.today()+datetime.timedelta(weeks=40-week),
		condition = condition,
		language = language,
		study_group = study_group
	)

#infinte loop to test weeks of message	
def test_get_message():
	while True:
		week = int(raw_input("Week: "))
		tasks.get_message(make_client(week=week))
		
def test_get_clients():
	while True:
		day = int(raw_input("Day: "))%7
		now = datetime.datetime.fromordinal(datetime.date.today().toordinal()) + datetime.timedelta(hours=8)
		c1 = tasks.get_clients_to_message(now=now+datetime.timedelta(days=day))
		c2 = tasks.get_clients_to_message(now=now+datetime.timedelta(days=day)+datetime.timedelta(hours=5))
		c3 = tasks.get_clients_to_message(now=now+datetime.timedelta(days=day)+datetime.timedelta(hours=11))
		print c1
		print c2
		print c3
	
test_get_clients()


