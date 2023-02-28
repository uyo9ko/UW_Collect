import streamlit as st
from PIL import Image,ImageOps
import numpy as np
import os
import time
import base64
from pathlib import Path
from nevaluate import nmetrics


def resize_image(image, max_size):
    width, height = image.size
    if width >= height:
        ratio = width/height
        image = image.resize((max_size, int(max_size/ratio)))
        image = ImageOps.expand(image, (0, int((max_size - image.height) / 2)), fill='white')
    else:
        ratio = height/width
        image = image.resize((int(max_size/ratio), max_size))
        image = ImageOps.expand(image, (int((max_size - image.width) / 2), 0), fill='white')
    return image


@st.cache
def cal_metrics(image):
    uiqm_1, uciqe_1 = nmetrics(np.array(image))
    return uiqm_1, uciqe_1


@st.cache
def enhance_image_my(image):
    my_model = MyModel()
    enhanced_image = my_model.enhance(image)
    uiqm_2, uciqe_2 = nmetrics(np.array(enhanced_image))
    return enhanced_image, uiqm_2, uciqe_2

@st.cache
def enhance_image_funie(image):
    funiegan = FunieGAN()
    enhanced_image = funiegan.enhance(image)
    uiqm_2, uciqe_2 = nmetrics(np.array(enhanced_image))
    return enhanced_image, uiqm_2, uciqe_2

@st.cache
def enhance_image_ursct(image):
    ursct_sesr= URSCT_SESR()
    enhanced_image = ursct_sesr.enhance(image)
    uiqm_2, uciqe_2 = nmetrics(np.array(enhanced_image))
    return enhanced_image, uiqm_2, uciqe_2

@st.cache
def enhance_image_udcp(image):
    udcp= UDCP()
    enhanced_image = udcp.enhance(image)
    uiqm_2, uciqe_2 = nmetrics(np.array(enhanced_image))
    return enhanced_image, uiqm_2, uciqe_2




st.set_page_config(page_title="Underwater Single Image Enhancer", page_icon="🤔", layout="wide")
# st.sidebar.header("Underwater Single Image Enhancer")
empty_image = Image.open('camera_1.png')
MAX_SIZE = 500
empty_image = resize_image(empty_image,MAX_SIZE)
image = None
left,middle,right = st.columns([1,4,1])
with middle:
    st.title("Underwater Single Image Enhancer")
    # Define the options for the selection bar
    # options = ['MyModel', 'UDCP', 'GCDP', 'UWCNN','Ucolor']
    options = ['UDCP', 'FunieGAN','URSCT_SESR','MyModel']
    # Create a imgfile uploader widget
    imgfile = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

_,col1, col2,_ = st.columns([1,2,2,1])

with col1:
    st.subheader("Input Image")
    form = st.form("my_form")
    tab11,tab12 = form.tabs(['Image','Metrics'])
    with tab11:
        placeholder_1 = st.empty()
        placeholder_1.image(empty_image, caption="Uploaded Image", use_column_width=True)
    with tab12:
        placeholder_uiqm_1 = st.empty()
        placeholder_uciqe_1= st.empty()
        placeholder_uiqm_1.metric("UIQM", "0.0")
        placeholder_uciqe_1.metric("UCIQE", "0.0")

    selected_option = form.selectbox("Select an Underwater enhance method :", options, index=0)
    sb = form.form_submit_button("Enhance")

with col2:  
    st.subheader("Enhanced Image")
    tab21,tab22 = st.tabs(['Image','Metrics'])
    with tab21:
        placeholder_2 = st.empty()
        placeholder_2.image(empty_image, caption="Enhanced Image", use_column_width=True)
    with tab22:
        placeholder_uiqm_2 = st.empty()
        placeholder_uciqe_2 = st.empty()
        placeholder_uiqm_2.metric("UIQM", "0.0","0.0")
        placeholder_uciqe_2.metric("UCIQE", "0.0","0.0")

if imgfile is not None:
    image = Image.open(imgfile)
    with col1:
        if image:
            resized_image = resize_image(image, MAX_SIZE)
            placeholder_1.image(resized_image, caption="Uploaded Image", use_column_width=True)
            uiqm_1, uciqe_1 = cal_metrics(image)
            placeholder_uiqm_1.metric("UIQM", f"{uiqm_1:.2f}")
            placeholder_uciqe_1.metric("UCIQE", f"{uciqe_1:.2f}")
            st.session_state["uiqm_1"] = uiqm_1
            st.session_state["uciqe_1"] = uciqe_1


if sb:
    with col2:
        if image :
            start_time = time.time()
            if selected_option == 'MyModel':
                from UE_code.enhance import MyModel
                enhanced_image, uiqm_2, uciqe_2 = enhance_image_my(image)
            elif selected_option == 'FunieGAN':
                from Funie_GAN_code.enhance import FunieGAN
                enhanced_image, uiqm_2, uciqe_2 = enhance_image_funie(image)
            elif selected_option == 'URSCT_SESR':
                from URSCT_SESR_code.enhance import URSCT_SESR
                enhanced_image, uiqm_2, uciqe_2 = enhance_image_ursct(image)
            elif selected_option == 'UDCP':
                from UDCP_code.enhance import UDCP
                enhanced_image, uiqm_2, uciqe_2 = enhance_image_udcp(image)    

            end_time = time.time()
            st.session_state["enhanced_image"] = enhanced_image
            st.session_state["uiqm_2"] = uiqm_2
            st.session_state["uciqe_2"] = uciqe_2
            st.session_state["enhance_time"] = end_time - start_time
        else:
            st.warning("Please upload an image to see the enhanced version")

if "enhanced_image" in st.session_state:
    with col2:
        resized_enhanced_image = resize_image(st.session_state["enhanced_image"], MAX_SIZE)
        placeholder_2.image(resized_enhanced_image, caption="Enhanced Image", use_column_width=True)
        placeholder_uiqm_2.metric("UIQM", f"{st.session_state['uiqm_2']:.2f}", f"{st.session_state['uiqm_2']- st.session_state['uiqm_1']:.2f}")
        placeholder_uciqe_2.metric("UCIQE", f"{st.session_state['uciqe_2']:.2f}", f"{st.session_state['uciqe_2']- st.session_state['uciqe_1']:.2f}")
        st.success("Image enhanced successfully")
        st.write(f"Enhance time: {st.session_state['enhance_time']:.2f} seconds")
        st.session_state["enhanced_image"].save('enhance_img.png')

with col2:
    with open("enhance_img.png", "rb") as the_file:
        btn = st.download_button(
                label="Download image",
                data=the_file,
                file_name="enhance_img.png",
                mime="image/png"
            )






