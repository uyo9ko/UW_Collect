# Underwater enhancement methods Collect

1. install the requirements.txt `pip install -r requirements.txt`

2. download pretrained models follow urls in `pretrained_models/download.txt` and put it in folder `pretrained_models`

3. run on local `streamlit run Underwater_Single_Image_Enhancer.py`

   deploy on web:
   1) run on port 80 (it can be other port): `streamlit run Underwater_Single_Image_Enhancer.py --server.port 80`
   2) install ngrok and add auth_token follow this https://ngrok.com/docs/getting-started
   3) run `ngrok http -region ap 80`
   
