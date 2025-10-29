import streamlit as st
import os, json, shutil
from PIL import Image
import time  # Import time module for timestamping skipped images

USER_UPLOADS_DIR = "user_uploads"
USER_REAL_DIR = os.path.join(USER_UPLOADS_DIR, "user_real")
USER_AI_DIR = os.path.join(USER_UPLOADS_DIR, "user_ai")
USER_IMAGES_DIR = os.path.join(USER_UPLOADS_DIR, "user_images")

# Ensure dirs exist
for folder in [USER_UPLOADS_DIR, USER_REAL_DIR, USER_AI_DIR, USER_IMAGES_DIR]:
    os.makedirs(folder, exist_ok=True)

st.title("📂 Admin Review Panel")

# Check if a success message should be displayed
if "success_message" not in st.session_state:
    st.session_state.success_message = None

# Display the success message if it exists
if st.session_state.success_message:
    st.success(st.session_state.success_message)
    # Clear the message after displaying it
    st.session_state.success_message = None

files = [f for f in os.listdir(USER_IMAGES_DIR) if f.endswith(".jpg")]

if not files:
    st.info("No user-uploaded images to review.")
else:
    # Pick the first image for review
    filename = files[0]
    img_path = os.path.join(USER_IMAGES_DIR, filename)
    json_path = img_path.replace(".jpg", ".json")

    # Load image
    image = Image.open(img_path)
    st.image(image, caption=filename, use_container_width=True)

    # Load metadata
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            metadata = json.load(f)
        st.json(metadata)

    # Action buttons
    col1, col2, col3 = st.columns(3)  # Added a third column for the Skip button
    if col1.button("✅ Mark as REAL"):
        shutil.move(img_path, os.path.join(USER_REAL_DIR, filename))
        if os.path.exists(json_path):
            shutil.move(json_path, os.path.join(USER_REAL_DIR, os.path.basename(json_path)))
        st.session_state.success_message = "Moved to REAL folder."
        st.rerun()

    if col2.button("🤖 Mark as AI"):
        shutil.move(img_path, os.path.join(USER_AI_DIR, filename))
        if os.path.exists(json_path):
            shutil.move(json_path, os.path.join(USER_AI_DIR, os.path.basename(json_path)))
        st.session_state.success_message = "Moved to AI folder."
        st.rerun()

    if col3.button("⏭️ Skip"):
        # Move the current image to the end of the list by renaming it with a timestamp
        timestamp = int(time.time())
        new_filename = f"skipped_{timestamp}_{filename}"
        new_img_path = os.path.join(USER_IMAGES_DIR, new_filename)
        shutil.move(img_path, new_img_path)
        if os.path.exists(json_path):
            new_json_path = new_img_path.replace(".jpg", ".json")
            shutil.move(json_path, new_json_path)
        st.session_state.success_message = "Skipped to the next image."
        st.rerun()
