import streamlit as st
from PIL import Image
import numpy as np
import os
from UE_code.enhance import enhance_my
import time


st.set_page_config(page_title="Underwater Image Enhancer", page_icon=":guardsman:", layout="wide")
st.title("Underwater Image Enhancer")
# Define the options for the selection bar
options = ['MyModel', 'UDCP', 'GCDP', 'UWCNN','Ucolor']

# Create the selection bar
selected_option = st.selectbox("Select an Underwater enhance method :", options, index=0)

# Create a file uploader widget
file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)
# Create a two-column layout
with col1:
    # First column
    st.subheader("Input Image")
    if file is None:
        image = Image.open('sample.png')
        st.image(image, caption="Sample Image", use_column_width=True)
    else:
        image = Image.open(file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    # set a button to enhance the image
    if st.button("Enhance Image"):
        with col2:
            st.subheader("Enhanced Image")
            if  'image' in locals():
                # display a loading spinner
                # record the time taken for the processing
                start_time = time.time()
                with st.spinner("Processing image..."):
                    # enhance the image
                    enhanced_image = enhance_my(image)
                end_time = time.time()
                # display the enhanced image
                st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)
                st.write("Time taken for processing: ", end_time - start_time, "seconds")
            else:
                st.warning("Please upload an image to see the enhanced version")



