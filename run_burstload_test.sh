#!/bin/bash

# we are testing for... 10 mins switching between 10 and 100 users every 1 minute

for ((i=0; i<5; i++))
do
    echo "Iteration $((i+1)): Starting auth test with 10 users"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_authentication.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 10 -JrampUp 0 -JdurationMs 60000 -l results/burstload_auth_10users_itr"$i".csv -n


    echo "Iteration $((i+1)): Starting auth test with 100 users"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_authentication.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 100 -JrampUp 0 -JdurationMs 60000 -l results/burstload_auth_100users_itr"$i".csv -n
done


for ((i=0; i<5; i++))
do
    echo "Iteration $((i+1)): Starting web heavy test with 10 users"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_heavy.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 10 -JrampUp 0 -JdurationMs 60000 -l results/burstload_webhvy_10users_itr"$i".csv -n


    echo "Iteration $((i+1)): Starting web heavy test with 100 users"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_heavy.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 100 -JrampUp 0 -JdurationMs 60000 -l results/burstload_webhvy_100users_itr"$i".csv -n
done


for ((i=0; i<5; i++))
do
    echo "Iteration $((i+1)): Starting web light test with 10 users"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_light.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 10 -JrampUp 0 -JdurationMs 60000 -l results/burstload_weblgt_10users_itr"$i".csv -n


    echo "Iteration $((i+1)): Starting web light test with 100 users"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_light.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 100 -JrampUp 0 -JdurationMs 60000 -l results/burstload_weblgt_100users_itr"$i".csv -n
done

