import json

# from .location_requests import get_single_location
# from .customer_requests import get_single_customer
import sqlite3
from models import Animal, Location, Customer

ANIMALS = [
    {"id": 1, "name": "Snickers", "species": "Dog", "locationId": 1, "customerId": 4},
    {"id": 2, "name": "Roman", "species": "Dog", "locationId": 1, "customerId": 2},
    {"id": 3, "name": "Blue", "species": "Cat", "locationId": 2, "customerId": 1},
]


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        """
        )

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )

            # Create a Location instance from the current row
            location = Location(
                row["id"], row["location_name"], row["location_address"]
            )

            # swp - Create a Customer instance from the current row
            customer = Customer(
                row["id"],
                row["customer_name"],
                row["customer_address"],
                row["customer_email"],
            )
            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            # Add the dictionary representation of the customer to the animal
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)
    return json.dumps(animals)


# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(
            data["id"],
            data["name"],
            data["breed"],
            data["status"],
            data["location_id"],
            data["customer_id"],
        )

        return json.dumps(animal.__dict__)


def get_animals_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """,
            (location_id,),
        )
        animals = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )
            animals.append(animal.__dict__)

    return json.dumps(animals)


def get_animals_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """,
            (status,),
        )
        animals = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )
            animals.append(animal.__dict__)

    return json.dumps(animals)


def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM animal
        WHERE id = ?
        """,
            (id,),
        )


def update_animal(id, new_animal):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Update the value.
            ANIMALS[index] = new_animal
            break
