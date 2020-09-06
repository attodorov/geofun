# Instructions
- run the following command - assumes Python3:
python server.py
- then open http://localhost:8100

- in order to get nearest cities, please use the following endpoint:

http://localhost:8100/api/neareststores/<uk postcode>/<distance in km>

example:

http://localhost:8100/api/neareststores/BN149GB/50

- searching cities and postcodes usage:

http://localhost:8100/api/searchstores?query=br

#assumptions

 - distance is measured in km (not miles)
 - distance is based on "bird's eye" - i.e. the direct line between two points, not car/road/rail distance

 #Running the unit tests: 

 python3 -m unittest tests/tests.py

#NOTES
- if we have to filter/search a really large list I would put it in a database or elasticsearch index instead of filtering in memory.

#TODO
- Currently the custom router i have implemented assumes api will have the pattern /api/<endpoint name>/<extra params> and while it is fully HTTP 1.1 RFC (REST) compliant, it may be improved to support more flexible naming such as /api/stores/search or /api/stores/nearest
- For nearest searching, I have it implemented like this: /api/neareststores/<postcode>/<distance> but it may be more appropriate to use a pattern such as /api/neareststores/<postcode>?distance=<distance>