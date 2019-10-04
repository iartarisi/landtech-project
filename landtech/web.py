from flask import Flask, jsonify
from geojson import Point, Feature, FeatureCollection


def create_app():
    app = Flask(__name__)
    return app


app = create_app()

@app.route('/places/')
def index():
    features = []
    with open('sold-price-data.txt') as f:
        for line in f:
            # TODO add validation
            x, y, p = line.split()
            x, y, p = int(x), int(y), int(p)

            point = Point((x, y))
            feature = Feature(geometry=point, properties={'price': p})
            features.append(feature)

    feature_collection = FeatureCollection(features)

    resp = {'price_data': feature_collection}
    return jsonify(resp)
