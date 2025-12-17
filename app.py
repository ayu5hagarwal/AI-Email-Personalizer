import streamlit as st
from main import generate_email

st.title("AI Email Personalizer")

person_info = st.text_area("Person's LinkedIn bio/info:")
your_product = st.text_area("Your product/service:")
goal = st.text_input("Your goal:")

if st.button("Generate Email"):
    if person_info and your_product and goal:
        email = generate_email(person_info, your_product, goal)
        st.success("Generated Email:")
        st.text_area("Copy this:", email, height=200)
    else:
        st.error("Please fill all fields")