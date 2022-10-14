import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import all, retrieve, create, update, delete


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None
        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/
        return (resource, id)  # This is a tuple

    # Here's a class function
    def get_all_or_single(self, resource, id):
        if id is not None:
            response = retrieve(resource, id)
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ""
        else:
            self._set_headers(200)
            response = all(resource)

        return response

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # self._set_headers(201)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None
        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            if (
                "name" in post_body
                and "species" in post_body
                and "locationId" in post_body
                and "customerId" in post_body
            ):
                self._set_headers(201)
                new_animal = create(resource, post_body)
            else:
                self._set_headers(400)
                new_animal = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"species is required" if "species" not in post_body else ""} {"locationId is required" if "locationId" not in post_body else ""} {"customerId is required" if "customerId" not in post_body else ""}'
                }

            # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_animal).encode())

        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create(resource, post_body)
            else:
                self._set_headers(400)
                new_location = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
                }

            # Encode the new location and send in response
            self.wfile.write(json.dumps(new_location).encode())

        if resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                new_employee = create(resource, post_body)
            else:
                self._set_headers(400)
                new_employee = {
                    "message": f'{"name is required" if "name" not in post_body else ""}'
                }

            # Encode the new employee and send in response
            self.wfile.write(json.dumps(new_employee).encode())

        if resource == "customers":
            if "name" in post_body:
                self._set_headers(201)
                new_customer = create(resource, post_body)
            else:
                self._set_headers(400)
                new_customer = {
                    "message": f'{"name is required" if "name" not in post_body else ""}'
                }

            # Encode the new customer and send in response
            self.wfile.write(json.dumps(new_customer).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Delete a single animal from the list
        update(resource, id, post_body)
        # Encode the new animal, location, employee, and customer and send in response
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    def do_DELETE(self):
        # Set a 204 response code
        # self._set_headers(204)
        response = ""
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Delete a single animal from the list
        if resource == "customers":
            response = {"message": "Unable to delete customer."}
            self._set_headers(405)
        else:
            delete(resource, id)
            self._set_headers(204)
        self.wfile.write(json.dumps(response).encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
