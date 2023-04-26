# apple_test

Implement a Uses Rate Limiter for APIs

What is a Rate Limiter?
Rate limiting is used to control the amount of incoming and outgoing traffic to or from a network. For example, let's say you are using a particular service's API that is configured to allow 100 requests/minute. If the number of requests you make exceeds that limit, then an error will be triggered. The reasoning behind implementing rate limits is to allow for a better flow of data and to increase security by mitigating attacks such as DDoS. 


Features:
1.Transaction per second limits based on license (user specific).
2.Throttling capabilities.
Ex: Let’s say TPS agreement is 100, and in first 10 milliseconds 90 requests came then rate limiter will make sure that only 10 request passes through in 1 sec boundary.

Tech Stack:
Python, DB (Any or H2 will do.).

Note: Commit code in public Github with instructions to run the code and share the link. 

##

docker-compose up --build 