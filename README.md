EECS-498-IR-Project
===================

Steps:
----------
1. `python getLinksFromDB.py`
2. Copy the list of article names from the `articles` file to 
  Wikipedia: Special Export
3. Download the XML file that will contain the list of articles you input to 
  Wikipedia: Special Export
4. `python run.py <Wikipedia XML file>`
5. `python hierarchy_tree.py`
6. Entropy calculation is done with:
     `python entropy.py`


##### Notes:
If you want to change the starting page for crawl, modify `line 119` in
`getLinksFromDB.py` to be `start_page = <Wikipedia article name>`

To change how many articles deep to crawl, modify `line 123` in
`getLinksFromDB.py`

To change k for k-means, change `line 90` in `run.py`

Our `getLinksFromDB.py` sends request to an external server which
will not exist 1 week after the last day of exams


WWII Dataset Steps:
-------------------

1. `python run.py WWII.xml`
2. `python hierarchy_tree.py`
3. Entropy calculation is done with:
     `python entropy.py`


Visualization:
--------------
The Javascript code for visualization was created on JSFiddle Code:
  * Tree View:
    * http://jsfiddle.net/yyli/X5H9F/26/
  * Cluster View:
    * http://jsfiddle.net/yyli/nKzKw/11/

It is not extremely simple to copy the json object into this interface,
therefore we are not providing a way to view it. Currently the sites
show Run 1 on the World War II dataset.

The generation for JSON objects is in `gen_json.py`

To change which clusters hierarchy is generated, modify `line 172` in
  `hierarchy_tree.py` to `i == <cluster number>`


