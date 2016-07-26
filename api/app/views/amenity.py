from flask import Flask, request, make_response, jsonify
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from app import app


@app.route('/amenities', methods=['GET', 'POST'])
def handle_amenity():
    '''Returns all amenities as JSON objects in an array with a GET request.
    Adds an amenity with a POST request.
    '''
    if request.method == 'GET':
        arr = []
        for amenity in Amenity.select():
            arr.append(amenity.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        try:
            Amenity.select().where(Amenity.name == request.form['name']).get()
            return make_response(jsonify(code=10003, msg="Name already " +
                                         "exists"), 409)
        except Amenity.DoesNotExist:
            params = request.values
            amenity = Amenity()
            for key in params:
                setattr(amenity, key, params.get(key))
            amenity.save()
            return jsonify(amenity.to_hash()), 200


@app.route('/amenities/<int:amenity_id>', methods=['GET', 'DELETE'])
def handle_amenity_id(amenity_id):
    '''Returns a JSON object of the amenity with the id passed as parameter
    with a GET request method. Removes an amenity with DELETE request method.

    Keyword arguments:
    amenity_id: The id of the amenity.
    '''
    try:
        amenity = Amenity.select().where(Amenity.id == amenity_id).get()
    except Amenity.DoesNotExist:
        raise Exception("There is no amenity with this id.")

    if request.method == 'GET':
        return jsonify(amenity.to_hash()), 200

    elif request.method == 'DELETE':
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        return make_response(jsonify(msg="Amenity deleted successfully."), 200)


@app.route('/places/<int:place_id>/amenities', methods=['GET'])
def handle_place_id_amenity(place_id):
    '''Returns all amenities of the place_id as JSON objects in an array with a
    GET request.

    Keyword arguments:
    place_id: The id of the amenity.
    '''
    try:
        PlaceAmenities.select().where(PlaceAmenities.place == place_id).get()
    except PlaceAmenities.DoesNotExist:
        return make_response(jsonify(msg="Amenity does not exist."), 404)

    if request.method == 'GET':
        arr = []
        for this in (PlaceAmenities
                     .select()
                     .where(PlaceAmenities.place == place_id)):
            arr.append(this.amenity.to_hash())

        return jsonify(arr), 200


@app.route('/places/<int:place_id>/amenities/<int:amenity_id>',
           methods=['POST', 'DELETE'])
def handle_amenity_for_place(place_id, amenity_id):
    '''Add the amenity with `amenity_id` to the place with `place_id` with a
    POST request. Delete the amenity with the id of `amenity_id` with a DELETE
    request.

    Keyword arguments:
    place_id -- The id of the place.
    amenity_id -- The id of the amenity.
    '''
    try:
        Amenity.select().where(Amenity.id == amenity_id).get()
    except Amenity.DoesNotExist:
        return make_response(jsonify(msg="Amenity does not exist."), 404)
    try:
        Place.select().where(Place.id == place_id).get()
    except Place.DoesNotExist:
        return make_response(jsonify(msg="Place does not exist."), 404)

    if request.method == 'POST':
        '''Save the connection in the ReviewPlace table.'''
        PlaceAmenities().create(place=place_id, amenity=amenity_id)

        return make_response(jsonify(msg="Amenity added to place " +
                                     "successfully."), 201)

    elif request.method == 'DELETE':
        (PlaceAmenities
         .delete()
         .where((PlaceAmenities.place == place_id) &
                (PlaceAmenities.amenity == amenity_id))
         .execute())

        Amenity.delete().where(Amenity.id == amenity_id).execute()

        return make_response(jsonify(msg="Amenity deleted successfully."), 200)
