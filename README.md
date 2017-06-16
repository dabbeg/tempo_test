# tempo_test

## Introduction
The project is set up with docker, where the web api and database are seperate containers. I used docker because, in my opinion, it is one of the easiest way to quickly run a project with multiple dependancies.

I decided to use Flask for a web framework since I'm more familiar with Python. It is easy to set up and the structure of the project files is entirely up to the developer.

For a database I used Redis. Redis is a NoSQL database, which means its data doesn't have nearly as many restrictions as relational databases which can be good and bad. The decision to use a NoSQL database was based on the simplicity of the entities and their relationship but for more complex entities a relational database would be a better choice.

### Prerequisites To Run Solution
* Docker
* Docker Compose

### How To Run
`docker-compose up`

## Solution
### Database
At startup the role table is initialized with the minimal data that was mentioned in the project description but the membership table is empty.

Though the api stores a table called memberships its purpose is not to keep track of the connection between a team and a user but only to store the memberships role. The tempo-test api keeps track of the connections.

Tables:
```
Role: {
    id: int,
    name: string,
    default: bool
}

Membership: {
    team_id: int,
    user_id: int,
    role_id: int
}
```

### Endpoints
1. Get all roles: `GET http://localhost:5000/api/role` <br/>
Returns all the data from the role table.

2. Get role with id 1: `GET http://localhost:5000/api/role/1` <br/>
Returns a single role with a list of memberships (team_id and user_id)

3. Get all memberships: `GET http://localhost:5000/api/membership` <br/>
Returns a list of all memberships (team_id and user_id)

4. Get membership with team_id 1 and user_id 2: `GET http://localhost:5000/api/membership/1/2` <br/>
Returns a single membership entity.

5. Set role for membership with team_id 1 and user_id 2: `PUT http://localhost:5000/api/membership/1/2` <br/>
Json body: `{ "role_id": 2 }` <br/>
Returns the updated membership entity.

### Complications
#### Rest URL for membership
Rest url is easy when working with a resource that has one primary key and a hierarchical relationship with other resources. That is, however, not the case in this excercise since membership has a composite primary key of team and user because team and user have a many-to-many relationship. The two solutions that made most sense to me were the following:
1. `/api/membership/{team_id}/{user_id}`
2. `/api/team/{team_id}/user/{user_id}`

I used the former because it states clearly what resource will be fetched, but the resource could be either a membership or a user in the latter.

#### Membership data
The only way to get the membership data (that is (team_id, user_id)) was to make n+1 requests to every team or every user resource where n is the number of teams or users. We want to minimize the number of requests, using the team resource would make most sense since the number of teams will most likely always be lower than the number of users.

Making multiple requests can be slow. The average time of making a single team request to the tempo-test api is 350ms. There are 5 teams so we need 6 requests to get the membership data which is 6\*350ms or 2.1 seconds. If we expect to have more teams, then this solution is not ideal. I thought of a few ways to speed things up:
1. *Threading*: The requests are not parallel, if n threads were used we could make n parallel requests, which means 350ms instead of 2.1s.
2. *Better server (hardware and/or containers)*: Having a good hardware for the server is important to be able to serve many parallel requests. Using multiple servers and multiple containers with a load balancer would speed things up as well.
3. *Store all membership data*: Making these requests at startup, storing the data and syncing at an interval would prevent that requests sent to this api would have to request tempo-test api multiple times. It would also mean that we are duplicating our data which should be avoided when possible.

In this implementation using endpoint 2, with the default role, or endpoint 3, will fire 6 requests to the tempo-test api.

#### Cleanup
When a membership is stored in our database and the user that is associated with the membership quits the team, the data is not removed from our database.
A cleanup act would solve this issue.
