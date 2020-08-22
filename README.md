Table of contents
=================
<a name="table-of-contents"></a>

* [Task overview](#task-overview)
* [Proposed solution](#proposed-solution)
    * [Chosen approach](#chosen-approach)
    * [Flow and examples](#flow-and-examples)
* [Further improvements and possible approaches](#further-improvements-and-possible-approaches)
* [Conclusion](#conclusion)


Task overview 
=============
<a name="task_overview"></a>

The task was divided into two subtasks. The main one was to create a wrapper around Nominatim Search API.
Requirements were as follows:

- [x] Application should be using Python 3.7+.
- [x] Application should be REST-compatible.
- [x] Application should have one GET endpoint. *Disclaimer*: In the task given endpoint was 
```GET /geolocate?address=<string>```. Because of the way that chosen framework treats ```?``` character I had to change
 the endpoint to ```GET /geolocate/address=<string>```. Hope that is not a problem, but if it is I please let me know 
 and I will create the API based on different framework.
- [x] Endpoint should return address data for the input query.
- [x] Returned data should be in JSON format.
- [x] Endpoint should return only one result.
- [x] Endpoint should raise 404 error code, if API cannot locate the address.
- [x] Automatic tests are not needed as the application relies heavily on the external API.

The second (bonus) task was to add Redis solution to the application to cache API requests. Requirements were as 
follows:

- [x] Implement Redis solution.
- [x] The key should we set to the input query and the value should be set to API call result.
- [x] Set the life span for the Redis entry e.g. 7 days.
- [x] Upon inputting the query application should check if key already exist in the Redis database, and if so return it 
from Redis without making expensive API call.

Proposed solution
=================
<a name="proposed-solution"></a>

Below I present details about proposed solution. 

Chosen approach
---------------
<a name="chosen-approach"></a>

Here is a brief overview of the technologies used in my solution:

- Application is based on Python 3.8.1.[]()
- For easier setup: [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
- For Redis monitoring: [RedisInsight](https://redislabs.com/redis-enterprise/redis-insight/).
- For creating the API i used [FastAPI](https://fastapi.tiangolo.com/). It is quite new web framework (about 1.5 years 
old) This framework requires Python version 3.6+. There are many features that speaks for using that framework:
    - Fast - on par with NodeJS and Go.
    - Robust.
    - Standards-based - on [OpenAPI](https://github.com/OAI/OpenAPI-Specification) and 
    [JSON Schema](http://json-schema.org/).
    - Intuitive.
    - And many more.
- For requests the most popular library is [Requests](https://requests.readthedocs.io/en/master/). I chose the 
[httpx](https://github.com/encode/httpx) library. It is almost a drop-in replacement for Requests library, but it is a 
lot more efficient and has async support.

The flow of the application can be briefly summarised in the graph:

![Application flow graph](images/flow.png?style=centerme)


Flow and examples
-----------------
<a name="flow-and-examples"></a>

As for the flow, to use the application following steps should be taken:
- Install docker and docker-compose on the machine. The instruction can be found on the docker site.
- Clone the repository and change directories.
```
git clone https://github.com/phryniewicz/nominatim_api.git
cd nominatim_api
```
- Build the docker image and start the server in the background.
```
docker-compose up -d
```
- When servers start go to ```http://localhost:8001/``` and create the Redis database with provided parameters.
![RedisInsight](images/redis_insight.png?style=centerme)
![RedisDatabase](images/redis_configuration.png?style=centerme)
The dummy password is ```ubuntu```.
- FastAPI provides the automatic documentation for the API. Go to ```http://localhost:5000/docs``` and test the API.
Since no automatic tests were needed, I performed few manual tests e.g. full address, partial address, just city, state,
 country, continent.
- After testing you can go back to ```http://localhost:8001/``` and in ```Browser``` window you can check more about our
 Redis instance.
 
Further improvements and possible approaches
============================================
<a name="futher-improvements-and-possible-approaches"></a>

Further improvements may consist of:

- [ ] At this moment we are using just a part of the Nominatim API capabilities, at the moment API is using their query 
system.
- [ ] At the moment we are returning address data, but we may want to return more details e.g. longitude and latitude of
 the query target.
- [ ] Add automatic tests.
- [ ] And many more.

Conclusion
==========
<a name="conclusion"></a>

That concludes the presentation of the solution. I hope you find it sufficient.
