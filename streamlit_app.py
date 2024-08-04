import streamlit as st
from streamlit_drawable_canvas import st_canvas
import base64

# Function to set background image
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
        }}
        .stButton>button {{
            background-color: #B4D6CD;
            color: #333333;
            border: 2px solid #666666;
            border-radius: 12px;
            padding: 0.5em 1em;
            font-size: 1em;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #98c1a2;
            color: #ffffff;
            border-color: #333333;
        }}
        .stMarkdown {{
            color: #333333;
            font-family: 'Arial', sans-serif;
            font-size: 1.1em;
        }}
        .stTextInput>div>div>input {{
            background-color: #ffffff;
            border: 2px solid #666666;
            border-radius: 8px;
            padding: 0.5em;
            font-size: 1em;
        }}
        .stSlider>div {{
            color: #333333;
        }}
        .shift-down {{
            margin-top: 30px;  /* Adjust the value as needed for approximately 5 lines */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def toggle_drawing():
    st.session_state.draw_enabled = not st.session_state.draw_enabled

# Set the background image
set_background('back_ground.png', background_size="70% 100%")

# Initialize the draw_enabled state if not already set
if 'draw_enabled' not in st.session_state:
    st.session_state.draw_enabled = False

# Layout with two columns
col1, col2 = st.columns(2)
# Column 1 content
with col1:
    st.markdown('<div class="shift-down">ตอนนี้คุณเป็นอย่างไรบ้าง?</div>', unsafe_allow_html=True)
    if st.button('กำลังเหนื่อยอยู่ใช่มั๊ย', key='1-1'):
        st.write("Tried_1")
    if st.button('กำลังกังวลอยู่ใช่มั๊ย', key='1-2'):
        st.write("Tried_2")
    if st.button('ต้องการกำลังใจมั๊ย', key='1-3'):
        st.write("Tried_3")

# Column 2 content
with col2:
    st.markdown('<div class="shift-down">อยากรู้จักตัวเองมากขึ้นมั๊ย?</div>', unsafe_allow_html=True)
    if st.button('อยากรู้จุดเด่นของฉันจัง', key='3-1'):
        st.write("landmark")
    if st.button('ฉันมีความสามารถอะไรบ้าง?', key='3-2'):
        st.write("ability")
    if st.button('ฉันเหมาะกับอาชีพอะไร?', key='3-3'):
        st.write("job?")

# Drawing section
st.write("คุณมีอะไรอยากระบายมั๊ย?")
if st.button('ลองวาดออกมาดูสิ' if not st.session_state.draw_enabled else 'ฉันรู้สึกดีขึ้นแล้ว', key='draw-toggle', on_click=toggle_drawing):
    st.write("Drawing enabled" if st.session_state.draw_enabled else "Drawing disabled")

# Canvas for drawing
if st.session_state.draw_enabled:
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fill color with some opacity
        stroke_width=1,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        width=720,  # Adjusted width to remove the marked area
        drawing_mode="freedraw",
        key="canvas",
    )
