# SAKURA Fault Graph Explorer
This repository contains a self-modeling approach and a diagnosis process for the Docker Clearwater vIMS:  [clearwater vIMS docker](https://github.com/cherrared/clearwater-docker.git)

## What's inside
* A knowledge base describing the Clearwater vIMS dependencies 
* A self-modeling algorithm: diagnosis.py
* A diagnosis Algorithm: modelingalgo.py
* Input of false and true observations: Obs.yml
* Input of the network topology : input-topo-ex1.yml and input-topo-ex2.yml
* The diagnosis process solutions:  Solutions.txt

## Prerequisites 

```
$ sudo apt-get install python3-tk 
```

```
sudo apt-get -y install python3-pip
```

```
$ pip3 install --user -r requirements2
```


* Clone the project: 
```
 git clone git@github.com:cherrared/SAKURA-Model-based-RCA.git
```


## Self-modeling algo:

```
$ python3 modelingalgo.py input-topo-ex1.yml

```
## Diagnosis process:
```
$ python3 diagnosis.py input-topo-ex1.yml obs.yml

```

## Example1:
![vIMS Architecture]( https://github.com/cherrared/SAKURA-Model-based-RCA/blob/master/architecture.png)

* The input-topo-ex1.yml describes this architecture of three sites or physical servers
* To model this architecture:


```
$ python3 modelingalgo.py input-topo-ex1.yml

```



### Fault Scenario Docker Bono Down:
![Bono down](https://github.com/cherrared/SAKURA-Model-based-RCA/blob/master/scenario.png )
* Input initial observations of this fault: obs.yml
* Run the diagnosis algo to explain the observations:
```
$ python3 diagnosis.py input-topo-ex1.yml obs.yml

```
* Each time provide the diagnosis process with the values of observations with testing the clearwater vIMS deployement: True, False or None
* Final result: 
![Result](https://github.com/cherrared/SAKURA-Model-based-RCA/blob/master/Figure_Dsss.png)



*** This is only an example of a vIMS fault. The topo.yml file and obs.yml file could be changed for any possible vIMS architecture and faults' observations
