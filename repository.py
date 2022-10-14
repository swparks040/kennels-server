DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 4,
        },
        {"id": 2, "name": "Roman", "species": "Dog", "locationId": 1, "customerId": 2},
        {"id": 3, "name": "Blue", "species": "Cat", "locationId": 2, "customerId": 1},
    ],
    "customers": [{"id": 1, "name": "Jenna Solis"}],
    "employees": [{"id": 1, "name": "Jenna Solis"}],
    "locations": [
        {"id": 1, "name": "Nashville North", "address": "8422 Johnson Pike"},
        {"id": 2, "name": "Nashville South", "address": "209 Emory Drive"},
    ],
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, id):
    """For GET requests to a single resource"""
    requested_data = None

    for data in DATABASE[resource]:
        if data["id"] == id:
            requested_data = data

            if resource == "animals":
                matching_location = retrieve(requested_data["locationId"], "locations")
                requested_data["location"] = matching_location
                matching_customer = retrieve(requested_data["customerId"], "customers")
                requested_data["customer"] = matching_customer
                requested_data.pop("locationId", None)
                requested_data.pop("customerId", None)
    return requested_data

def create(resource, new_data):
    """For POST requests to a collection"""
    max_id = DATABASE[resource][-1]["id"]
    new_id = max_id + 1
    new_data["id"] = new_id
    DATABASE[resource].append(new_data)
    return new_data

def update(resource, id, edited_data):
    """For PUT requests to a single resource"""
    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            DATABASE[resource][index] = edited_data
            break
    return edited_data

def delete(resource, id):
    """For DELETE requests to a single resource"""
    data_index = -1
    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            # Found the data. Store the current index.
            data_index = index
    # If the animal was found, use pop(int) to remove it from list
    if data_index >= 0:
        DATABASE[resource].pop(data_index)
