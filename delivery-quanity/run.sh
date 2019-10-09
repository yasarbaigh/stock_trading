#/usr/bin/sh
cd /home/yasar/my-git/stock_trading/delivery-quanity

echo "\n\n\n\n" > dq.log
echo "-------------------------------" >> dq.log

now=$(date +"%T")

echo "Current time : $now" >> dq.log

mvn compile
mvn exec:java >> dq.log

