## SENG 533 TERM PROJECT

### Setup Instructions
1. Install docker
2. Install docker-compose
3. Deploy default teastore (without kieker) and enable monitoring with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_default.yaml up -d
    (may have to change microservice ports if err)
    ```
4. Check all microservices are running with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_default.yaml ps
    ```
5. Stop microservices with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_default.yaml down
    ```


### Testing Instructions
Our team is using jmeter to run both of our experiments.
1. Download jmeter with:
    ```
    curl -o apache-jmeter-5.4.3.tgz https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.4.3.tgz
    ```
2. To test a sample jmeter script, enter the SENG533-Project directory and run:
    ```
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t TeaStore/examples/jmeter/teastore_browse_nogui.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 10 -JrampUp 1 -l test_jmeter.csv -n
    ```
3. To run the jmeter scripts used in this experiment, first start the os monitoring script [provided on a feature branch](https://github.com/asma21976/SENG533-Project/tree/301c9a233094d88d0ba5dafc3ff6a852891b4c1f/Monitoring%20scripts/OSMonitor):
    ```
    python3 Monitoring\ scripts/OSMonitor/osmonitor.py --out-dir results/exp1 --test-name trial1_test
    ```

4. After starting the os monitoring script, use another terminal to run one of the provided bash scripts:
    ```
    ./run_exp1_burstload_test.sh
    ```

5. Once the bash script finishes, end the OS monitoring using the ctrl+c interrupt.

6. You may also test our result parsing script [provided on a feature branch](https://github.com/asma21976/SENG533-Project/tree/301c9a233094d88d0ba5dafc3ff6a852891b4c1f/Monitoring%20scripts/ResultsParser) or our statistical analysis script [also provided on a feature branch](https://github.com/asma21976/SENG533-Project/tree/301c9a233094d88d0ba5dafc3ff6a852891b4c1f/Monitoring%20scripts/StatisticalAnalysis).
