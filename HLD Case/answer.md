1. we are going to use async event loop.
Because we have heavy db read write and getting data from user location i/o bound task, if a user location get stuck or any issues then my entire apps request will be blocked so async loop is the best fit here. 
to protect Golden Production Rule Violation we will use multi process for cpu bounded work like ride matching calculation, distance and for i/o bound task we can use direct db execution to make read write more fast

2. here we will use stateless architecture where when a user login we will create a token and return it to the user and we will use that token to track the user and it will happen in our system code like login view or login api endpoint and other endpoint will get the user from the token
when session is stateless then every node treat the session as first request and from the token we get the user id or the user info and we can confirm that user get this token via login, so in another instance user can login so we use that login token.
if a driver's account is flagged or reported for stateless architecture we will make the existing token expiry 0 and refresh token will be changed then the driver account will logout automatically at the next request.

3. we will use sql database like postgress for user profiles, trip billing history etc. but for every 4 sec data like cordinate string etc we can use caching here like cordinate's will write in the redis and user will see that from redis so read write will be more fast and like after 1 min or 5 min we will take the data from redis and write in the database
for finding nearest drilver or passenger we will check first our rider location from redis because we are writing data in the redis and then we calculate the best match using any heapq for the nearest driver if driver accept then take that ride else driver reject pop from the heapq.

4. to reduce the down time and single point of failure we have to use the eda architecture in our system like cordinates collect in one app, ride match in one app, after ride start track the ride in one app etc and we can use message broker like redis or kafka to control this eda and for per app we need to use multiple instance so that if one down other can alive and continue the server.

server A = cordinates collect in this app
server B = match ride in this app
server C = after ride start track ride

```


                                                            |-----------------------|
                                                            |    | -> A1 -> |       |
                        |-> nginx(local api gateway) -> redis -> | -> A2 -> |       |   
                        |                                |       |          | -> db1(slave)|
client -> nginx(aws) -> | -------------------------------|       | -> B1 -> |              |->db1(master) 
                        |                                |       | -> B2 -> |              |->db2(master)
                        |-> nginx(local api gateway) -> redis -> |          | -> db2(slave)|
                                                            |    | -> C1 -> |        |
                                                            |    | -> C2 -> |        |
                                                            |________________________|

```