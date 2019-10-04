from landtech import web


def test_places(client):
    # When making a GET request to the 'places' index
    resp = client.get('/places/', json=True)

    # Then the response will contain all the features
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert 'places' in resp_json
    assert resp_json['places']['type'] == 'FeatureCollection'
    features = resp_json['places']['features']
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


def test_post(client):
    # Given a valid place
    feature = {
        'geometry': {
            'coordinates': [10, 10],
            'type': 'Point'},
        'properties': {'price': 123456},
        'type': 'Feature'}

    # When making a valid POST request to the places API
    resp = client.post(
        '/places/',
        json=feature)

    # Then the request will be accepted
    assert resp.status_code == 201
    assert resp.data == b''

    # And a subsequent request will return the new place
    resp = client.get('/places/', json=True)
    new_feature = resp.get_json()['places']['features'][-1]
    # can't assert on percentile because it's non-deterministic
    del new_feature['properties']['percentile']
    assert new_feature == feature


def test_invalid_post(client):
    # Given an invalid document (but valid JSON)
    invalid = {
        'geometry': {
            'coordinates': [10, 10, 10, 10, 10],
            'type': 'Point'},
        'properties': {'price': 123456},
        'type': 'Feature'}

    # When making a POST request to the places API
    resp = client.post('/places/', json=invalid)

    # Then the request will return a 400
    assert resp.status_code == 400
    assert resp.get_json() == {'error': 'Invalid GeoJSON. Expected a Feature.'}


def test_percentiles():
    perc = web.percentiles([1, 1, 2, 5, 100, 5, 9, 5, 5, 10])
    assert perc(1) == 5
    assert perc(2) == 25
    assert perc(5) == 75
    assert perc(9) == 90
    assert perc(100) == 100
