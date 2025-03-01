# Casting Agency

Site live on Render site at : https://final-project-capstone-casting-agency.onrender.com

This  is the final project of the Udacity Full Stack Developer Nano Degree Program. It models a company that is responsible for creating movies and managing and assigning actors to those movies.The goal of this project is to deploy a Flask application hosted in Render Cloud/PostgreSQL and enable Role Based Authentication and roles-based access control (RBAC) with Auth0 (a third-party authentication system). There are three roles within the company of Assistant, Director and Producer.

## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

To do so, run the following commands

```bash
python -m virtualenv env
source env/bin/activate
```

#### Installing the dependencies

Once you have your virtual environment setup and running, install dependencies from the root directory by running

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup
With Postgres running, create a casting database:

```bash
createdb casting_agency
```
Populate the database using the data.psql file provided. From the backend folder in terminal run:

```bash
psql casting_agency< data.psql
```

## Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   - `delete:movies`
6. Create new roles for:
   - Casting Assistant (Can view actors and movies)
     - can `get:actors`
     - can `get:movies`

   - Casting Director (All permissions a Casting Assistant has and Add or delete an actor from database and Modify actors or movies)
      - `get:actors`
      - `get:movies`
      - `post:actors`
      - `patch:actors`
      - `patch:movies`
      - `delete:actors`

   - Executive Producer (All permissions a Casting Director has and Add or delete a movie from the database)
      - `get:actors`
      - `get:movies`
      - `post:actors`
      - `post:movies`
      - `patch:actors`
      - `patch:movies`
      - `delete:actors`
      - `delete:movies`

## Setting up the environment variables
setup.sh has all the environment variables needed for the project. The app may fail if they are not set properly.

The file should have the following values - 
DATABASE_URL
AUTH0_DOMAIN
API_AUDIENCE
ASSISTANT_TOKEN
DIRECTOR_TOKEN
PRODUCER_TOKEN
#### The rests also use the Auth token set in env variables and will give an error if the tokens are expired.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
export FLASK_ENV=development # enables debug mode
python3 api.py
```

## Verify on the Browser
Navigate to project homepage http://127.0.0.1:5000/ or http://localhost:5000


## Testing

To run the tests, run

```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test<data.psql
python3 test.py
```


### API Documentation

In order to use the API users need to be authenticated. Jwt tokens can be generated by logging in with the provided credentials on the hosted site.

#### Endpoints

GET /movies
- General:
   - Returns all the movies.
   - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: 
curl -X GET "http://127.0.0.1:5000/movies" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $TOKEN"

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Fri, 22 Jul 2011 00:00:00 GMT",
      "title": "Captain America: The First Avenger"
    },
    {
      "id": 2,
      "release_date": "Fri, 06 May 2011 00:00:00 GMT",
      "title": "Thor"
    },
    {
      "id": 3,
      "release_date": "Fri, 07 Jul 2017 00:00:00 GMT",
      "title": "Spider-Man: Homecoming"
    },
    {
      "id": 4,
      "release_date": "Fri, 16 Feb 2018 00:00:00 GMT",
      "title": "Black Panther"
    },
    {
      "id": 5,
      "release_date": "Sun, 12 Jan 2025 00:00:00 GMT",
      "title": "Avengers: Endgame"
    },
  ],
  "success": true
}
```

GET /movies/<int:id>
- General:
   - Returns a specific movie for which the ID is passed.
   - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: 
curl -X GET "http://127.0.0.1:5000/movies/1" \
-H "Content-Type: application/json" \ 
-H "Authorization: Bearer $TOKEN"

```json
{
  "movie": {
    "id": 1,
    "release_date": "Fri, 22 Jul 2011 00:00:00 GMT",
    "title": "Captain America: The First Avenger"
  },
  "success": true
}
```

POST /movies
- General:
   - Creates a new movie based on the inputs given.
   - Roles authorized : Executive Producer.

- Sample: 
curl -X POST http://127.0.0.1:5000/movies \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $TOKEN" \
 -d '{"title": "Titanic", "release_date": "1999-01-01"}'

```json
{
  "movie": {
    "id": 52,
    "release_date": "Fri, 01 Jan 1999 00:00:00 GMT",
    "title": "Titanic"
  },
  "success": true
}
```

PATCH /movies/<int:id>
- General:

   - Updates a movie based on a payload.
   - Roles authorized : Casting Director, Executive Producer.

- Sample: 
curl http://127.0.0.1:5000/movies/52 \
-X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d '{"title": "Titanic remake"}' 

```json
{
  "movie": {
    "id": 52,
    "release_date": "Fri, 01 Jan 1999 00:00:00 GMT",
    "title": "Titanic remake"
  },
  "success": true
}
```

DELETE /movies/<int:id>
- General:

  - Deletes a movies by id
  - Roles authorized : Executive Producer.

- Sample: 
curl http://127.0.0.1:5000/movies/52 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \                             
-X DELETE


```json
{
  "delete": "52",
  "success": true
}
```


GET /actors
- General:
   - Returns all the actors.
   - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: 
curl -X GET "http://127.0.0.1:5000/actors" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $TOKEN"

```json
{
  "actors": [
    {
      "age": 36,
      "gender": "Female",
      "id": 1,
      "name": "Scarlett Johansson"
    },
    {
      "age": 53,
      "gender": "Male",
      "id": 2,
      "name": "Mark Ruffalo"
    },
    {
      "age": 42,
      "gender": "Male",
      "id": 3,
      "name": "Chris Evans"
    },
    {
      "age": 43,
      "gender": "Female",
      "id": 4,
      "name": "Natalie Portman"
    },
    {
      "age": 47,
      "gender": "Male",
      "id": 5,
      "name": "Benedict Cumberbatch"
    },
  ],
  "success": true
}
```

GET /actors/<int:id>
- General:
   - Returns a specific actor for which the ID is passed.
   - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: 
curl -X GET "http://127.0.0.1:5000/actors/1" \
-H "Content-Type: application/json" \ 
-H "Authorization: Bearer $TOKEN"

```json
{
  "actors":{
      "age": 36,
      "gender": "Female",
      "id": 1,
      "name": "Scarlett Johansson"
    },
  "success": true
}
```

POST /actors
- General:
   - Creates a new actor based on the inputs given.
   - Roles authorized : Casting Director, Executive Producer.

- Sample: 
curl -X POST http://127.0.0.1:5000/actors \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $TOKEN" \
 -d '{"name": "Shahrukh Khan", "age": "61","gender":"male" }'

```json
{
  "actor": {
    "age": 61,
    "gender": "male",
    "id": 27,
    "name": "Shahrukh Khan"
  },
  "success": true
}
```

PATCH /actors/<int:id>
- General:

   - Updates an actor based on a payload.
   - Roles authorized : Casting Director, Executive Producer.

- Sample: 
curl http://127.0.0.1:5000/actors/27 \
 -X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d '{"name": "Shaaharukh", "age": 62}'' 

```json
{
  "actor": {
    "age": 62,
    "gender": "male",
    "id": 27,
    "name": "Shaaharukh"
  },
  "success": true
}
```

DELETE /actors/<int:id>
- General:

  - Deletes an actor by id
  - Roles authorized : Casting Director, Executive Producer.

- Sample: 
curl http://127.0.0.1:5000/actors/27 \ 
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
 -X DELETE


```json
{
  "delete": "27",
  "success": true
}
```

### Error Codes

Errors are returned as JSON objects in the following format:

1) Resource not found

```json
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```

2) Bad request

```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

3) Unprocessble Request

```json
{
    "success": False, 
    "error": 422,
    "message": "unprocessable"
}
```

4) Internal Server Error

```json
{
    "success": False, 
    "error": 500,
    "message": "internal server error"
}
```

5) RBAC errors 
```json
{
    "success": False, 
    "error": 401,
    "message": "authorization_header_missing"
}
```

6) Permission errors
```json
{
    "success": False, 
    "error": 403,
    "message": "Permission not found."
}
```