import ssl
import socket
import subprocess
import platform
import pickle
from datetime import datetime
import time

# from sendAlert import emailNotification

class serverpulse():
    def __init__(self, serverName, serverPort, connectionType, priorityLevel) -> None:

        self.name = serverName
        self.port = serverPort
        self.connection = connectionType.lower()
        self.priority = priorityLevel.lower()

        self.history = []
        self.alert = False

    def check_connection(self):
        success = False
        msg = ""
        now = datetime.now()

        try:
            if self.connection == "plain":
                # Attempt a plain TCP connection
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"'{self.name}' is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False  # Disable alert if connection is successful

            elif self.connection == "ssl":
                # Attempt an SSL-secured connection
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"'{self.name}' is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False  # Disable alert if connection is successful

            else:
                # Fallback to ping if connection type is unknown
                if self.ping():
                    msg = f"'{self.name}' is up. On port {self.port} with {self.connection}"
                    success = True
                    self.alert = False  # Disable alert if ping is successful
        # Handeling edgeCases
        except socket.timeout:
            # This exception occurs when the connection attempt exceeds the allowed time limit.
            # It typically happens if the server is unresponsive or unreachable within the timeout period.
            msg = f"Server: {self.name} timeout. On port {self.port}"

        except (ConnectionRefusedError, ConnectionResetError) as e:
            # ConnectionRefusedError: Occurs when the server is refusing the connection.
            # This might mean the server is up but not accepting connections on the specified port.
            
            # ConnectionResetError: Happens when the connection is forcibly closed by the server.
            # This could occur due to a server crash or the server intentionally closing the connection.
            msg = f"Server: {self.name}, {e}"

        except Exception as e:
            # A catch-all for any other exceptions that are not specifically handled above.
            # This will handle any unexpected errors and log a generic message.
            msg = f"Unknown error: {e}"
        
        if success == False and self.alert == False:
            # Send Alert
            self.alert = True
            # future implementation
            # Uncomment when wanted to use 
            # emailNotification(self.name,f"{msg}\n{now}","test@xyz.com")


        self.history_logger(msg,success,now)

    def history_logger(self, msg, success, now):
        history_max = 100
        self.history.append((msg,success,now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            # Determine the correct flag for the number of packets based on the OS
            count_flag = 'n' if platform.system().lower() == "windows" else 'c'
            
            # Run the ping command
            output = subprocess.check_output(
                f"ping -{count_flag} 1 {self.name}",
                shell=True,
                universal_newlines=True
            )
            
            # Check if the output contains 'unreachable'
            if 'unreachable' in output:
                return False
            else:
                return True
        
        except Exception:
            return False
        
if __name__ == "__main__":
    try:
        # Load the saved servers list from a pickle file
        servers = pickle.load(open("servers.pickle", "rb"))
    except:
        # If loading fails, define a default list of servers, add below
        servers = [
            serverpulse("google.com", 80, "plain", "high") # example server
        ]

    start_time = time.time()
    duration = 60  # Duration in seconds (1 min)
    # Check connection for each server and print the history length
    while time.time() - start_time < duration:
        for server in servers:
            server.check_connection()
            print(len(server.history))
            print(server.history[-1])

        # Save the updated list of servers back to the pickle file
        pickle.dump(servers, open("servers.pickle", "wb"))

        # Sleep for 5 minutes before the next check
        time.sleep(5)  # 300 seconds = 5 second


    

