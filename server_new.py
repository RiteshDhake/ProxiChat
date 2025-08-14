# import modules
import socket
import threading

HOST = '192.168.0.125'
PORT = 1234 # you can use any port b/w 0 to 65535
LISTENER_LIMIT = 5
active_client = []
active_client_socket = {} # List of all current users on the server

#Function to send message to a single client
def send_message_client(client, message):
    try:
        client.sendall(message.encode())
    except:
        # Handle case where client is disconnected
        pass

def file_handler(client):
    try:
        client.send("sending_file".encode())
        file_bytes = b""
        done = False
        while not done:
            message = client.recv(2048)
            if not message:  # Client disconnected
                break
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += message
        client.sendall(file_bytes)
        client.sendall(b"<END>")
        msg = "file_sent"
        client.sendall(msg.encode())
    except:
        # Handle disconnection during file transfer
        pass

def remove_client(username, client):
    """Remove client from active lists"""
    # Remove from active_client list
    for i, (user, cli) in enumerate(active_client):
        if user == username and cli == client:
            active_client.pop(i)
            break
    
    # Remove from active_client_socket dictionary
    if username in active_client_socket:
        del active_client_socket[username]
    
    # Close the client socket
    try:
        client.close()
    except:
        pass

# function used to listen any upcoming messages
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message == "":  # Client disconnected
                print(f"Client {username} disconnected")
                # Notify other clients
                disconnect_msg = f"{username}~left the chat"
                send_messages_to_all(disconnect_msg)
                # Remove client from active lists
                remove_client(username, client)
                break
            elif message == "sending_file":
                file_handler(client)
            elif message.startswith("@"):
                # Private message format: @username: message
                try:
                    target_username, private_message = message[1:].split(":", 1)
                    if target_username in active_client_socket:
                        active_client_socket[target_username].send(f"Private from {username}~{private_message}".encode())
                    else:
                        client.send(f"User {target_username}~not found.".encode())
                except ValueError:
                    client.send("Invalid private message format. Use @username: message".encode())
            else:
                final_msg = username + '~' + message
                send_messages_to_all(final_msg)
        except ConnectionResetError:
            # Client forcibly closed connection
            print(f"Client {username} forcibly disconnected")
            disconnect_msg = f"{username}~left the chat"
            send_messages_to_all(disconnect_msg)
            remove_client(username, client)
            break
        except Exception as e:
            # Handle other exceptions
            print(f"Error with client {username}: {e}")
            disconnect_msg = f"{username}~left the chat"
            send_messages_to_all(disconnect_msg)
            remove_client(username, client)
            break

#Function to send any message to all clients that
# are currently connected to this server
def send_messages_to_all(message):
    # Create a copy of the list to avoid modification during iteration
    clients_copy = active_client.copy()
    for user in clients_copy:
        try:
            send_message_client(user[1], message)
        except:
            # If sending fails, remove the client
            remove_client(user[0], user[1])

#function to handle client
def client_handler(client):
    # Server will listen for client message that
    # will contain username
    username = None
    try:
        while True:
            # recv is used to listen message from client
            # 2048 specifies the length of message
            # utf-8 is the encoding used
            username = client.recv(2048).decode('utf-8')
            if username != "":
                active_client.append((username, client))
                active_client_socket[username] = client

                  # --- ADD THE NEW LOGIC HERE ---
                # 1. Get the list of all current usernames
                current_users = [user for user, _ in active_client]
                
                # 2. Format the list into a string
                active_users_list_str = "active_users:" + ",".join(current_users)
                
                # 3. Send the list to the new client only
                send_message_client(client, active_users_list_str)

                prompt_message = f"{username}~joined the chat"
                send_messages_to_all(prompt_message)
                break
            else:
                print("Client Username is empty")
    except:
        print("Error receiving username from client")
        client.close()
        return
    
    # Start listening for messages from this client
    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    #Creating the socket class object
    # AF_INET = we are using IPV4,
    #SOCK_STREAM = using TCP protocol
    # if you want to use UDP use SOCK_DGRAM
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow socket reuse
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Creating try catch block
    try:
        server.bind((HOST, PORT))  # passing socket (socket = ip+port)
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
        return
    
    # SET SERVER LIMIT
    server.listen(LISTENER_LIMIT)
    
    # Listening to client connection
    while True:
        try:
            client, address = server.accept()
            # address is tuple where 0th item = host_ip
            # 1st item = port
            print(f"Connected to Client {address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()
        except KeyboardInterrupt:
            print("Server shutting down...")
            break
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()