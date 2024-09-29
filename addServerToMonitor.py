# program to add a server to the list after creating your pickle file

import pickle
from ServerPulse import serverpulse

# Load the existing list of servers from the pickle file
servers = pickle.load(open("servers.pickle", "rb"))

print("Add a new server to the list")

# Prompt the user for details about the new server
servername = input("Enter the server's hostname or IP address: ")
port = int(input("Enter the port number (e.g., 80, 443): "))
connection = input("Enter the connection type (ping, plain, ssl): ")
priority = input("Enter the priority level (high, low): ")

# Create a new Server object with the provided details
new_server = serverpulse(servername, port, connection, priority)

# Add the new server to the list
servers.append(new_server)

# Save the updated list of servers back to the pickle file
pickle.dump(servers, open("servers.pickle", "wb"))

print("Server added successfully.")
