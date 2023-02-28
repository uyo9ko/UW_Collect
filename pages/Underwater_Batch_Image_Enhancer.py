import streamlit as st
from PIL import Image,ImageOps
import numpy as np
import os


import time
import base64
from pathlib import Path
from nevaluate import nmetrics
import pandas as pd
import glob
import zipfile


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
def cal_metrics(files, df_input, name2file):
    for imgfile in files:
        name2file[imgfile.name] = imgfile
        image = Image.open(imgfile)
        uiqm, uciqe = nmetrics(np.array(image))
        df_input.loc[-1]= [imgfile.name, uiqm, uciqe]
        df_input.index = df_input.index + 1
        df_input = df_input.sort_index()
    return df_input, name2file



st.set_page_config(page_title="Underwater Batch Image Enhancer", page_icon="🤖️", layout ='wide')
# st.sidebar.header("Underwater Batch Image Enhancer")

left,middle,right = st.columns([1,4,1])
with middle:
    st.title("Underwater Batch Image Enhancer")
    # Define the options for the selection bar
    options = ['UDCP', 'FunieGAN','URSCT_SESR','MyModel']
    # Create a file uploader widget
    files = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

_,col1, col2,_ = st.columns([1,2,2,1])

empty_df = pd.DataFrame(columns=['Image Name', 'UIQM', 'UCIQE'])
for i in range(5):
    empty_df.loc[-1]=["", "", ""]
    empty_df.index = empty_df.index + 1
    empty_df = empty_df.sort_index()

with col1:
    st.subheader("Input Image")
    # form = st.form("my_form")
    placeholder_table1= st.empty()
    placeholder_table1.table(empty_df)
    selected_option = st.selectbox("Select an Underwater enhance method :", options, index=0)
    sumbit_button = st.button("Enhance")


with col2:  
    st.subheader("Enhanced Image")
    placeholder_table2 = st.empty()
    placeholder_table2.table(empty_df)

name2file = {}
if len(files) > 0:
    # read the image file
    with col1:
        with st.spinner("Calculating Metrics..."):
            df_input = pd.DataFrame(columns=['Image Name', 'UIQM', 'UCIQE'])
            df_input,name2file = cal_metrics(files, df_input, name2file)
            placeholder_table1.table(df_input)
    

if sumbit_button: 
    with col2:
        if  'df_input' in locals():
            # clear the output folder
            for file in os.listdir('batch_results'):
                os.remove(os.path.join('batch_results', file))
            start_time = time.time()
            df_output = pd.DataFrame(columns=['Image Name', 'UIQM', 'UCIQE'])
            work_list = df_input['Image Name'].tolist()
            progress_bar = st.progress(0)
            if selected_option == 'MyModel':
                from UE_code.enhance import MyModel
                enhance_model = MyModel()
            elif selected_option == 'FunieGAN':
                from Funie_GAN_code.enhance import FunieGAN
                enhance_model = FunieGAN()
            elif selected_option == 'URSCT_SESR':
                from URSCT_SESR_code.enhance import URSCT_SESR
                enhance_model = URSCT_SESR()
            elif selected_option == 'UDCP':
                from UDCP_code.enhance import UDCP
                enhance_model = UDCP()

            for idx, img_name in enumerate(work_list):
                progress_bar.progress((idx+1)/len(work_list))
                image = Image.open(name2file[img_name])
                enhanced_image = enhance_model.enhance(image)
                enhanced_image.save(os.path.join('batch_results', img_name))
                uiqm, uciqe = nmetrics(np.array(enhanced_image))
                df_output.loc[-1]= [img_name, uiqm, uciqe]
                df_output.index = df_output.index + 1
                df_output = df_output.sort_index()
                placeholder_table2.table(df_output)
            end_time = time.time()
            st.session_state['df_output'] = df_output
            st.success("ALL images enhanced successfully")
            st.write('average uiqm', df_output['UIQM'].mean())
            st.write('average uciqe', df_output['UCIQE'].mean())
            st.write("Time taken for processing: ", end_time - start_time, "seconds")
        else:
            st.warning("Please upload images to see the enhanced version")

if 'df_output' in st.session_state:
    placeholder_table2.table(st.session_state['df_output'])



# open it as a regular file and supply to the button as shown in the example:
with open("images.zip", "rb") as file:
    # create the file, from your code
    outputs = glob.glob('batch_results/*')
    if len(outputs) > 0:
        with zipfile.ZipFile("images.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for idx,image in enumerate(outputs):
                with open(image, 'rb') as f:
                    img_data = f.read()
                    z.writestr(os.path.basename(outputs[idx]),img_data)
        with col2:
            btn = st.download_button(
                    label = "Download Images",
                    data = file,
                    file_name = "images.zip",
                    mime = "application/zip"
                )