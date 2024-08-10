import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image,ImageDraw, ImageFont
import base64
import io
import os
import random

def get_random_image_path(folder_path):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    random_image_file = random.choice(image_files)
    return os.path.join(folder_path, random_image_file)

def save_img(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)  # ตั้งตำแหน่งของ pointer ที่จุดเริ่มต้น

    st.download_button(
        label="บันทึกรูปภาพ",
        data=buf.getvalue(),
        file_name="Image.png",
        mime="image/png"
    )

def go_to_page(page_name):
    st.session_state.current_page = page_name

def buttom_subpage():
    st.write("ถ้าคุณต้องการคนรับฟัง หรืออยากเล่าอะไร น้องยินดีรับฟังเสมอนะ")
    st.write("สามารถส่งข้อความ หรือติดตามผลงานของน้องยินดีได้ตามช่องทางนี้เลย")
    display_icon_with_link(".devcontainer/icon/facebook.png", 'The YouDee Project', "https://www.facebook.com/youdee.project")
    display_icon_with_link(".devcontainer/icon/ig.png", '@youdee.project', "https://www.instagram.com/youdee.project/")
    display_icon_with_link(".devcontainer/icon/web.png", 'The YouDee Project', "https://www.youdee.redcross.or.th/")
    if st.button("Go Back", on_click=go_to_page, args=("main",)):
        pass    

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
            margin-top: -20px; /* Move content up by 10px */
        }}
        .stSelectbox>div>div {{
            background-color: #B4D6CD;
            width: 70%;
            border: 2px solid #666666;
            border-radius: 12px;
            transition: all 0.3s ease;
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

       .stDownloadButton>button {{
            background-color: #B4D6CD;
            color: #333333;
            border: 2px solid #666666;
            border-radius: 12px;
            padding: 0.5em 1em;
            font-size: 1em;
            transition: all 0.3s ease;
        }}
        .stDownloadButton>button:hover {{
            background-color: #98c1a2;
            color: #ffffff;
            border-color: #333333;
        }}

        .shift-down {{
            margin-top: 10px; 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def find_key_by_value(groups, item):
    for key, sub_dict in groups.items():
        for sub_key, sub_list in sub_dict.items():
            if item in sub_list:
                return key
    return None


set_background('.devcontainer/back_ground.png', background_size="100% 100%")

LABEL_MAP = {
    0: 'Angry',
    1: 'Fearful',
    2: 'Happy',
    3:  'Neutral',
    4: 'Sad'
}



if 'draw_enabled' not in st.session_state:
    st.session_state.draw_enabled = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

if st.session_state.current_page == "main":
    st.title("คุณต้องการอะไรบอกน้องยินดีได้เลยนะ")
    if st.button('กำลังใจจากน้องยินดี', key='0-1', on_click=go_to_page, args=("inspire",)):
        pass

    if st.button('อยากรู้จักตัวเองมากขึ้นมั๊ย', key='0-3', on_click=go_to_page, args=("yourself",)):
        pass

    if st.button('น้องยินดีชวนระบายความรู้สึก', key='0-4', on_click=go_to_page, args=("feel",)):
        pass


elif st.session_state.current_page == "inspire":
    st.title("ตอนนี้คุณเป็นอย่างไรบ้าง")
    if st.button('กำลังเหนื่อยอยู่ใช่มั๊ย', key='1-1', on_click=go_to_page, args=("tried",)):
        pass
    if st.button('กำลังกังวลอยู่ใช่มั๊ย', key='1-2', on_click=go_to_page, args=("confuse",)):
        pass
    if st.button('ต้องการกำลังใจมั๊ย', key='1-3', on_click=go_to_page, args=("value",)):
        pass
    if st.button("Go Back", on_click=go_to_page, args=("main",)):
        pass

elif st.session_state.current_page == "yourself":
    st.title("อยากรู้จักตัวเองในด้านไหน?")
    if st.button('อยากรู้จุดเด่นของฉันจัง', key='3-1', on_click=go_to_page, args=("landmark",)):
        st.write("landmark")
    if st.button('ฉันมีความสามารถอะไรบ้าง?', key='3-2', on_click=go_to_page, args=("ability",)):
        st.write("ability")
    if st.button('ฉันเหมาะกับอาชีพอะไร?', key='3-3', on_click=go_to_page, args=("job",)):
        st.write("job")
    if st.button("Go Back", on_click=go_to_page, args=("main",)):
        pass

elif st.session_state.current_page == "feel":
    st.title("คุณมีอะไรอยากระบายมั๊ย?")

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
    if st.button("Go Back", on_click=go_to_page, args=("main",)):
        pass

elif st.session_state.current_page in ("tried", "confuse", "value"):
    image_path = get_random_image_path(".devcontainer/card/" + st.session_state.current_page)
    image = Image.open(image_path)
    st.markdown('<div class="shift-down">สามารถบันทึกรูปภาพ เพื่อแชร์ให้คนสำคัญของเพื่อนๆ และให้กำลังใจตัวเองได้นะ</div>', unsafe_allow_html=True)
    st.image(image)
    save_img(image)
    buttom_subpage()

elif st.session_state.current_page == "landmark":
    st.title("จุดเด่นของคุณคืออะไรกันแน่นะ?")
    advice_dict = {
        "ความรักและความสัมพันธ์": 
            "- สามารถฟังปัญหาของเพื่อนอย่างละเอียดและไม่ตัดสิน\n"
            "- มีความเข้าใจในอารมณ์และความรู้สึกของผู้อื่น\n"
        ,
        "การเรียนและการทำงาน": (
            "- ทักษะในการวางแผนและจัดการเวลา\n"
            "- ความรู้และประสบการณ์ในเรื่องที่เพื่อนต้องการคำแนะนำ\n"
            "- สามารถให้กำลังใจและแรงบันดาลใจให้กับเพื่อนได้\n"
        ),
        "ครอบครัว": (
            "- ความเข้าใจในปัญหาครอบครัว\n"
            "- สามารถสื่อสารและเจรจาให้คำแนะนำที่เหมาะสมได้\n"
            "- ความอ่อนโยนและเห็นอกเห็นใจผู้อื่น\n"
        ),
        "สุขภาพจิตและอารมณ์": (
            "- สามารถฟังและเข้าใจความรู้สึกของผู้อื่นได้ดี\n"
            "- ความรู้พื้นฐานด้านจิตวิทยา\n"
            "- ความเข้าใจและเห็นอกเห็นใจ\n"
        ),
        "การเงิน": (
            "- ทักษะในการวางแผนการเงินและการจัดการทรัพย์สิน\n"
            "- ความรู้ด้านการเงินและการลงทุน\n"
        ),
        "การตัดสินใจสำคัญ": (
            "- ทักษะในการวิเคราะห์และประเมินสถานการณ์\n"
            "- สามารถให้คำแนะนำที่มีเหตุผลและมีความเป็นไปได้\n"
        )
    }


    selected_category = st.selectbox(
    "ฉันให้คำปรึกษากับคนอื่นเรื่องอะไรได้มากที่สุด?",
    options=list(advice_dict.keys())
    )

    if st.button('เปิดดูจุดเด่นของฉัน'):
        if selected_category:
            image = Image.open(".devcontainer/yourself/landmark.png")
            draw = ImageDraw.Draw(image)
            text = "คุณสามารถแก้ปัญหาเรื่อง :"+selected_category+"\n\nสิ่งที่เป็นจุดเด่นของคุณคือ""\n" +advice_dict[selected_category]
            position = (70, 100)
            font = ImageFont.truetype(".devcontainer/font/angsana.ttc", 40)
            draw.text(position, text, font=font, fill="black")
            st.image(image, use_column_width=True)
            save_img(image)
        else:
            st.warning("Please select an option before submitting.")

    buttom_subpage()

elif st.session_state.current_page == "ability":
    st.title("Styled Dropdown Example")
    groups = {
        "การช่วยเหลือและการมีส่วนร่วมในสังคม": {
            "passion": ["การทำงานอาสาสมัคร", "การร่วมกิจกรรมสังคม", "การสนับสนุนสิ่งแวดล้อม"],
            "do": ["เข้าร่วมโครงการอาสาสมัคร", "ทำกิจกรรมเพื่อสังคม", "เข้าร่วมงานกิจกรรมในชุมชน", "ช่วยเหลือในการจัดงาน", "ร่วมกิจกรรมอนุรักษ์สิ่งแวดล้อม", "ส่งเสริมการใช้ชีวิตอย่างยั่งยืน"]
        },
        "การสร้างสรรค์และศิลปะ": {
            "passion": ["การวาดภาพและการปั้น", "การเขียนและการประพันธ์", "การออกแบบ", "การถ่ายภาพ"],
            "do": ["ลงเรียนคอร์สศิลปะ", "ร่วมกิจกรรมศิลปะในชุมชน", "เปิดสตูดิโอสร้างสรรค์ของตัวเอง", "เขียนบล็อก", "เข้าร่วมกลุ่มนักเขียน", "ส่งผลงานเข้าประกวด", "เรียนรู้การออกแบบกราฟิกออนไลน์", "ออกแบบผลิตภัณฑ์และขายบนแพลตฟอร์มออนไลน์", "ฝึกถ่ายภาพด้วยการเข้าร่วมเวิร์กช็อป", "สร้างพอร์ตโฟลิโอ", "แชร์ผลงานบนโซเชียลมีเดีย"]
        },
        "การเรียนรู้และการศึกษา": {
            "passion": ["การศึกษาวิชาการ", "การเรียนรู้ภาษา", "การค้นคว้าและวิจัย"],
            "do": ["อ่านหนังสือและเข้าร่วมการสัมมนา", "เรียนออนไลน์ผ่านแพลตฟอร์มต่างๆ", "เรียนภาษาผ่านแอปพลิเคชัน", "เข้าร่วมกลุ่มสนทนาภาษา", "ทำวิจัยในหัวข้อที่สนใจ", "นำเสนอผลงานวิจัยในที่ประชุม"]
        },
        "การกีฬาและการออกกำลังกาย": {
            "passion": ["การเล่นกีฬา", "การออกกำลังกาย", "การผจญภัยกลางแจ้ง"],
            "do": ["เข้าร่วมทีมกีฬาท้องถิ่น", "แข่งขันกีฬาในระดับสมัครเล่น", "เข้าฟิตเนส", "ฝึกโยคะ", "วิ่งมาราธอน", "เดินป่า", "ปีนเขา", "ดำน้ำลึก"]
        },
        "การทำอาหารและเครื่องดื่ม": {
            "passion": ["การทำอาหาร", "การทำขนมและเบเกอรี่", "การชงเครื่องดื่ม"],
            "do": ["เรียนทำอาหาร", "เปิดร้านอาหารของตัวเอง", "แชร์สูตรอาหารออนไลน์", "ขายขนมโฮมเมด", "เปิดร้านเบเกอรี่", "เรียนรู้การชงเครื่องดื่ม", "เปิดคาเฟ่"]
        },
        "การดูแลสุขภาพและความงาม": {
            "passion": ["การดูแลผิวพรรณและเส้นผม", "การออกกำลังกายเพื่อสุขภาพ", "การทานอาหารเพื่อสุขภาพ"],
            "do": ["ลงเรียนคอร์สดูแลผิวพรรณและเส้นผม", "ให้คำปรึกษาด้านความงาม", "เข้าร่วมกลุ่มออกกำลังกาย", "สอนคลาสออกกำลังกาย", "ทำอาหารเพื่อสุขภาพ", "เขียนบล็อกเกี่ยวกับโภชนาการ"]
        },
        "การท่องเที่ยวและการผจญภัย": {
            "passion": ["การท่องเที่ยวต่างประเทศ", "การเดินทางในประเทศ", "การผจญภัยและการสำรวจ"],
            "do": ["วางแผนการเดินทาง", "เขียนบล็อกท่องเที่ยว", "สำรวจสถานที่ท่องเที่ยวในประเทศ", "แบ่งปันประสบการณ์การเดินทาง", "เดินป่า", "สำรวจธรรมชาติ", "บันทึกประสบการณ์การผจญภัย"]
        },
        "การทำงานและอาชีพ": {
            "passion": ["การพัฒนาทักษะและความรู้", "การเป็นผู้ประกอบการ", "การสร้างเครือข่าย"],
            "do": ["เข้าร่วมคอร์สเรียนและการสัมมนา", "อ่านหนังสือและวารสารในสาขาอาชีพของตน", "เริ่มต้นธุรกิจ", "เรียนรู้การบริหารจัดการธุรกิจ", "เข้าร่วมงานประชุมและกิจกรรมทางธุรกิจ", "ใช้โซเชียลมีเดียในการสร้างเครือข่าย"]
        }
    }

   # Extract all passions and dos
    options_passion = []
    options_do = []

    for group in groups.values():
        options_passion.extend(group["passion"])
        options_do.extend(group["do"])

    # Remove duplicates by converting to set and back to list
    options_passion = list(set(options_passion))
    options_do = list(set(options_do))

    # Sort options for better UX
    options_passion.sort()
    options_do.sort()

    selected_option_passion = st.selectbox("สิ่งที่ฉันทำแล้วมีความสุข:", options_passion)
    selected_option_do = st.selectbox("สิ่งที่ฉันทำได้ดี:", options_do)

    def check_match(option_passion, option_do):
        for group in groups.values():
            if option_passion in group["passion"] and option_do in group["do"]:
                return "match"
        return "not match"

    if st.button('เปิดดูความสามารถของฉัน'):
        image = Image.open(".devcontainer/yourself/ability.png")
        draw = ImageDraw.Draw(image)
        if check_match(selected_option_passion, selected_option_do) == "match":
            text = "ดีใจด้วยนะ คุณได้ทำในสิ่งที่รัก!!!\n\nคุณมีความสามารถ และคุณมีความหลงไหลในเรื่อง : "+find_key_by_value(groups, selected_option_do)
        else:
            text = "คุณมีความสามารถ : "+find_key_by_value(groups, selected_option_do)+"\n\nแต่คุณมีความหลงไหลในเรื่อง : "+find_key_by_value(groups, selected_option_passion)+"\n\nน้องยินดีขอให้คุณได้ทำในสิ่งที่รักนะ!"
        position = (100, 600)
        font = ImageFont.truetype(".devcontainer/font/angsana.ttc", 40)
        draw.text(position, text, font=font, fill="black")
        st.image(image, use_column_width=True)
        save_img(image)
    buttom_subpage()

elif st.session_state.current_page == "job":
    st.title("Styled Dropdown Example")
    activities_dict = {
        "วาดภาพและปั้นดินเผา": {
            "skill": ["พัฒนาทักษะการมองเห็นและการประสานมือ-ตา", "ความคิดสร้างสรรค์", "การแสดงออกทางศิลปะ"],
            "job": ["ศิลปิน", "นักวาดภาพ", "นักปั้น"]
        },
        "เขียนหนังสือหรือบทกวี": {
            "skill": ["พัฒนาทักษะการเขียน", "การคิดวิเคราะห์", "การแสดงออกทางความคิด"],
            "job": ["นักเขียน", "นักประพันธ์", "บรรณาธิการ"]
        },
        "ถ่ายภาพและตกแต่งภาพ": {
            "skill": ["พัฒนาทักษะการมองเห็น", "การใช้เทคโนโลยีการถ่ายภาพ", "การตกแต่งภาพดิจิทัล"],
            "job": ["ช่างภาพ", "นักตกแต่งภาพ", "ผู้สร้างสรรค์เนื้อหาดิจิทัล"]
        },
        "เล่นดนตรีหรือร้องเพลง": {
            "skill": ["พัฒนาทักษะการฟัง", "การประสานมือ-ตา", "การแสดงออกทางอารมณ์"],
            "job": ["นักดนตรี", "นักร้อง", "ครูสอนดนตรี"]
        },
        "งานฝีมือ": {
            "skill": ["พัฒนาทักษะการมองเห็น", "การประสานมือ-ตา", "ความคิดสร้างสรรค์"],
            "job": ["ช่างฝีมือ", "นักออกแบบผลิตภัณฑ์แฮนด์เมด", "ครูสอนศิลปะ"]
        },
        "ออกกำลังกายในยิมหรือฟิตเนส": {
            "skill": ["พัฒนาทักษะความแข็งแรง", "ความยืดหยุ่น", "การออกกำลังกายอย่างมีระบบ"],
            "job": ["เทรนเนอร์ฟิตเนส", "โค้ชส่วนตัว"]
        },
        "เล่นกีฬาต่างๆ": {
            "skill": ["พัฒนาทักษะการประสานมือ-ตา", "ความแข็งแรง", "การทำงานเป็นทีม"],
            "job": ["นักกีฬาอาชีพ", "โค้ชกีฬา", "นักวิเคราะห์กีฬาหรือนักพากย์กีฬา"]
        },
        "วิ่งหรือปั่นจักรยาน": {
            "skill": ["พัฒนาทักษะความแข็งแรง", "ความอดทน", "การวางแผนเส้นทาง"],
            "job": ["นักกีฬาอาชีพ", "โค้ช", "นักจัดการกิจกรรมกีฬาหรือทัวร์"]
        },
        "โยคะและการทำสมาธิ": {
            "skill": ["พัฒนาทักษะความยืดหยุ่น", "การผ่อนคลายจิตใจ", "การควบคุมลมหายใจ"],
            "job": ["ครูสอนโยคะ", "ครูสอนสมาธิ"]
        },
        "กิจกรรมกลางแจ้ง": {
            "skill": ["พัฒนาทักษะความแข็งแรง", "การวางแผน", "การเอาตัวรอด"],
            "job": ["ไกด์นำเที่ยว", "ครูสอนปีนเขา", "ผู้จัดกิจกรรมกลางแจ้ง"]
        },
        "อ่านหนังสือและนิตยสาร": {
            "skill": ["พัฒนาทักษะการอ่าน", "การคิดวิเคราะห์", "การเรียนรู้ต่อเนื่อง"],
            "job": ["นักเขียน", "นักวิจารณ์หนังสือ", "บรรณาธิการ"]
        },
        "เรียนออนไลน์หรือเรียนคอร์สใหม่ๆ": {
            "skill": ["พัฒนาทักษะความรู้ในด้านใหม่", "การจัดการเวลา", "การคิดวิเคราะห์"],
            "job": ["ผู้สอนออนไลน์", "ผู้สร้างเนื้อหาการศึกษา", "ที่ปรึกษาการเรียน"]
        },
        "ศึกษาภาษาใหม่ๆ": {
            "skill": ["พัฒนาทักษะการสื่อสาร", "ความคิดวิเคราะห์", "การเชื่อมโยงวัฒนธรรม"],
            "job": ["ครูสอนภาษา", "ล่าม", "นักแปล"]
        },
        "เล่นเกมพัฒนาทักษะ": {
            "skill": ["พัฒนาทักษะการคิดวิเคราะห์", "การแก้ปัญหา", "การวางแผนกลยุทธ์"],
            "job": ["นักพัฒนาเกม", "ครูสอนเกม", "นักวิจารณ์เกม"]
        },
        "เข้าร่วมเวิร์กช็อปและการสัมมนา": {
            "skill": ["พัฒนาทักษะการเรียนรู้ต่อเนื่อง", "การสร้างเครือข่าย", "การนำเสนอ"],
            "job": ["วิทยากร", "ผู้จัดงานสัมมนา", "ที่ปรึกษา"]
        },
        "สังสรรค์กับเพื่อนและครอบครัว": {
            "skill": ["พัฒนาทักษะการสื่อสาร", "การสร้างความสัมพันธ์", "การทำงานเป็นทีม"],
            "job": ["ผู้จัดงานอีเวนต์", "ผู้ให้คำปรึกษาเรื่องความสัมพันธ์"]
        },
        "เข้าร่วมกิจกรรมอาสาสมัคร": {
            "skill": ["พัฒนาทักษะการทำงานร่วมกัน", "ความเห็นอกเห็นใจ", "การจัดการโครงการ"],
            "job": ["ผู้จัดการองค์กรการกุศล", "ผู้ให้คำปรึกษาชุมชน", "นักสังคมสงเคราะห์"]
        },
        "เข้าร่วมงานสังคมหรือปาร์ตี้": {
            "skill": ["พัฒนาทักษะการสื่อสาร", "การสร้างเครือข่าย", "การจัดการเวลา"],
            "job": ["ผู้จัดงานอีเวนต์", "พิธีกร", "นักจัดรายการวิทยุ"]
        },
        "การเข้าร่วมคลับหรือกลุ่มที่มีความสนใจร่วมกัน": {
            "skill": ["พัฒนาทักษะการสร้างเครือข่าย", "การแลกเปลี่ยนความรู้", "การทำงานเป็นทีม"],
            "job": ["ผู้บริหารชมรม", "ผู้ประสานงานกลุ่มความสนใจ"]
        },
        "การเยี่ยมเยียนและช่วยเหลือคนในชุมชน": {
            "skill": ["พัฒนาทักษะความเห็นอกเห็นใจ", "การทำงานร่วมกัน", "การสื่อสาร"],
            "job": ["นักสังคมสงเคราะห์", "ผู้ให้คำปรึกษาชุมชน"]
        },
        "การทำสปาหรือการดูแลผิวพรรณ": {
            "skill": ["พัฒนาทักษะการดูแลตนเอง", "การผ่อนคลาย", "การใช้ผลิตภัณฑ์"],
            "job": ["ผู้เชี่ยวชาญด้านความงาม", "เจ้าของสปา", "ผู้ให้คำปรึกษาด้านความงาม"]
        },
        "การนวดและการทำทรีตเมนต์เพื่อสุขภาพ": {
            "skill": ["พัฒนาทักษะการดูแลตนเอง", "การผ่อนคลาย", "การใช้ผลิตภัณฑ์"],
            "job": ["นักนวดบำบัด", "ผู้เชี่ยวชาญด้านการรักษาสุขภาพ"]
        },
        "การทำอาหารเพื่อสุขภาพ": {
            "skill": ["พัฒนาทักษะการทำอาหาร", "การวางแผนโภชนาการ", "การใช้วัตถุดิบอย่างมีประสิทธิภาพ"],
            "job": ["เชฟ", "นักโภชนาการ", "ผู้สร้างเนื้อหาด้านอาหารและสุขภาพ"]
        },
        "การดูแลเส้นผมและแต่งหน้า": {
            "skill": ["พัฒนาทักษะการดูแลตนเอง", "การใช้ผลิตภัณฑ์", "การแสดงออกทางความงาม"],
            "job": ["ช่างแต่งหน้า", "ช่างทำผม", "ผู้ให้คำปรึกษาด้านความงาม"]
        },
        "การทำสมาธิและการพักผ่อน": {
            "skill": ["พัฒนาทักษะการผ่อนคลายจิตใจ", "การควบคุมลมหายใจ", "การมีสมาธิ"],
            "job": ["ครูสอนสมาธิ", "ผู้ให้คำปรึกษาด้านสุขภาพจิต"]
        },
        "ดูหนังและซีรีส์": {
            "skill": ["พัฒนาทักษะการฟังและการเข้าใจเรื่องราว", "การผ่อนคลาย", "การวิเคราะห์เรื่องราว"],
            "job": ["นักวิจารณ์ภาพยนตร์", "ผู้เขียนบทภาพยนตร์", "ผู้ผลิตเนื้อหาวิดีโอ"]
        },
        "ฟังเพลงและดูคอนเสิร์ต": {
            "skill": ["พัฒนาทักษะการฟัง", "การแสดงออกทางอารมณ์", "การผ่อนคลาย"],
            "job": ["นักดนตรี", "นักวิจารณ์เพลง", "ผู้จัดการคอนเสิร์ต"]
        },
        "เล่นเกมวิดีโอหรือเกมบอร์ด": {
            "skill": ["พัฒนาทักษะการคิดวิเคราะห์", "การแก้ปัญหา", "การทำงานเป็นทีม"],
            "job": ["นักพัฒนาเกม", "นักกีฬาอีสปอร์ต", "ผู้จัดการแข่งขันเกม"]
        },
        "การท่องเที่ยวและสำรวจสถานที่ใหม่ๆ": {
            "skill": ["พัฒนาทักษะการวางแผน", "การปรับตัว", "การเรียนรู้วัฒนธรรมใหม่"],
            "job": ["ไกด์นำเที่ยว", "นักเขียนท่องเที่ยว", "ผู้จัดการทัวร์"]
        },
        "ช้อปปิ้งและการเข้าชมงานแสดงสินค้าต่างๆ": {
            "skill": ["พัฒนาทักษะการวางแผน", "การจัดการเงิน", "การค้นหาสินค้าที่มีคุณค่า"],
            "job": ["นักจัดหาสินค้า", "ผู้จัดงานแสดงสินค้า"]
        },
        "การเขียนโปรแกรมหรือการทำโครงงานเทคโนโลยี": {
            "skill": ["พัฒนาทักษะการเขียนโปรแกรม", "การแก้ปัญหา", "การคิดเชิงตรรกะ"],
            "job": ["นักพัฒนาซอฟต์แวร์", "นักวิจัย", "วิศวกร"]
        },
        "การสร้างโมเดลหรือการประกอบของเล่น": {
            "skill": ["พัฒนาทักษะการมองเห็น", "การประสานมือ-ตา", "การสร้างสรรค์"],
            "job": ["นักออกแบบผลิตภัณฑ์", "วิศวกร", "ช่างฝีมือ"]
        },
        "การศึกษาและทดลองวิทยาศาสตร์": {
            "skill": ["พัฒนาทักษะการคิดวิเคราะห์", "การวิจัย", "การทดลอง"],
            "job": ["นักวิจัย", "นักวิทยาศาสตร์", "อาจารย์มหาวิทยาลัย"]
        },
        "การทำบล็อกหรือสร้างเนื้อหาดิจิทัล": {
            "skill": ["พัฒนาทักษะการเขียน", "การสื่อสาร", "การสร้างเนื้อหา"],
            "job": ["บล็อกเกอร์", "นักเขียนเนื้อหา", "ผู้ผลิตวิดีโอ"]
        },
        "การสำรวจและศึกษาดาวเทียมและอวกาศ": {
            "skill": ["พัฒนาทักษะการวิจัย", "การวิเคราะห์ข้อมูล", "การเรียนรู้วิทยาศาสตร์"],
            "job": ["นักวิจัยด้านอวกาศ", "วิศวกรอวกาศ", "นักดาราศาสตร์"]
        }
    }
    dropdown_options = list(activities_dict.keys())
    selected_category = st.selectbox("กิจกรรมยามว่างที่ฉันชอบทำคือ", dropdown_options)

    if st.button('เปิดดูอาชีพที่เหมาะกับฉัน'):
        if selected_category:
            image = Image.open(".devcontainer/yourself/job.png")
            draw = ImageDraw.Draw(image)
            text = "ทักษะที่คุณได้จากกิจกรรมคือ :\n- "+"\n- ".join(activities_dict[selected_category]["skill"])+"\n\nอาชีพที่เหมาะกับคุณคือ :""\n" +", ".join(activities_dict[selected_category]["job"])
            position = (100, 600)
            font = ImageFont.truetype(".devcontainer/font/angsana.ttc", 40)
            draw.text(position, text, font=font, fill="black")
            st.image(image, use_column_width=True)
            save_img(image)
        else:
            st.warning("Please select an option before submitting.")
    buttom_subpage()
