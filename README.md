# tempo_test

## Introduction
The project is setup with docker, where the web api and database are seperate containers. I thought it would be the easiest way for anybody to run the solution, see the 'How To Run' sub section.

I decided to use flask for a web framework because i'm familiar with python, it's easy to setup and the structure of the project files is entirely up to the developer.

For a datastore I use Redis which is a NoSQL database. Because the entities and their relationships are not very complicated I decided to use a NoSQL database instead of relational database.

### Prerequisites
* Docker
* Docker Compose

### How To Run
`docker-compose up`

## Solution
### Database
Entities:
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
At startup the role table is initialized with the minimal data that was mentioned in the project description but the membership table is empty.

### Endpoints
1. Get all roles: `GET http://localhost:5000/api/role`

2. Get role with id 1: `GET http://localhost:5000/api/role/1`

3. Get all memberships: `GET http://localhost:5000/api/membership`

4. Get membership with team_id 1 and user_id 2: `GET http://localhost:5000/api/membership/1/2`

5. Set role for membership with team_id 1 and user_id 2: `PUT http://localhost:5000/api/membership/1/2`
With a json body: `{ "role_id": 2 }`

### Flow
Role is just a regular resource with only GET endpoints were endpoint 1 gets all roles and endpoint 2 gets the role with the id in the request and its memberships.

The Membership resource is not as simple. Though the api stores a table called memberships its purpose is not to keep track of the connection between a team and a user but only to store the memberships role. The tempo-test api keeps track of the connections.
To get a role for a membership (requesting endpoint 4) the membership table is searched, if it does not exist there, the membership is returned with the default role_id.
If endpoint 5 is requested with a role_id that is not the default the membership and role is inserted into the membership table.

### Complications
#### Rest URL
Rest url is easy when working with a resource that has one primary key and a hierarchical relationship with other resources. But that is not the case in this excercise where membership has a composite primary key of team and user because team and user have a many-to-many relationship. The two solutions that made most sense to me were:
1. `/api/membership/{team_id}/{user_id}`
2. `/api/team/{team_id}/user/{user_id}`
I used number 1. because I think it states clearly what resource will be fetched but with number 2 the resource could be a membership or a user.

#### Membership data
The only way to get the membership data (that is (team_id, user_id)) is to make n+1 requests to every team or every user resource where n is the number of teams or users. Because we want to minimize the number of requests, using the team resource would make most sense. The number of users will probably always be bigger than the number of teams.

Making multiple requests can be slow. The average time of making a single team request to the tempo-test api is 350ms. There are 5 teams so we need 6 requests to get the membership data which is 6\*350ms or 2.1 seconds. If we expect to have more teams then this solution is not ideal. I thought of a few ways to speed things up:
1. Threading - The requests are not parallel, if n threads were used we could make n parallel requests, which means 350ms instead of 2.1s.
2. Better server (hardware and/or containers) - I assume the heroku server being used does not have optimal hardware for production usage. Using multiple servers and multiple containers with a load balancer would speed things up as well.
3. Store all membership data - Making these requests at startup, storing the data and syncing at an interval would prevent that requests sent to this api would have to request tempo-test api multiple times.

#### Cleanup
This is not a major issue but if a membership is stored in our database and the user that has this membership quits the team, the data is not removed from out database.
A cleanup act could solve this issue.
