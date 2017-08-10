# URL Shortener

## Description
The concept is to take a url and produce a short version using a Base62 representation of the url.

The shortened snippet has a bidirectional mapping to the primary key in the Snippet table.

When we request one of the short urls, we parse your request's User-Agent to figure out your
device type. If a specialized redirect url (mobile, tablet) is specified we use that, otherwise
we use the default redirect url (desktop_redirect). We also increment the counter for the
used redirect type.

We use:
* [marshmallow-jsonapi](https://github.com/marshmallow-code/marshmallow-jsonapi) to create a JSON-api and schema validation.
* [Blueprints](http://flask.pocoo.org/docs/0.11/blueprints/) and [Flask-restful](https://github.com/flask-restful/flask-restful) to create modular REST apis.
* [PostgreSQL](https://www.postgresql.org/) as our datastore.
* [Alembic](http://alembic.zzzcomputing.com/en/latest/) for migrations.


## Database
Dependency on PostgreSQL.

## Bootstrap
```
cd shortener
virtualenv env
source env/bin/activate
pip install fabric

# Bootstrap your environment
fab bootstrap

# Bootstrap your database
fab bootstrap_database
fab bootstrap_database:env=test
```

## Testing
```
source env/bin/activate
fab test
```

## Running a server locally
```
source env/bin/activate
fab serve
```

## Production server
TBD

## Tables
Snippet
* id: Integer PK -  Encoded to a short url
* desktop_redirect: String, Required - The redirect url for desktop
* mobile_redirect: String - The redirect url for mobile
* tablet_redirect: String - The redirect url for tablet
* desktop_redirect_count: Integer, default = 0 - Counter for redirects to desktop
* mobile_redirect_count: Integer, default = 0, Counter for redirects to mobile
* tablet_redirect_count: Integer, default = 0, Counter for redirects to tablet
* short_url: String - The short url

The Snippet table contains a url snippet containing redirects for mobile, tablet, and desktop, as well
as keeping counters for each time each redirect is used.


## Endpoints
### Create a new snippet:
* desktop_redirect --> redirect for desktop as well as default
* mobile_redirect --> redirect for mobile
* tablet_redirect --> redirect for tablet

Request:
```
curl -H "Content-Type: application/json" -X POST -d '{"data":{"attributes":{"desktop_redirect":"https://facebook.com/", "mobile_redirect":"https://wikipedia.com", "tablet_redirect": "https://google.com"},"type": "snippets"}}' http://localhost:5000/snippets/
```

Response:
```
{
    "data": {
        "attributes": {
            "desktop_redirect": "https://facebook.com/",
            "desktop_redirect_count": 0,
            "mobile_redirect": "https://wikipedia.com",
            "mobile_redirect_count": 0,
            "short_url": "http://localhost:5000/1",
            "tablet_redirect": "https://google.com",
            "tablet_redirect_count": 0,
            "time_since_creation": "-1 day, 19:00:00.010453"
        },
        "id": "1",
        "type": "snippets"
    }
}
```

### Get data for all snippets
Request:
```
curl http://localhost:5000/snippets/
```

Response:
```
{
    "data": [
        {
            "attributes": {
                "desktop_redirect": "https://facebook.com/",
                "desktop_redirect_count": 0,
                "mobile_redirect": "https://wikipedia.com",
                "mobile_redirect_count": 0,
                "short_url": "http://localhost:5000/1",
                "tablet_redirect": "https://google.com",
                "tablet_redirect_count": 0,
                "time_since_creation": "-1 day, 19:01:11.517199"
            },
            "id": "1",
            "type": "snippets"
        },
        {
            "attributes": {
                "desktop_redirect": "https://facebook.com/",
                "desktop_redirect_count": 0,
                "mobile_redirect": "https://wikipedia.com",
                "mobile_redirect_count": 0,
                "short_url": "http://localhost:5000/2",
                "tablet_redirect": "https://google.com",
                "tablet_redirect_count": 0,
                "time_since_creation": "-1 day, 19:00:15.089031"
            },
            "id": "2",
            "type": "snippets"
        }
    ]
}
```

### Get data for a single snippet
Request:
```
curl http://localhost:5000/snippets/1
```

Response:
```
{
    "data": {
        "attributes": {
            "desktop_redirect": "https://facebook.com/",
            "desktop_redirect_count": 0,
            "mobile_redirect": "https://wikipedia.com",
            "mobile_redirect_count": 0,
            "short_url": "http://localhost:5000/1",
            "tablet_redirect": "https://google.com",
            "tablet_redirect_count": 0,
            "time_since_creation": "-1 day, 19:02:13.839261"
        },
        "id": "1",
        "type": "snippets"
    }
}
```

### View a short url
* Visit the snippet. ex. `http://localhost:5000/1` (where the snippet is 1)
* curl the snippet endpoint setting a specified user-agent (for testing)
```
curl -H "User-Agent: ipad" http://localhost:5000/1
```
