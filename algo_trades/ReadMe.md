1.	python 3.10 or latest
2.	install from packages from requirements.txt 
3.	Setup Angel-one smart-API Setup
4.	create a directory /opt/tmp/angel_1/   for logs and temp-files
5.	run python starter.py


====================================================

Cron settings
1. create directories  
	/opt/algo_step/angel_smart_api/
	/opt/tmp/angel_1/
	
2. add below cronjob	

15 9 * * 1-5 /usr/bin/python3 /opt/algo_step/angel_smart_api/starter.py >> /opt/tmp/angel_1/cron_job.log 2>&1


====================================================

