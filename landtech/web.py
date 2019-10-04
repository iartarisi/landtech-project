from flask import Flask, jsonify, request
from geojson import Point, Feature, FeatureCollection
import numpy as np


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


DATABASE_FILE = 'sold-price-data.txt'


def percentiles(prices, percs=None):
    """Return a function which calculates percentiles given a list of `prices`

    The returned function will take on param `n` and return the
    percentile in which it can be found (from the list `percs`)
    """
    if percs is None:
        percs = [5, 25, 75, 90, 100]

    array = np.array(prices)
    res = np.percentile(array, percs)

    # return a closure which uses the computation from above (no need to
    # recalculate percentiles)
    def percentile(n):
        for label, perc in zip(percs, res):
            if n <= perc:
                return label

    return percentile


def fetch_features():
    """Return a FeatureCollection with all the data we have"""
    places = []
    with open(DATABASE_FILE) as f:
        for line in f:
            # TODO add validation
            x, y, p = line.split()
            x, y, p = int(x), int(y), int(p)
            places.append((x, y, p))

    prices = [p for x, y, p in places]
    percentile = percentiles(prices)

    features = []
    for (x, y, p) in places:
        point = Point((x, y))
        perc = percentile(p)
        feature = Feature(
            geometry=point, properties={'price': p, 'percentile': perc})
        features.append(feature)

    feature_collection = FeatureCollection(features)
    return feature_collection


@app.route('/places/', methods=['GET'])
def places_index():
    """Return all the places in the database

    Returns a {'places': GeoJSON document} JSON
    """
    # this isn't realistic; I don't think there would be an occasion
    # where we'd want to retrieve all of the places. This method would
    # have to require some sort of filtering
    feature_collection = fetch_features()
    resp = {'places': feature_collection}
    return jsonify(resp)


@app.route('/places/', methods=['POST'])
def places_post():
    """Create a new place

    Expects a GeoJSON Feature
    """
    body = request.get_json()
    feature = Feature(**body)

    # XXX add more validation
    if not feature.is_valid:
        return {'error': 'Invalid GeoJSON. Expected a Feature.'}, 400

    x, y = feature['geometry']['coordinates']
    p = feature['properties']['price']

    with open(DATABASE_FILE, 'a') as df:
        df.write(f"{x} {y} {p}\n")

    return '', 201
