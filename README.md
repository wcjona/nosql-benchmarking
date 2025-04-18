1. Install Virtualbox: https://www.virtualbox.org/wiki/Downloads
2. Install Ubuntu Server 24.04: https://ubuntu.com/download/server
3. Setup new VM on Virtualbox
4. For resources:
- Single core system: 8192 mb memory, 1 core
- Multi core system: 8192 mb memory, 4 core
k
Install python:
`sudo apt-get update`
`sudo apt-get install python3 python3-pip`

Install mongo:
`sudo apt-get install -y mongodb`
`pip3 install pymongo`


Install Cassandra:
`sudo apt-get install cassandra`
`pip3 install cassandra-driver`

Install Redis:
`sudo apt-get install redis-server`
`pip3 install redis`

Verify Services running:
`sudo systemctl start mongod`
`sudo systemctl status mongod`

`sudo systemctl status cassandra`
`sudo systemctl start cassandra`

`sudo systemctl start redis-server`
`sudo systemctl status redis-server`
