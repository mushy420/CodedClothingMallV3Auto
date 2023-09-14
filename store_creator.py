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

# Create the main window
root = tk.Tk()
root.title("Coded Clothing Mall V3 Store Creator")
root.geometry("400x300")
root.configure(bg="#8B5FBF")

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

# Create the button
create_button = tk.Button(root, text="Create Stores", font=("Arial", 12), command=handle_click)
create_button.pack(pady=20)

# Run the GUI
root.mainloop()
