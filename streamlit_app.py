import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import base64
import io
import os
import random

def get_random_image_path(folder_path):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    random_image_file = random.choice(image_files)
    return os.path.join(folder_path, random_image_file)

def go_to_page(page_name):
    st.session_state.current_page = page_name

def toggle_drawing():
    st.session_state.draw_enabled = not st.session_state.draw_enabled

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
            padding-left: 20%;
            padding-left: -10px;
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
            margin-top: 10px; 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background('.devcontainer/back_ground.png', background_size="100% 100%")

if 'draw_enabled' not in st.session_state:
    st.session_state.draw_enabled = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

if st.session_state.current_page == "main":
    st.write("ตอนนี้คุณเป็นอย่างไรบ้าง?")
    if st.button('กำลังเหนื่อยอยู่ใช่มั๊ย', key='1-1', on_click=go_to_page, args=("tried",)):
        pass
    if st.button('กำลังกังวลอยู่ใช่มั๊ย', key='1-2', on_click=go_to_page, args=("confuse",)):
        pass
    if st.button('ต้องการกำลังใจมั๊ย', key='1-3', on_click=go_to_page, args=("value",)):
        pass

    st.write("อยากรู้จักตัวเองมากขึ้นมั๊ย?")
    if st.button('อยากรู้จุดเด่นของฉันจัง', key='3-1'):
        st.write("landmark")
    if st.button('ฉันมีความสามารถอะไรบ้าง?', key='3-2'):
        st.write("ability")
    if st.button('ฉันเหมาะกับอาชีพอะไร?', key='3-3'):
        st.write("job?")

    st.write("คุณมีอะไรอยากระบายมั๊ย?")
    if st.button('ลองวาดออกมาดูสิ' if not st.session_state.draw_enabled else 'ฉันรู้สึกดีขึ้นแล้ว', key='draw-toggle', on_click=toggle_drawing):
        st.write("Drawing enabled" if st.session_state.draw_enabled else "Drawing disabled")

    if st.session_state.draw_enabled:
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
                label="เก็บไว้เป็นที่ระลึกได้นะ",
                data=byte_im,
                file_name="drawing.png",
            )

elif st.session_state.current_page in ("tried", "confuse", "value"):
    image_path = get_random_image_path(".devcontainer/card/" + st.session_state.current_page)
    image = Image.open(image_path)
    st.markdown('<div class="shift-down">สามารถบันทึกรูปภาพ เพื่อแชร์ให้คนสำคัญของเพื่อนๆ และให้กำลังใจตัวเองได้นะ</div>', unsafe_allow_html=True)
    st.image(image)
    st.write("ถ้าเพื่อนต้องการคนรับฟัง หรืออยากเล่าอะไร น้องยินดีรับฟังเสมอนะ")
    st.write("สามารถส่งข้อความ หรือติดตามผลงานของน้องยินดีได้ตามช่องทางนี้เลย")
    display_icon_with_link(".devcontainer/icon/facebook.png", 'The YouDee Project', "https://www.facebook.com/youdee.project")
    display_icon_with_link(".devcontainer/icon/ig.png", '@youdee.project', "https://www.instagram.com/youdee.project/")
    display_icon_with_link(".devcontainer/icon/web.png", 'The YouDee Project', "https://www.youdee.redcross.or.th/")
    if st.button("Go Back", on_click=go_to_page, args=("main",)):
        pass

elif st.session_state.current_page == "landmark":
    st.write("ถ้าเพื่อนต้องการคนรับฟัง หรืออยากเล่าอะไร น้องยินดีรับฟังเสมอนะ")
    st.write("สามารถส่งข้อความ หรือติดตามผลงานของน้องยินดีได้ตามช่องทางนี้เลย")
    display_icon_with_link(".devcontainer/icon/facebook.png", 'The YouDee Project', "https://www.facebook.com/youdee.project")
    display_icon_with_link(".devcontainer/icon/ig.png", '@youdee.project', "https://www.instagram.com/youdee.project/")
    display_icon_with_link(".devcontainer/icon/web.png", 'The YouDee Project', "https://www.youdee.redcross.or.th/")
    if st.button("Go Back", on_click=go_to_page, args=("main",)):
        pass
