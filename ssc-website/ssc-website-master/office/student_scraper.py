from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys

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
		try:
			program.send_keys(Keys.DOWN)
			semester=driver.find_element_by_id('semester')
			semester.send_keys(Keys.END)
			month=driver.find_element_by_id('month')
			month.send_keys(Keys.DOWN)
			month.send_keys(Keys.ENTER)
			#now that the page is loaded
			#pgsize = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pagesize")))
			pg_size=driver.find_element_by_id('pagesize')
			pg_size.send_keys(Keys.END)
			pg_size.send_keys(Keys.ENTER)
			names=driver.find_elements_by_class_name('s_name')
			n_list=[]
			for i in names:
				n_list.append(str(i.text))
			students[prg]=n_list
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
					#pgsize = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pagesize")))
					pg_size=driver.find_element_by_id('pagesize')
					pg_size.send_keys(Keys.END)
					pg_size.send_keys(Keys.ENTER)
					names=driver.find_elements_by_class_name('s_name')
					n_list=[]
					for i in names:
						n_list.append(str(i.text))
					students[prg]=n_list
				except Exception as e:
					if 'PROGRAMME' not in prg:
						print e
					#move on

	driver.close()
	#process the list
	#save the list
	path=os.path.join(os.getcwd(),'setup_support','student_photos','college_studentlist')
	f=file(os.path.join(path,'student_list'),'w')
	pickle.dump(students,f)
	f.close()
