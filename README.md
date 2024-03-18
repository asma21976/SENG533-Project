### SENG 533 TERM PROJECT

#### setup instructions
For most reliable performance, deploy microservices on RAC

1. install docker
2. install docker-compose
3. deploy default teastore (without kieker) and enable monitoring with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_new.yaml up -d
    (may have to change microservice ports if err)
    ```
4. check all microservices are running with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_new.yaml ps
    ```
5. stop microservices with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_new.yaml down
    ```

#### setup for multi-instance
Note: WebUI, Auth, DB, and registry do not require scaling

 ```
  docker-compose -f ./TeaStore/examples/docker/docker-compose_new.yaml up -d --scale persistence={NUM_INST} --scale image={NUM_INST}--scale recommender={NUM_INST} 
```

#### test instructions
##### if using jmeter

1. download jmeter with:
    ```
    curl -o apache-jmeter-5.4.3.tgz https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.4.3.tgz
    ```
2. from SENG533-Project dir, run:
    ```
    java -jar ~/apache-jmeter-5.4.3/bin/ApacheJMeter.jar -t TeaStore/examples/jmeter/teastore_browse_nogui.jmx -Jhostname 127.0.0.1 -Jport 8080 -JnumUser 10 -JrampUp 1 -l test_jmeter.csv -n
    ```

##### if using LIMBO HTTP Load Generator

1. ahh may not use this because we need to run load generator on a separate (local) machine


##### if using Locust
1. install pip3 (and python>=3.6)
2. pip3 install locust
3. add locust to path
4. run test:
    ```
    locust -f TeaStore/examples/locust/locustfile.py --headless -u 100 -r 10
    ```
