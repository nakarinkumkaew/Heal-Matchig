import streamlit as st

# กำหนดชื่อของแอปพลิเคชัน
st.title("My Streamlit App")

# สร้างปุ่มแรก
if st.button('Button 1'):
    st.write('You clicked Button 1!')

# สร้างปุ่มที่สอง
if st.button('Button 2'):
    st.write('You clicked Button 2!')
