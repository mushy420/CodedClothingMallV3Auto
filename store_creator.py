import tkinter as tk
import time
import requests

# Define the function to create stores
def create_stores(num_stores, group_ids):
    # Loop through the group IDs
    for group_id in group_ids:
        # Get the group owner
        group_info = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}").json()
        owner_id = group_info["owner"]["userId"]
        
        # Get the player and their character
        player = requests.get(f"http://localhost:6463/rpc?v=1&id=1&name=GetUserByUserId&args=[{owner_id}]").json()["result"]["username"]
        character = None
        while not character:
            try:
                character = requests.get(f"http://localhost:6463/game/join?placeId=7406897155&playerName={player}&accessCode=&spawnLocationName=SpawnLocation&spawnLocationType=CFrame").json()["data"]["character"]
            except:
                time.sleep(1)
        
        # Get the owner's clothing items
        clothing_items = requests.get(f"https://inventory.roblox.com/v2/users/{owner_id}/inventory").json()["data"]
        shirt_id = None
        pants_id = None
        for item in clothing_items:
            if item["assetType"]["name"] == "Shirt":
                shirt_id = item["assetId"]
            elif item["assetType"]["name"] == "Pants":
                pants_id = item["assetId"]
            if shirt_id and pants_id:
                break
        
        # Loop through the number of stores
        for i in range(num_stores):
            # Get the player's store
            store = None
            while not store:
                try:
                    store = requests.get(f"http://localhost:6463/game/getallchildren?characterId={character}&classname=Model&name=Store").json()["data"][0]
                except:
                    time.sleep(1)
            
            # Press the E key to claim the store
            requests.post(f"http://localhost:6463/game/sendkey?playerName={player}&keyCode=Enum.KeyCode.E&isKeyDown=true")
            time.sleep(0.5)
            requests.post(f"http://localhost:6463/game/sendkey?playerName={player}&keyCode=Enum.KeyCode.E&isKeyDown=false")
            
            # Leave the store
            requests.post(f"http://localhost:6463/game/leavegame?playerName={player}")
            time.sleep(1)
            
            # Rent a new store
            requests.post(f"http://localhost:6463/game/buygamepass?playerName={player}&gamePassId=123456789")
            time.sleep(1)
            
            # Rejoin the game
            character = None
            while not character:
                try:
                    character = requests.get(f"http://localhost:6463/game/join?placeId=7406897155&playerName={player}&accessCode=&spawnLocationName=SpawnLocation&spawnLocationType=CFrame").json()["data"]["character"]
                except:
                    time.sleep(1)
            
            # Get the player's new store
            new_store = None
            while not new_store:
                try:
                    new_store = requests.get(f"http://localhost:6463/game/getallchildren?characterId={character}&classname=Model&name=Store").json()["data"][0]
                except:
                    time.sleep(1)
            
            # Add the owner's shirt and pants to the new store
            shirt = requests.post(f"http://localhost:6463/game/createinstance?className=Shirt&parent={new_store}&properties.ShirtTemplate=http://www.roblox.com/asset/?id={shirt_id}").json()["data"]["instanceId"]
            pants = requests.post(f"http://localhost:6463/game/createinstance?className=Pants&parent={new_store}&properties.PantsTemplate=http://www.roblox.com/asset/?id={pants_id}").json()["data"]["instanceId"]
            
            # Print the store information
            print(f"Store {i+1} created with Shirt ID {shirt_id} and Pants ID {pants_id} using Group ID {group_id}")
            
            # Load the player's store
            requests.post(f"http://localhost:6463/game/teleportplayer?playerName={player}&placeId=7406897155&spawnName={store}")
            time.sleep(1)

# Define the function to handle errors
def handle_error(error):
    error_window = tk.Toplevel()
    error_window.title("Error")
    error_window.geometry("300x100")
    error_label = tk.Label(error_window, text=error)
    error_label.pack(pady=20)
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(pady=10)

# Define the function to handle the button click
def handle_click():
    # Get the values from the entry boxes
    num_stores = int(num_stores_entry.get())
    group_ids = group_ids_entry.get().split(",")
    group_ids = [int(group_id.strip()) for group_id in group_ids]
    
    # Call the create_stores function and handle errors
    try:
        create_stores(num_stores, group_ids)
    except Exception as e:
        handle_error(str(e))

# Define the function to start the script
def start_script():
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    handle_click()

# Define the function to stop the script
def stop_script():
    start_button.config(state="normal")
    stop_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("Coded Clothing Mall V3 Store Creator")
root.geometry("400x400")

# Create the gradient background
gradient = tk.Canvas(root, width=400, height=400)
gradient.pack()
gradient.create_rectangle(0, 0, 400, 400, fill="#8B5FBF", outline="")
for i in range(400):
    gradient.create_line(0, i, 400, i, fill=f"#{i:02x}00ff")

# Create the title label
title_label = tk.Label(root, text="Coded Clothing Mall V3 Store Creator", font=("Arial", 20), bg="#8B5FBF", fg="white")
title_label.pack(pady=20)

# Create the entry boxes
num_stores_label = tk.Label(root, text="Number of Stores:", font=("Arial", 12), bg="#8B5FBF", fg="white")
num_stores_label.pack()
num_stores_entry = tk.Entry(root, font=("Arial", 12))
num_stores_entry.pack(pady=10)

group_ids_label = tk.Label(root, text="Group IDs (comma-separated):", font=("Arial", 12), bg="#8B5FBF", fg="white")
group_ids_label.pack()
group_ids_entry = tk.Entry(root, font=("Arial", 12))
group_ids_entry.pack(pady=10)

# Create the start/stop buttons
button_frame = tk.Frame(root, bg="#8B5FBF")
button_frame.pack(pady=20)
start_button = tk.Button(button_frame, text="Start", font=("Arial", 12), command=start_script)
start_button.pack(side=tk.LEFT, padx=10)
stop_button = tk.Button(button_frame, text="Stop", font=("Arial", 12), command=stop_script, state="disabled")
stop_button.pack(side=tk.LEFT, padx=10)

# Run the GUI
root.mainloop()
