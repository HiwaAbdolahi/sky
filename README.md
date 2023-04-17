Simpleperf
Simpleperf is a Python script for measuring network performance between hosts in a network. It uses the iperf tool for measuring bandwidth and latency, and can be used to evaluate the performance of different network topologies, protocols, and configurations.

Requirements
Python 3.x
iperf (both client and server)
Mininet (for creating virtual network topologies)
Usage
Create a Mininet network topology using the portfolio-topology.py script.
Start iperf servers on the desired hosts using the iperf-server.sh script.
Run Simpleperf with the desired parameters, such as duration, protocol, and number of parallel connections.
Example usage: python3 simpleperf.py -s 10.0.1.2 :> run the server 
python3 simpleperf.py -c -I 10.0.1.2 -p 8080 -t 25 -P 2 :> make parallel connection on 10.0.1.2



Output
Simpleperf will output the measured bandwidth and latency in MB/s and ms, respectively. The results are saved to a file in the measurements directory, with a filename indicating the hosts and parameters used.