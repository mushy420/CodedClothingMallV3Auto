# Coded Clothing Mall V3 Store Creator

This Python script allows you to automatically create stores in the Coded Clothing Mall V3 game on Roblox using the shirt and pants of the owner of one or more Roblox groups. The script uses the requests library to interact with the Roblox API and the tkinter library to create a GUI.

## Requirements

- Python 3.x
- tkinter
- requests

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies using pip: `pip install -r requirements.txt`.
3. Run the script: `python store_creator.py`.
4. Enter the group ID(s) of the owner(s) of the shirt and pants you want to use in the "Group IDs" field of the GUI. You can enter up to 50 group IDs separated by commas. (123456, 123446, 233446, 2344566, 1234556)
5. Enter the number of stores you want to create in the "Number of Stores" field of the GUI.
6. Click the "Start" button to begin creating stores.
7. The script will automatically join the Coded Clothing Mall V3 game and create the specified number of stores using the shirt and pants of the owner(s) of the specified group ID(s).
8. To stop the script, click the "Stop" button.

## Error Handling

If the script encounters an error, an error message will be displayed in a pop-up window. Click the "OK" button to close the window. Additionally, any errors will be logged in the `store_creator.log` file.

## Disclaimer

This script is provided for educational purposes only. Use at your own risk. The author is not responsible for any damage or loss caused by the use of this script.

## Contributing

If you find any issues with the script or have suggestions for improvements, please feel free to open an issue or pull request on the GitHub repository.

## License

This script is licensed under the MIT License. See the LICENSE file for more information.
