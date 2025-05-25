# import libraries
import streamlit as st
import os
from datetime import datetime
from assistant import RhinoModelingAssistant
from dotenv import load_dotenv


# ----------------------------
# File Management Functions
# ----------------------------

def save_code_to_file(code: str, folder: str = "~/Desktop/RhinoScripts") -> str:
    """
    Saves generated Python code to a timestamped file.
    
    Features:
    - Creates target directory if not exists
    - Uses cross-platform path expansion (~ handling)
    - Generates human-readable timestamped filenames
    - Ensures UTF-8 encoding for special characters
    
    Args:
        code (str): Python code to save
        folder (str): Target directory (default: Desktop/RhinoScripts)
    
    Returns:
        str: Filename of the saved script
    """

    formatted_time = datetime.now().strftime('%Y-%m-%d_%I-%M-%S_%p')
    filename = f"rhino_model_{formatted_time}.py"
    path = os.path.join(os.path.expanduser(folder), filename)

    # Create the folder if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Write the code to the file
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    return filename


# ----------------------------
# Application Initialization
# ----------------------------

# Initialize API client and assistant

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(" API key not found. Please check your .env file.")
    st.stop()
assistant = RhinoModelingAssistant(api_key = api_key)

# Set up Streamlit page configuration
st.set_page_config(page_title="Rhino AI",)
st.title("🏠 Architectural Model Generator")


# ----------------------------
# Session State Management
# ----------------------------

# Initialize session state variables to store model parameters, instructions, and code
if "model_parameters" not in st.session_state:
    st.session_state.model_parameters = {}
if "modeling_instructions" not in st.session_state:
    st.session_state.modeling_instructions = ""
if "rhino_python_script" not in st.session_state:
    st.session_state.rhino_python_script = ""


# ----------------------------
# User Input Section
# ----------------------------

# Architectural description input with example guidance
shape_description = st.text_input(
    "📝 Describe your building style",
    "For example: A cool skyscraper in modernist style, inspired by the architecture of Shanghai's Bund",
    help=("Describe the object you wish to model in architectural terms. "
    "For example, 'A modernist skyscraper with curvature and symmetry inspired by New York city."
    )
)


# ----------------------------
# Parameter Generation Flow
# ----------------------------

# Suggest parameters: # When the user clicks the button, prompt will be sent to the openai API, which will return a Python Dictionary with parameters.
if st.button("🛠️ Generate Parameters"):
    params = assistant.suggest_parameters(shape_description)
    if params:
        st.session_state.model_parameters = params
    else:
        st.error("Failed to extract parameters. Please try again.")


# ----------------------------
# Parameter Adjustment Interface
# ----------------------------

# Adjust parameters and generate code
if st.session_state.model_parameters:
    st.subheader("🔧 Adjust Parameters")
    tuned_parameters = {}
    with st.form("parameters_form"):
        for name, specs in st.session_state.model_parameters.items():
            tuned_parameters[name] = st.slider(
                label=name,
                min_value=float(specs["min"]),
                max_value=float(specs["max"]),
                value=float(specs["default"]),
                step=float(specs["step"])
            )
        if st.form_submit_button("Get Rhino Code 💻"):
            # Generate modeling steps and code
            st.session_state.modeling_instructions = assistant.generate_steps(
                tuned_parameters)
            st.session_state.rhino_python_script = assistant.generate_code(
                tuned_parameters)


# ----------------------------
# Modeling Instructions Display
# ----------------------------
if st.session_state.modeling_instructions:
    st.subheader("Rhino Modeling Steps")
    st.write(st.session_state.modeling_instructions)


# ----------------------------
# Code Display & Management
# ----------------------------

# Display and save Rhino Python script
if st.session_state.rhino_python_script:
    st.subheader("Rhino Python Code")
    filename = save_code_to_file(st.session_state.rhino_python_script)
    filepath = os.path.join(os.path.expanduser("~/Desktop/RhinoScripts"), filename)
    st.success(f"✅ Script auto-saved at:\n ` {filepath} `")
    st.code(st.session_state.rhino_python_script, language="python")


# ----------------------------
# Code Feedback System
# ----------------------------

# Provide feedback loop for code adjustments
st.subheader("Code Feedback and Adjustment")
revision_request = st.text_area(
    "Want to adjust the code or got an Error? Enter your query here:",)

if st.button("Improve Code") and revision_request:
    original_code = st.session_state.rhino_python_script

    corrected = assistant.fix_code_with_feedback(
        code=original_code,
        feedback=revision_request
    )
    st.session_state.rhino_python_script = corrected

    with st.spinner("🧠 Analyzing Feedback..."):
        summary = assistant.summarize_code_changes(original_code, corrected)
        st.subheader("📝 Summary of Changes")
        st.markdown(summary)


    st.subheader("🧾 Modified Rhino Script")

    filename = save_code_to_file(corrected)
    full_path = os.path.join(os.path.expanduser("~/Desktop/RhinoScripts"), filename)
    st.success(f"✅ Modified script auto-saved at:\n `{full_path}`")

    st.code(corrected, language="python")

    
