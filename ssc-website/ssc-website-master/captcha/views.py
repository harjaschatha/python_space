from django.http import HttpResponse
import json
import random
import hashlib
import captcha


def get_captcha(request):
	'''Returns a captcha string along with an answer hash.'''
	data={}
	if random.random()<0.5:#create a new captcha string and hash
		#
		x=random.choice(range(100))
		y=random.choice(range(100))
		op=random.choice(['+','-','x','>','<'])
		data['string']=string(x)+op+string(y)
		#see if it already exists
		try:
			cap=captcha.models.hash_table.objects.get(string=data['string'])
		except:#if does not exist
			answer=eval(data['string'])#find answer
			#
			q_hash=hashlib.md5(data['string'])
			a_hash=hashlib.md5(string(answer))
			#create a new entry
			new_hash=captcha.models.hash_table()
			new_hash.string=data['string']
			new_hash.hash=a_hash.hexdigest()
			new_hash.save()
			data['hash']=new_hash.hash
		else:
			data['hash']=cap.hash
	else:#return an existing captcha
		cap=captcha.models.hash_table.objects.all()
		cap=random.choice(cap)
		data['string']=cap.string
		data['hash']=cap.hash
	return HttpResponse(json.dumps(data),content_type='application/json')
	
def check_captcha(request):
	'''Returns a captcha submission and thus validates the humanity of the user'''
	if request.method=='POST':
		string=request.POST['string']
		hash=request.POST['hash']
		try:
			cap=captcha.models.hash_table.objects.get(string=string)
		except:
			return HttpResponse(json.dumps(False),content_type='application/json')
		else:
			if cap.hash=hash:	
				return HttpResponse(json.dumps(True),content_type='application/json')
			else:
				return HttpResponse(json.dumps(False),content_type='application/json')
