# this file contain list of server and code to provide the next server in round robin fashion
# this will be usefull for load balancing , when we have multiple server and we want to distribute the load evenly

server_list = ["localhost:8001", "localhost:8002", "localhost:8003"]
pointer = 0

def get_next_server():                # this function will return the next server in round robin fashion i.e. one by one according to the server_list
    global pointer                    # pointer is used to keep track of the current server and we need to specify in python that this is a global variable
    if pointer>= len(server_list):
        pointer = 0
    selected_server = server_list[pointer]
    pointer += 1
    return selected_server