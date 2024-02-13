### SENG 533 TERM PROJECT

#### setup instructions

1. install docker
2. install docker-compose
3. deploy default teastore (without kieker) and enable monitoring with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_default.yaml up -d
    (may have to change microservice ports if err)
    ```
4. check all microservices are running with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_default.yaml ps
    ```
5. stop microservices with:
    ```
    docker-compose -f ./TeaStore/examples/docker/docker-compose_default.yaml down
    ```


#### test instructions
##### if using jmeter

1. download jmeter with:
    ```
    curl -o apache-jmeter-5.4.3.tgz https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.4.3.tgz
    ```
2. from SENG533-Project dir, run:
    ```
    ~/apache-jmeter-5.4.3/bin/jmeter.sh -n -t examples/jmeter/teastore_browse_nogui.jmx -Jhostname 10.1.1.1 -Jport 8080 -JnumUser 10 -Jrampup 1 -l test_provided_jmeter.log
    ```

##### if using LIMBO HTTP Load Generator

1. ahh may not use this because we need to run load generator on a separate (local) machine

