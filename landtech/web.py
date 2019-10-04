from flask import Flask, jsonify
from geojson import Point, Feature, FeatureCollection


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


def fetch_features():
    """Return a FeatureCollection with all the data we have"""
    places = []
    with open('sold-price-data.txt') as f:
        for line in f:
            # TODO add validation
            x, y, p = line.split()
            x, y, p = int(x), int(y), int(p)
            places.append((x, y, p))

    features = []
    for (x, y, p) in places:
        point = Point((x, y))
        feature = Feature(geometry=point, properties={'price': p})
        features.append(feature)

    feature_collection = FeatureCollection(features)
    return feature_collection


@app.route('/places/')
def places_index():
    """Return all the places in the database

    Returns a {'price_data': GeoJSON document} JSON
    """
    # this isn't realistic; I don't think there would be an occasion
    # where we'd want to retrieve all of the places. This method would
    # have to require some sort of filtering
    feature_collection = fetch_features()
    resp = {'price_data': feature_collection}
    return jsonify(resp)
