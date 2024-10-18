Add below snippet in file  FivePaisaClient

self.session = requests.Session()
self.session.verify = False

====================



#* * * * 1-5 date >> /home/trys/opt/tmp/c.log

* * * * 1-5 /usr/bin/python3 /home/trys/kch/ts.py >>/home/trys/opt/tmp/cp.log 2>&1

15 9 * * 1-5 /usr/bin/python3 /home/trys/kch/ranga_starter.py >> /home/trys/opt/tmp/angel.log 2>&1

=================================

mkdir -p /home/trys/opt/tmp/

sudo apt install python3-pip

python3 -m pip install smartapi-python pandas pytop logzero websocket --break-system-packages


nohup python3 /home/trys/kch/ranga_starter.py >> /home/trys/opt/tmp/angel.log 2>&1 &

 ==============================

kill -9 $(ps -ef | grep angel_flask_starter.py | awk '{print $2}') ;


python3 angel_flask_starter.py > op.log 2>&1 &





kill -9 $(ps -ef | grep angel_flask_starter.py | awk '{print $2}') ;
kill -9 $(ps -ef | grep 'frontend/node_modules/.bin/vue-cli-service' | awk '{print $2}') ;