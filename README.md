# Instructions
- run the following command - assumes Python3:
python server.py
- then open http://localhost:8100
- (this will auto load index.html where there is a list of store location)
- there is also UI to search based on a query string in real time with the respective 100 ms delay and 2 chars min. There's also lazy load in the UI as you scroll (for that i have decreased the height of the results container because 3 items don't usually fit the whole screen)
- auto-complete/suggest and paging with a ui widget:
http://localhost:8100/auto_suggest.html
(this one has dependency on jQuery UI - it's just the widget/library script that's loaded in the head)
- the custom search (without any dependencies) in index.html sends the query string along with other params such as whether to do startsWith or contains
- the auto_suggest widget is completely client-side, it loads the list once on load.
- in order to get nearest cities, please use the following endpoint:

http://localhost:8100/api/neareststores/<uk postcode>/<distance in km>

example:

http://localhost:8100/api/neareststores/BN149GB/50

- searching cities and postcodes API usage:

http://localhost:8100/api/searchstores?query=br

#assumptions
 - lazy load is assumed to be client-side, i.e. items are on the client but will be lazily-loaded in the UI
 - lazy load can for sure be server-side as well. for that a skip/limit query params can be added
 - distance is measured in km (not miles)
 - distance is based on "bird's eye" - i.e. the direct line between two points, not car/road/rail distance

 #Running the unit tests: 

 python3 -m unittest tests/tests.py

#NOTES
- if we have to filter/search a really large list I would put it in a database or elasticsearch index instead of filtering in memory.

#TODO
- Currently the custom router i have implemented assumes api will have the pattern /api/<endpoint name>/<extra params> and while it is fully HTTP 1.1 RFC (REST) compliant, it may be improved to support more flexible naming such as /api/stores/search or /api/stores/nearest
- For nearest searching, I have it implemented like this: /api/neareststores/<postcode>/<distance> but it may be more appropriate to use a pattern such as /api/neareststores/<postcode>?distance=<distance>