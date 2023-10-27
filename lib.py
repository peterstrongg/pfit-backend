import time
import os
import re

def startup_routine():
    print("[+] Running startup routine...")

    # Make sure graph directory exists and is empty
    if not (os.path.exists("graphs")):
        os.makedirs("graphs")
    else:
        for f in os.listdir("graphs"):
            if(re.match(".+\.png", f)):
                print("[+] Deleting", f, "...")
                os.remove("graphs/" + f)

    print("[+] Startup routine completed successfully.\n")
        

def del_graph(graph_name):
    if re.match("graphs.+\.png", graph_name):
        time.sleep(5)
        if os.path.exists(graph_name):
            os.remove(graph_name)