#!/bin/bash

instances="$1"
trial="$2"

if [ -z "$trial" ]; then
    echo "Trial flag not provided."
    exit 1
else
    echo "Trial flag provided: $trial"
    rm -f results/horizontal/trial"${trial}"_inst"${instances}"_*
fi

if [ -z "$instances" ]; then
    echo "instance flag not provided."
else
    echo "Instance flag provided: $instances"

    echo "Starting auth test with 100 users with $instances instances"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_authentication.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 100 -JrampUp 0 -l results/horizontal/trial"${trial}"_inst"$instances"_auth_100users.csv -n

    echo "Starting web heavy test with 100 users with $instances instances"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_heavy.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 100 -JrampUp 0 -l results/horizontal/trial"{$trial}"_inst"$instances"_webhvy_100users.csv -n

    echo "Starting web light test with 100 users with $instances instances"
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_light.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 100 -JrampUp 0 -l results/horizontal/trial"{$trial}"_inst"$instances"_weblgt_100users.csv -n

fi

