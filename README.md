## Phase 1: Install Visual Studio & Python

Download Visual Studio 2022:
Go to the Visual Studio website and download the Community 2022 edition (it's free).
Install the Python Workload:
Run the installer.
Go to the "Workloads" tab.
Check the box for "Python development".
In the "Installation details" panel on the right, make sure "Python 3" is checked.
Click "Install" and wait for it to complete.

## Phase 2: Create and Structure Your Project

Create a New Project:
Open Visual Studio 2022.
On the start screen, click "Create a new project".
In the search bar, type "Python".
Select the template named "Python Application" and click "Next".
Configure your project:
Project name: skyy_facial_recognition
Location: Choose where to save your project.
Click "Create".
Set Up the Project Structure:
Visual Studio will create a project with a single .py file.
In the "Solution Explorer" panel (usually on the right), you'll see your project.
Rename the main file: Right-click the .py file (it might be named skyy_facial_recognition.py) and rename it to main.py.
Create the src folder: Right-click the skyy_facial_recognition project (the bold one) -> Add -> New Folder. Name it src.
Create the application_data folder: Right-click the project again -> Add -> New Folder. Name it application_data.
Inside application_data, create three more folders: database, images, and logs1.


Move main.py into src:
Drag and drop the main.py file from the root into the src folder.
Create All Other Project Files:
Top-Level Files:
Right-click the skyy_facial_recognition project -> Add -> New Item.
Select "Empty File", name it config.json, and click Add.
Do this again to create requirements.txt.
src Folder Files:
Right-click the src folder -> Add -> New Item.
Select "Empty Python File" for each of these:
__init__.py (This tells Python src is a module)
api.py
camera.py
config.py
controller.py
database.py
encryption.py
facial_recognition.py
Your Solution Explorer should now look like this:Solution 'skyy_facial_recognition'
└── skyy_facial_recognition
    ├── application_data
    │   ├── database
    │   ├── images
    │   └── logs
    ├── src
    │   ├── __init__.py
    │   ├── api.py
    │   ├── camera.py
    │   ├── config.py
    │   ├── controller.py
    │   ├── database.py
    │   ├── encryption.py
    │   ├── facial_recognition.py
    │   └── main.py
    ├── config.json
    └── requirements.txt


## Phase 3: Add Code and Install Dependencies

Populate All Files:
Open each file you created (e.g., config.json, src/config.py, etc.).
Copy and paste the code from my previous answers into the correct, corresponding file.
Crucial src/api.py Tweak: Make sure you use the final, updated version of src/api.py that uses request: Request and controller = request.app.state.controller in each API function.
Create the Python Environment:
In the Solution Explorer, right-click on "Python Environments" -> Add Environment....
Select "Virtual environment".
A good name for it is .venv.
For the "Install packages from file" option, enter requirements.txt.
Click "Create".
Visual Studio will now automatically create the virtual environment and pip install all the libraries from your requirements.txt. You can watch the progress in the "Output" window.

## Phase 4: Run and Test the Application

Set the Startup File:
Visual Studio will try to run the project's root .py file, but we moved ours.
Right-click the skyy_facial_recognition project -> Properties.
In the "General" tab, find the "Startup File" field.
Change it from main.py to src/main.py.
Click Save (or Ctrl+S).
Run the Project:
Click the Start button (green arrow) in the toolbar or press F5.
A console window will open. You should see all the loguru messages, starting with "Logging configured," "Initializing services..." and ending with the Uvicorn server startup messages.
It will say something like: INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit).
Test Your "Real MCP" API:
While your project is running, you can test it.
Visual Studio 2022 has a built-in "Endpoints Explorer" for web APIs.
Go to View -> Other Windows -> Endpoints Explorer.
It should automatically find your FastAPI project. You will see your four POST endpoints listed.
Right-click /facial_recognition/register_user -> Generate Request.
A new .http file will open. This is a built-in REST client.
Modify the JSON body to look like the SRS sample 2, but for registration (you'll need a real base64-encoded image of a face for this to work).


Click the green "Send Request" button.
That's it! You now have the full application running inside Visual Studio, complete with a virtual environment and a real-time API server.
