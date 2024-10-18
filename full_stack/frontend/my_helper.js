nohup npm run serve > op.log 2>&1 &
nohup python3 angel_flask_starter.py > op.log 2>&1 &

==========

ps -ef | grep angel_flask_starter.py ; 
ps -ef | grep 'frontend/node_modules/.bin/vue-cli-service' ;




kill -9 $(ps -ef | grep angel_flask_starter.py | awk '{print $2}') ;
kill -9 $(ps -ef | grep 'frontend/node_modules/.bin/vue-cli-service' | awk '{print $2}') ;