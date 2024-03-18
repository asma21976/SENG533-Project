#!/bin/bash

# we are testing 3 different groups of users for 10 mins each


trial="$1"

# Check if the trial flag value is provided
if [ -z "$trial" ]; then
    echo "Trial Flag not provided."
else
    echo "Trial Flag provided: $trial"
    rm -f results/constload/trial"${trial}"*

    user_list=(10 50 100)
    for user in "${user_list[@]}"
    do
	echo "Starting auth test for ${user} users"
	java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_authentication.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser"${user}" -JrampUp 0 -JdurationMs 600000 -l results/constload/trial"${trial}"_auth_"${user}"users.csv -n

	echo "Starting web heavy test for ${user} users"
	java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_heavy.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser"${user}" -JrampUp 0 -JdurationMs 600000 -l results/constload/trial"${trial}"_webhvy_"${user}"users.csv -n

	echo "Starting web light test for ${user} users"
	java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_light.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser"${user}" -JrampUp 0 -JdurationMs 600000 -l results/constload/trial"${trial}"_weblgt_"${user}"users.csv -n
    done
fi

