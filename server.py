import socket
import threading
import sqlite3
import logging

# SQLite database file path
DATABASE_FILE = '/tmp/abc.db'

# Maximum number of concurrent connections
MAX_CONNECTIONS = 5

# Create a lock for accessing the database
database_lock = threading.Lock()


def handle_client(connection_socket):
    """
    Handles a client connection by receiving and executing SQLite queries.
    """
    # Create a new database connection and cursor for this client thread
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    while True:
        # Receive the query from the client
        query = connection_socket.recv(1024).decode('utf-8')
        if not query:
            break

        # Execute the query
        with database_lock:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
            except Exception as e:
                result = str(e)

        # Send the query result back to the client
        connection_socket.sendall(str(result).encode('utf-8'))

    # Close the database connection and the client connection
    cursor.close()
    connection.close()
    connection_socket.close()


def start_server():

    print(sqlite3.version)
    print(sqlite3.__file__)

    """
    Starts the server to listen for client connections.
    """
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('0.0.0.0', 8888))

    # Listen for client connections
    server_socket.listen(MAX_CONNECTIONS)
    print("Server started and listening for connections...")

    while True:
        # Accept a client connection
        connection_socket, address = server_socket.accept()
        print(f"Client connected: {address}")

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(connection_socket,))
        client_thread.start()


# Start the server
start_server()
