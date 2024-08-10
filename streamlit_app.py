import streamlit as st
from streamlit_drawable_canvas import st_canvas
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
from io import BytesIO
import base64
import io
import os
import random

# Function to get a random image from a folder
def get_random_image_path(folder_path):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    random_image_file = random.choice(image_files)
    return os.path.join(folder_path, random_image_file)

# Function to save image and provide a download button
def save_img(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    st.download_button(
        label="บันทึกรูปภาพ",
        data=buf.getvalue(),
        file_name="Image.png",
        mime="image/png"
    )

# Function to navigate between pages
def go_to_page(page_name):
    st.session_state.current_page = page_name

# Function to display social media buttons
def display_icon_with_link(icon_path, content, url):
    with open(icon_path, "rb") as icon_file:
        icon_encoded = base64.b64encode(icon_file.read()).decode()
    icon_and_content_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <a href="{url}" target="_blank">
            <img src="data:image/png;base64,{icon_encoded}" style="height: 30px; margin-right: 10px;">
        </a>
        <span style="font-size: 1em; color: #333333;">{content}</span>
    </div>
    """
    st.markdown(icon_and_content_html, unsafe_allow_html=True)

# Function to set the background of the app
def set_background(image_file, background_size="cover"):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: {background_size};
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center center;
            background-color: #B4D6CD;
            padding: 5%;
            margin-top: -20px; 
        }}
        .stButton>button, .stDownloadButton>button {{
            background-color: #B4D6CD;
            color: #333333;
            border: 2px solid #666666;
            border-radius: 12px;
            padding: 0.5em 1em;
            font-size: 1em;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover, .stDownloadButton>button:hover {{
            background-color: #98c1a2;
            color: #ffffff;
            border-color: #333333;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background
set_background('.devcontainer/back_ground.png', background_size="100% 100%")

# Initialize session state variables
if 'draw_enabled' not in st.session_state:
    st.session_state.draw_enabled = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

# Main page layout
if st.session_state.current_page == "main":
    st.header("เลือกหัวข้อที่สนใจ")
    if st.button('กำลังใจจากน้องยินดี'):
        go_to_page("inspire")
    if st.button('น้องยินดีขอเดาอารมณ์ของคุณ'):
        go_to_page("photo")
    if st.button('อยากรู้จักตัวเองมากขึ้นมั๊ย'):
        go_to_page("yourself")
    if st.button('น้องยินดีชวนระบายความรู้สึก'):
        go_to_page("feel")

# Page: Inspire
elif st.session_state.current_page == "inspire":
    st.header("ตอนนี้คุณเป็นอย่างไรบ้าง")
    if st.button('กำลังเหนื่อยอยู่ใช่มั๊ย'):
        go_to_page("tried")
    if st.button('กำลังกังวลอยู่ใช่มั๊ย'):
        go_to_page("confuse")
    if st.button('ต้องการกำลังใจมั๊ย'):
        go_to_page("value")
    if st.button("Go Back"):
        go_to_page("main")

# Page: Yourself
elif st.session_state.current_page == "yourself":
    st.header("อยากรู้จักตัวเองในด้านไหน?")
    if st.button('อยากรู้จุดเด่นของฉันจัง'):
        st.write("landmark")
    if st.button('ฉันมีความสามารถอะไรบ้าง?'):
        st.write("ability")
    if st.button('ฉันเหมาะกับอาชีพอะไร?'):
        st.write("job")
    if st.button("Go Back"):
        go_to_page("main")

# Page: Photo (Emotion detection)
elif st.session_state.current_page == "photo":
    st.header("น้องยินดีขอเดาอารมณ์ของคุณ")

    # Load the YOLO model
    model = YOLO('.devcontainer/model/best_m_size.pt')

    # Ensure session state for last detected image is initialized
    if 'last_detected_image' not in st.session_state:
        st.session_state.last_detected_image = None

    class YOLOVideoTransformer(VideoTransformerBase):
        def __init__(self):
            self.model = model

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            results = self.model(img)[0]

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = results.names[int(box.cls)]
                confidence = float(box.conf)
                color = LABEL_COLOR_MAP.get(label, (0, 255, 0))
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f'{label} ({confidence:.2f})',
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            st.session_state.last_detected_image = img
            return img

    # Start webcam for emotion detection
    ctx = webrtc_streamer(key="example", video_transformer_factory=YOLOVideoTransformer)

    # Display detected image and download button if available
    if st.session_state.last_detected_image is not None:
        st.image(st.session_state.last_detected_image, channels="BGR")
        save_img(Image.fromarray(cv2.cvtColor(st.session_state.last_detected_image, cv2.COLOR_BGR2RGB)))

    if st.button("Go Back"):
        go_to_page("main")

# Page: Feel (Drawing)
elif st.session_state.current_page == "feel":
    st.header("คุณมีอะไรอยากระบายมั๊ย?")

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        width=300,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
