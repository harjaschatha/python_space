from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys


def clean_to_string(string):
        '''
        removes non ascii characters
        '''
        allowed='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'#alphabets
        allowed+=allowed.lower()#lowercase
        allowed+='!@#$%^&*()_+=-.,: '
        allowed+="'"
        allowed+='\n'
        new_str=''
        for i in string:
                if i in allowed:
                        new_str+=i
        return new_str


def scrape():
	driver = webdriver.Firefox()
	driver.implicitly_wait(10) # seconds
	driver.get("http://sscattendance.formistry.com/report/")

	program = driver.find_element_by_name("program")
	#find program list
	program_list=program.text
	program_list=program_list.split('\n')[1:]
	#program_list
	students={}#list of students
	for prg in program_list:
		print prg
		try:
			program.send_keys(Keys.DOWN)
			semester=driver.find_element_by_id('semester')
			semester.send_keys(Keys.END)
			month=driver.find_element_by_id('month')
			month.send_keys(Keys.DOWN)
			month.send_keys(Keys.ENTER)
			#now that the page is loaded
			papers=driver.find_elements_by_class_name('tbl_heading')
			n_list=[]
			for i in papers:
				n_list.append(clean_to_string(i.text))
			papers=[clean_to_string(i) for i in n_list[2:-3]]
			
			students[prg]=papers
		except Exception as e:
			if 'PROGRAMME' not in prg:
				print e
			else:
				try:
					program.send_keys(Keys.DOWN)
					semester=driver.find_element_by_id('semester')
					semester.send_keys(Keys.END)
					month=driver.find_element_by_id('month')
					month.send_keys(Keys.DOWN)
					month.send_keys(Keys.ENTER)
					#now that the page is loaded
					papers=driver.find_elements_by_class_name('tbl_heading')
					n_list=[]
					for i in names:
						n_list.append(clean_to_string(i.text))
					papers=n_list[2:-3]
					students[prg]=papers
				except Exception as e:
					if 'PROGRAMME' not in prg:
						print e
					#move on

	driver.close()
	#process the list
	#save the list
	path=os.path.join(os.getcwd(),'setup_support','papers')
	f=file(os.path.join(path,'paper_list'),'w')
	pickle.dump(students,f)
	f.close()
