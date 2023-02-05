# UW_Collect

1. install the requirements.txt `pip install -r requirements.txt`

2. download pretrained models from https://drive.google.com/uc?id=1E7edgJ83wuLrTRMO7HWd1zL_Z-e2_Zsq and put it in folder `pretrained models`

3. run on local `streamlit run streamlit_app.py`

   deploy on web:
   1) run on port 80 (it can be any port): `streamlit run streamlit_app.py --server.port 80`
   2) install ngrok and add auth_token follow this https://ngrok.com/docs/getting-started
   3) run `ngrok http -region ap 80`
   
