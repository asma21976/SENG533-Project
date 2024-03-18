#!/bin/bash

trap 'sigint_handler' SIGINT
sigint_handler() {
    echo "Ctrl+C detected. Terminating both processes..."
    # Terminate python_script1 and python_script2
    kill -SIGINT "$pid_monitor" "$pid_jmeter"
    exit 1
}

trap 'jmeter_exit_handler' EXIT
jmeter_exit_handler() {
    echo "JMeter process has finished. Sending SIGINT to the monitor process..."
    kill -INT "$pid_monitor"
}


trial="$1"

# Check if the trial flag value is provided
if [ -z "$trial" ]; then
    echo "Trial Flag not provided."
else
    echo "Trial Flag provided: $trial"
    rm -f results/constload/trial"${trial}"*

    # we are testing 3 different groups of users for 10 mins each
    user_list=(10) # 50 100)
    for user in "${user_list[@]}"
    do
	echo "Starting auth test for ${user} users"
	echo "java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_authentication.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser${user} -JrampUp 0 -JdurationMs 600 -l results/constload/trial${trial}_auth_${user}users.csv -n"
	sleep 5

	java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_authentication.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser"${user}" -JrampUp 0 -JdurationMs 10 -l results/constload/trial"${trial}"_auth_"${user}"users.csv -n &
	pid_jmeter=$!

	python3 Monitoring\ scripts/OSMonitor/osmonitor.py --out-dir results/constload/ --test-name trial"${trial}"_auth_"${user}"users &
	pid_monitor=$!
	wait "$pid_jmeter"
	echo "OSMonitor PID: $pid_monitor"
	
	echo "Terminating OSMonitor..."
	kill -TERM "$pid_monitor"

	echo "Starting web heavy test for ${user} users"
	echo "java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_heavy.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser${user} -JrampUp 0 -JdurationMs 600 -l results/constload/trial${trial}_webhvy_${user}users.csv -n"
	sleep 5

	java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_heavy.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser"${user}" -JrampUp 0 -JdurationMs 10 -l results/constload/trial"${trial}"_webhvy_"${user}"users.csv -n &
	pid_jmeter=$!

	python3 Monitoring\ scripts/OSMonitor/osmonitor.py --out-dir results/constload/ --test-name trial"${trial}"_webhvy_"${user}"users &
	pid_monitor=$!
	wait "$pid_jmeter"
	echo "OSMonitor PID: $pid_monitor"

	echo "Terminating OSMonitor..."
	kill -TERM "$pid_monitor"
	
	echo "Starting web light test for ${user} users"
	echo "java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_light.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser${user} -JrampUp 0 -JdurationMs 600 -l results/constload/trial${trial}_weblgt_${user}users.csv -n"
	sleep 5

	java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t goal-1/teastore_browse_nogui_webui_light.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser"${user}" -JrampUp 0 -JdurationMs 10 -l results/constload/trial"${trial}"_weblgt_"${user}"users.csv -n &
	pid_jmeter=$!

	python3 Monitoring\ scripts/OSMonitor/osmonitor.py --out-dir results/constload/ --test-name trial"${trial}"_weblgt_"${user}"users &
	pid_monitor=$!
	echo "OSMonitor PID: $pid_monitor"
	wait "$pid_jmeter"

	echo "Terminating OSMonitor..."
	kill -TERM "$pid_monitor"
    done
fi


