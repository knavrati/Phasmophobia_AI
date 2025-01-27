import mss
import cv2
import numpy as np
import time
import requests
import json
import base64
import os
import pyttsx3
import google.generativeai as genai
from google.auth import default
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# Initialize text-to-speech engine and provide a greeting
tts_engine = pyttsx3.init()
tts_engine.say("Hello, I am here to assist you with your ghost hunting adventure!")
tts_engine.runAndWait()

# ========== 1) Authentication ==========
# Authenticate using default credentials with cloud platform scope
credentials, project_id = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
print(f"Authenticated Project: {project_id}")

def load_credentials():
    """Load and return credentials using the client secret file."""
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    credentials_path = r'PATH_TO_YOUR_SECRET'  # Update path as needed

    # Initiate OAuth flow using client secrets
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, scopes=scopes, redirect_uri="http://localhost:8080/"
    )
    credentials = flow.run_local_server(port=8080)
    return credentials

def save_credentials(credentials):
    """Save credentials for future use."""
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())
    print("Token saved to token.json")

def get_authenticated_session():
    """Get an authenticated session, refresh if necessary."""
    credentials = None
    try:
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json')
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials = load_credentials()
                save_credentials(credentials)
    except (IOError, RefreshError) as e:
        print(f"Error loading or refreshing credentials: {e}")
    return credentials

# Obtain and configure credentials
credentials = get_authenticated_session()
genai.configure(credentials=credentials)

# ========== 2) Ghost Dictionary and Matching Function ==========
# Define ghost types and their corresponding evidence
ghosts = {
    "Spirit": {"evidence": ["EMF Level 5", "Spirit Box", "Ghost Writing"]},
    "Wraith": {"evidence": ["EMF Level 5", "Spirit Box", "D.O.T.S Projector"]},
    "Phantom": {"evidence": ["Spirit Box", "Fingerprints", "D.O.T.S Projector"]},
    "Poltergeist": {"evidence": ["Spirit Box", "Fingerprints", "Ghost Writing"]},
    "Banshee": {"evidence": ["Fingerprints", "Ghost Orb", "D.O.T.S Projector"]},
    "Jinn": {"evidence": ["EMF Level 5", "Fingerprints", "Freezing Temperatures"]},
    "Mare": {"evidence": ["Spirit Box", "Ghost Orb", "Ghost Writing"]},
    "Shade": {"evidence": ["EMF Level 5", "Ghost Writing", "Freezing Temperatures"]},
    "Demon": {"evidence": ["Fingerprints", "Ghost Writing", "Freezing Temperatures"]},
    "Yurei": {"evidence": ["Ghost Orb", "Freezing Temperatures", "D.O.T.S Projector"]},
    "Oni": {"evidence": ["EMF Level 5", "Freezing Temperatures", "D.O.T.S Projector"]},
    "Hantu": {"evidence": ["Fingerprints", "Ghost Orb", "Ghost Writing"]},
    "Yokai": {"evidence": ["Spirit Box", "Ghost Orb", "D.O.T.S Projector"]},
    "Goryo": {"evidence": ["EMF Level 5", "Fingerprints", "D.O.T.S Projector"]},
    "Myling": {"evidence": ["EMF Level 5", "Fingerprints", "Ghost Writing"]},
    "Onryo": {"evidence": ["Spirit Box", "Ghost Orb", "Freezing Temperatures"]},
    "The Twins": {"evidence": ["EMF Level 5", "Spirit Box", "Freezing Temperatures"]},
    "Raiju": {"evidence": ["EMF Level 5", "Ghost Orb", "D.O.T.S Projector"]},
    "Obake": {"evidence": ["EMF Level 5", "Fingerprints", "Ghost Orb"]},
    "The Mimic": {"evidence": ["Spirit Box", "Fingerprints", "Freezing Temperatures"]},
    "Revenant": {"evidence": ["Ghost Orb", "Ghost Writing", "Freezing Temperatures"]},
    "Moroi": {"evidence": ["Spirit Box", "Ghost Writing", "Freezing Temperatures"]},
    "Deogen": {"evidence": ["Spirit Box", "Ghost Writing", "D.O.T.S Projector"]},
    "Thaye": {"evidence": ["Ghost Orb", "Ghost Writing", "D.O.T.S Projector"]},
}

def match_ghost_to_evidence(evidence_list, ghost_database):
    """
    Return all ghosts whose evidence exactly matches the given evidence_list.
    """
    evidence_set = set(evidence_list)
    matching = []
    for ghost, details in ghost_database.items():
        ghost_evidence_set = set(details["evidence"])
        if evidence_set == ghost_evidence_set:
            matching.append(ghost)
    return matching if matching else ["No matching ghost"]

def image_to_base64(path_to_image):
    """Convert an image file to a base64-encoded string."""
    with open(path_to_image, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Example usage: Convert reference images to base64
spirit_box_b64 = image_to_base64(r"C:\Users\kylen\Desktop\AI\AI_pictures\spirit.png")
emf5_b64 = image_to_base64(r"C:\Users\kylen\Desktop\AI\AI_pictures\EMF5.png")
fingerprints_b64 = image_to_base64(r"C:\Users\kylen\Desktop\AI\AI_pictures\UV.png")
salt_b64 = image_to_base64(r"C:\Users\kylen\Desktop\AI\AI_pictures\salt.png")
freezing_b64 = image_to_base64(r"C:\Users\kylen\Desktop\AI\AI_pictures\freezing.png")
writing_b64 = image_to_base64(r"C:\Users\kylen\Desktop\AI\AI_pictures\writing.png")

# ========== 3) Model Setup for Google Generative AI ==========
# Replace the API key with a placeholder for security
genai.configure(api_key="YOUR_API_KEY_HERE")  
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_ai_content(prompt):
    """Generate content using the Gemini model based on the provided prompt."""
    response = model.generate_content(prompt)
    return response.text if response.text else "No content generated"

# ========== 4) Screen Capture Utility ==========
def capture_screen(monitor_index=2):
    """
    Capture screen from a specified monitor index using mss.
    Adjust monitor_index if your system has a different number of monitors.
    """
    with mss.mss() as sct:
        if monitor_index < 1 or monitor_index > len(sct.monitors):
            raise ValueError(f"Invalid monitor index: {monitor_index}. Available monitors: {len(sct.monitors) - 1}")
        monitor = sct.monitors[monitor_index]
        sct_img = sct.grab(monitor)
        return np.array(sct_img)

def process_image(image):
    """
    Preprocess the captured image by converting it to grayscale.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

# ========== 5) Sending Image to Gemini API ==========
def send_image_to_gemini(image):
    """
    Sends a base64-encoded image to the Gemini model using the 'generateContent' endpoint.
    """
    # Replace the API key placeholder
    api_key = "YOUR_API_KEY_HERE"
    
    # Encode image to base64
    _, img_encoded = cv2.imencode('.jpg', image)
    base64_image = base64.b64encode(img_encoded).decode('utf-8')

    # Define the prompt with reference images and instructions
    prompt_text = (
        """You are analyzing images from the game Phasmophobia to determine the ghost type.\n\n
Here is how we will do this:\n
- The FIRST FIVE images below are just REFERENCE images. They are NOT from the current game.\n
- The FINAL (sixth) image is the LIVE screenshot from the actual game.\n\n
Use the five reference images ONLY to understand what each piece of evidence should look like.\n
DO NOT treat the reference images as actual evidence in this current scenario.\n\n
Then, look at the FINAL image and identify any real evidence visible THERE.\n\n

1. **Spirit Box**: The white lights under the "RESPONSE" label are lit. That confirms Spirit Box activity.
2. **EMF 5**: The EMF reader shows ALL 5 bars lit (if it's only 2 bars, that is NOT EMF 5).
3. **UV Fingerprint**: A glowing green handprint OR footprint visible under UV light.
4. **Ghost Stepping in Salt**: If you see the ghost's footstep in salt, note that it CANNOT be a Wraith (Wraiths never step in salt).
5. **Freezing Temperatures**: A temperature reading below at negative C for example (-0.1°C) on the thermometer. (Visible cold breath by itself does NOT confirm freezing.)

Follow these rules carefully:
1. Only use evidence visibly confirmed in the provided image(s). Do not speculate or infer.
2. Glowing light green Fingerprints or Footprints must be visible under UV light.
3. Freezing Temperatures: Only confirmed if the thermometer reads below 0°C (ignore cold breath alone).
4. EMF Level 5: Only confirmed if all 5 bars are lit.
5. Spirit Box: Confirmed if the box's "RESPONSE" lights are visibly lit or you clearly see/hear a response on the screen or indicator.
6. Ghost Orb: Visible only if a floating orb appears on camera. This will not appear if we are not looking through a screen. Only indicate if you see this on a camera or a screen.
7. D.O.T.S Projector: Confirmed if a ghost silhouette or shape walks through the green dots.
8. Ghost Writing: Confirmed if the ghost has written/drawn in the book, Not if the book is blank.
9. It may take awhile to get evidence so do not rush at all. It is also impossible to get all 3 evidence from one image so take your time.

After identifying EXACTLY three pieces of evidence, match them to the ghost type. If fewer than three are visible or the combo doesn’t match a single ghost from the table, say “Cannot determine the ghost type from the visible evidence.”

Please produce a single, definitive answer. 
1. List ONLY the visible evidence from the final screenshot (1–3 items). 
2. If exactly 3, name the ghost from the table. 
3. If fewer than 3 or if the combo doesn’t match a single ghost, say “Cannot determine the ghost type from the visible evidence.” 
Do not give intermediate partial steps or contradictory statements. 

Evidence List:
- EMF Level 5
- Spirit Box
- Fingerprints
- Freezing Temperatures
- Ghost Orb
- Ghost Writing
- D.O.T.S Projector

Ghost Type Reference Table (3 evidence each):
- Spirit: EMF Level 5, Spirit Box, Ghost Writing
- Wraith: EMF Level 5, Spirit Box, D.O.T.S Projector
- Phantom: Spirit Box, Fingerprints, D.O.T.S Projector
- Poltergeist: Spirit Box, Fingerprints, Ghost Writing
- Banshee: Fingerprints, Ghost Orb, D.O.T.S Projector
- Jinn: EMF Level 5, Fingerprints, Freezing Temperatures
- Mare: Spirit Box, Ghost Orb, Ghost Writing
- Shade: EMF Level 5, Ghost Writing, Freezing Temperatures
- Demon: Fingerprints, Ghost Writing, Freezing Temperatures
- Yurei: Ghost Orb, Freezing Temperatures, D.O.T.S Projector
- Oni: EMF Level 5, Freezing Temperatures, D.O.T.S Projector
- Hantu: Fingerprints, Ghost Orb, Ghost Writing
- Yokai: Spirit Box, Ghost Orb, D.O.T.S Projector
- Goryo: EMF Level 5, Fingerprints, D.O.T.S Projector
- Myling: EMF Level 5, Fingerprints, Ghost Writing
- Onryo: Spirit Box, Ghost Orb, Freezing Temperatures
- The Twins: EMF Level 5, Spirit Box, Freezing Temperatures
- Raiju: EMF Level 5, Ghost Orb, D.O.T.S Projector
- Obake: EMF Level 5, Fingerprints, Ghost Orb
- The Mimic: Spirit Box, Fingerprints, Freezing Temperatures
- Revenant: Ghost Orb, Ghost Writing, Freezing Temperatures
- Moroi: Spirit Box, Ghost Writing, Freezing Temperatures
- Deogen: Spirit Box, Ghost Writing, D.O.T.S Projector
- Thaye: Ghost Orb, Ghost Writing, D.O.T.S Projector
"""

    )

    # Create the payload with prompt and reference images
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text},
                    # 1) Reference: Spirit Box
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": spirit_box_b64  # Reference image for Spirit Box
                        }
                    },
                    {"text": "ONLY USE AS Reference image for Spirit Box with lights on 'RESPONSE' when comparing to live screenshots."},
                    # 2) Reference: EMF 5
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": emf5_b64  # Reference image for EMF Level 5
                        }
                    },
                    {"text": "ONLY USE AS Reference image showing EMF 5 bars lit when comparing to live screenshots."},
                    # 3) Reference: Fingerprints
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": fingerprints_b64  # Reference image for Fingerprints
                        }
                    },
                    {"text": "ONLY USE AS Reference image of UV fingerprints (green handprint) when comparing to live screenshots."},
                    # 4) Reference: Salt Footstep
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": salt_b64  # Reference image for Salt Footsteps
                        }
                    },
                    {"text": "ONLY USE AS Reference image of ghost footsteps in salt (not a Wraith) when comparing to live screenshots."},
                    # 5) Reference: Freezing Temps
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": freezing_b64  # Reference image for Freezing Temperatures
                        }
                    },
                    {"text": "ONLY USE AS Reference image of thermometer < 1.0°C for freezing when comparing to live screenshots."},
                    # 6) Reference: Ghost Writing
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": writing_b64  # Reference image for Ghost Writing
                        }
                    },
                    {"text": "**FINAL IMAGE**: This is the real screenshot from the game. Only evidence shown here counts!"},
                    # 7) Live Screen Capture
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": base64_image  # Live screenshot from the game
                        }
                    },
                    {"text": "Here is the current live screenshot from the game."}
                ]
            }
        ]
    }

    # Define the API endpoint with the placeholder API key
    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-1.5-flash:generateContent"
        f"?key={api_key}"
    )
    headers = {"Content-Type": "application/json"}

    # Send POST request to Gemini API
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to send image. Status code: {response.status_code}, Response: {response.text}")
        return None

# ========== 6) Evidence Extraction and Ghost Matching ==========
found_evidence = []

def process_description(description):
    """
    Process the AI's text to find newly mentioned evidence.
    Then check if we have exactly 3 total evidence to match with the ghost database.
    """
    global found_evidence

    new_evidence = []
    evidence_terms = {
        "emf level 5": "EMF Level 5",
        "spirit box": "Spirit Box",
        "fingerprints": "Fingerprints",
        "freezing temperatures": "Freezing Temperatures",
        "ghost orb": "Ghost Orb",
        "ghost writing": "Ghost Writing",
        "d.o.t.s projector": "D.O.T.S Projector",
    }

    lower_desc = description.lower()
    for key, evidence_name in evidence_terms.items():
        if key in lower_desc:
            # Add evidence if not already found
            if evidence_name not in found_evidence:
                new_evidence.append(evidence_name)
                found_evidence.append(evidence_name)

    # Announce newly discovered evidence
    if new_evidence:
        for e in new_evidence:
            print(f"{e}!")
            speak_text(f"New evidence found: {e}")
    else:
        print("No New Evidence")

    # Display all found evidence
    print(f"Found Evidence: {found_evidence}")

    # Perform ghost matching if exactly 3 evidence pieces are found
    if len(found_evidence) == 3:
        possible_ghosts = match_ghost_to_evidence(found_evidence, ghosts)
        if len(possible_ghosts) == 1 and possible_ghosts[0] != "No matching ghost":
            ghost_name = possible_ghosts[0]
            print(f"The ghost is {ghost_name}!")
            speak_text(f"The ghost is {ghost_name}! Be careful.")
        else:
            print("Cannot determine the ghost type from the visible evidence.")
    elif len(found_evidence) < 3:
        print("Not enough evidence to determine the ghost.")
    else:
        # Handle cases with more than 3 evidence pieces
        print("We have more than 3 evidence, which is unusual. Possibly conflicting data.")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def speak_text(text):
    """Use text-to-speech to announce the provided text."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    """Main loop to continuously capture and process game screenshots."""
    while True:
        screen = capture_screen()
        processed_image = process_image(screen)
        result = send_image_to_gemini(processed_image)

        if result and "candidates" in result and len(result["candidates"]) > 0:
            description = result["candidates"][0]["content"]["parts"][0]["text"]
            print(f"Generated Description: {description}")
            process_description(description)
        else:
            print("No response or error from Gemini API.")

        time.sleep(4.5)  # Adjust the loop sleep time as needed

if __name__ == "__main__":
    main()
