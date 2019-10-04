from landtech import web

def test_places(client):
    # When making a GET request to the 'places' index
    resp = client.get('/places/', json=True)

    # Then the response will contain all the features
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert 'price_data' in resp_json
    assert resp_json['price_data']['type'] == 'FeatureCollection'
    features = resp_json['price_data']['features']
    assert len(features) == 2500
    feature1 = features[0]
    assert feature1 == {
        'geometry': {'coordinates': [60, 23], 'type': 'Point'},
        'properties': {'price': 1422640, 'percentile': 25},
        'type': 'Feature'}
    feature_1 = features[-1]
    assert feature_1 == {
        'geometry': {'coordinates': [60, 75], 'type': 'Point'},
        'properties': {'price': 7516381, 'percentile': 75},
        'type': 'Feature'}


def test_percentiles():
    perc = web.percentiles([1, 1, 2, 5, 100, 5, 9, 5, 5, 10])
    assert perc(1) == 5
    assert perc(2) == 25
    assert perc(5) == 75
    assert perc(9) == 90
    assert perc(100) == 100
