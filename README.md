# Instructions
- run the following command - assumes Python3:
python server.py
- then open http://localhost:8100

- in order to get nearest cities, please use the following endpoint:

http://localhost:8100/api/neareststores/<uk postcode>/<distance in km>

example:

http://localhost:8100/api/neareststores/BN149GB/50/10

#assumptions

 - distance is in km (not miles)

 #Unit tests: 

 python3 -m unittest tests/tests.py 
