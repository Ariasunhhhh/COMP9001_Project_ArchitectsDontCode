# Rhino AI – Architects Don't Code

**Rhino AI** is an intelligent architectural modeling generator that streamlines the architectural modelling process in Rhino 3D.  
By leveraging natural language input and AI-generated scripting, this tool empowers users to create parametric models without writing any code.

Designed for students, designers, and Rhino beginners, Rhino AI enables quick architectural prototyping with ease and clarity.

---

##  Features

- **Natural Language to Geometry**  
  Describe your desired structure in plain English and receive geometry parameters ready for modelling.

- **Automated Code Generation**  
  Generate full Rhino Python scripts using RhinoScriptSyntax, ready to run in Rhino's editor.

- **Interactive Parameter Control**  
  Adjust model dimensions through intuitive sliders based on AI-suggested ranges.

- **Beginner-Friendly Instructions**  
  Step-by-step guidance on how to run the code in Rhino, tailored for users with no prior experience.

- **Error Feedback & Fixing**  
  Submit error messages or personal feedback to automatically correct or improve the generated code.

- **Get Script Documentation**  
  Automatically saves Rhino Python script to the desktop.
  
---

##  How to Use

### 1. Install Dependencies
| Package         | Purpose                                                                       |
| --------------- | ----------------------------------------------------------------------------- |
| `streamlit`     | Web-based UI framework for creating the interactive app interface.            |
| `openai`        | Connects to OpenAI’s GPT API for generating parameters, code, and fixes.      |
| `python-dotenv` | Loads environment variables (e.g., your API key) securely from a `.env` file. |
| `os`            | Handles file paths, directories, and file saving operations.                  |
| `datetime`      | Generates timestamped filenames for saved Python scripts.                     |
| `json`          | Used to handle API responses in JSON format.                                  |
| `re`            | Regular expressions used to extract code blocks and handle errors.            |

### 2. Configure API Access  
You must obtain an OpenAI API key to use this application. 

Create a .env file in the root directory with the following content:  
OPENAI_API_KEY = your-api-key-here

### 3. Requirements

- **Rhino 8**  
  Required for executing the generated Python scripts.  
  _USYD students: please refer to the university’s installation guide._

- **Python Third-party packages**  
  These will be installed via `pip`:

  ```text
  streamlit>=1.35.0
  openai>=1.14.0
  python-dotenv>=1.0.1  

### 4. Launch the App  
To start the Rhino AI assistant interface, run the following command in your terminal:  
streamlit run main.py  
Once launched, a browser window will open automatically at http://localhost:8501.  

### 5. Model in Rhino  
- Describe your building idea (e.g.,  
“A twisting modern tower with a wide base”  
or  
“A cool skyscraper in modernist style, inspired by the architecture of Shanghai's Bund”)    
- Click “Generate Parameters” to get dimension sliders  
- Adjust values using the sliders  
- Click “Generate Code” to get a Rhino Python script  
- Follow the step-by-step instructions shown in the app  
- Paste the script into Rhino’s Python editor (EditPythonScript) and run it  
- Done! Your model is now created  

---

##  Components

The system consists of three main components:
| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `main.py`          | The Streamlit front-end application. Handles UI logic and user interaction. |
| `assistant.py`     | The AI logic layer. Contains the `RhinoModelingAssistant` class that communicates with OpenAI to generate parameters, code, and feedback loops. |
| `.env`             | Stores your OpenAI API key.                |

##  Demo  
https://github.com/user-attachments/assets/99071303-e312-406a-b201-f2a30626b9f3  

Final result  
![1748177978304](https://github.com/user-attachments/assets/27867fd4-4826-431e-a6c7-781d3abd5be2)





