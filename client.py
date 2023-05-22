import socket
import sqlite3

def send_query(query):
    """
    Sends a query to the server and receives the result.
    """
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(('localhost', 8888))
    print("Connected to the server.")

    # Send the query to the server
    client_socket.sendall(query.encode('utf-8'))

    # Receive and print the query result
    result = client_socket.recv(1024).decode('utf-8')
    print(result)

    # Close the client socket
    client_socket.close()

# Specify the SQLite query
query = f"SELECT json_group_array(json_object('name', data->'name')) FROM products WHERE CAST(data->'price' AS INTEGER) > 8;"
print(query)

# Send the query to the server
send_query(query)

