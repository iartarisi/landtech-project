This is a solution to the [Sold Price Map challenge](https://github.com/landtechnologies/technical-challenge/blob/master/sold-price-map.md).

## Quickstart

Run `docker-compose up`. This will run the tests and start a flask server. You can then do `docker-compose exec web bash` in order to run further commands from inside the application container.

## Docs

Two JSON REST API endpoints are provided for retrieving all the places and for creating a new place respectively. The [GeoJSON](https://geojson.org/) specification is used for representing places.

```
GET /places/

{
    'places': {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [10, 10]
                },
                'properties': {
                    'price': 1422640,
                    'percentile': 25
                }
            },
            ...
        ]
    }
}
```

```
POST /places/

{
    'type': 'Feature',
    'geometry': {
        'type': 'Point',
        'coordinates': [10, 10]
    },
    'properties': {
        'price': 1422640,
        'percentile': 25
    }
}
```

## Considerations/TODO

The GeoJSON has the advantages of being a __standard__ way of representing points and other location-data (presumably what other LandTech features will build upon). It is easily extensible so allows for augmenting the existing data.

Another binary format could be devised if network performance/transited data was a concern. In the exercise example, there are 10000 possible data points so it should be easy to devise a format which would remove the need for specifying each point's location (e.g. specifying the relative location of the next point or specifying all prices and having a blank code for missing prices).

Endpoints relating to a place are missing: retrieving a single place (`GET`), updating a place (`PUT`), deleting a place (`DELETE`).

Pagination could be implemented depending if the number of points retrieved on a single request would continue to grow.

There is no database right now. The points should be stored in a database. The choice of database will probably depend on how the application evolves and what other data structures will be supported.

Using PostgreSQL would allow the price percentile calculations to be done on each retrieval of a single place (`percentile_disc` and `percentile_cont` functions). That would allow the database of places to grow without burdening the application's memory.

Using a separate database would also alleviate the concurrency problems from having to open a file for reading/writing.

There are more tests that can be written: invalid GeoJSON values, invalid json, invalid headers, request too long, interrupted request etc.

There is more validation to be done in the POST endpoint.

The API could be documented using the OpenAPI specification. Ideally, a web framework which would generate the API docs from the code would be used so that the docs don't go out of sync with the code.

## Testing

Uses pytest:

```
$ PYTHONPATH=. pytest -v

```

Also see the docker container which runs the tests before starting.
