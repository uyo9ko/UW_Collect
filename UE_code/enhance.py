import os
from UE_code.model import MainModel
from UE_code.dataset import ImageDataset
import pytorch_lightning as pl
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch
import numpy as np
from PIL import Image
import gdown

def enhance_my(image):
    my_model = MainModel()
    if not os.path.exists('UE_code/model.pt'):
        # url = 'https://drive.google.com/uc?id=1E7edgJ83wuLrTRMO7HWd1zL_Z-e2_Zsq'
        # filename = 'UE_code/model.pt'
        # gdown.download(url, filename, quiet=True)
        os.system('gdown 1E7edgJ83wuLrTRMO7HWd1zL_Z-e2_Zsq -O pretrained_models/My_model.pt')
    model_weights = torch.load('pretrained_models/My_model.pt')
    prefix = 'model.'
    n_clip = len(prefix)
    model_weights = {k[n_clip:]: v for k, v in model_weights.items()
                    if k.startswith(prefix)}
    for key in list(model_weights.keys()):
        model_weights[key.replace('model.', '')] = model_weights.pop(key)

    my_model.load_state_dict( model_weights)
    my_model.eval()

    # load your pre-trained model
    transform = A.Compose(
                    transforms=[A.Resize(448, 608), ToTensorV2()],
                )

    # convert image to numpy array
    image = np.array(image)
    image = transform(image=image)["image"]
    image = image.float() / 255.0
    image = image.unsqueeze(0)

    # use the pre-trained model to predict enhanced image
    _trans, _atm, enhanced_image = my_model(image)
    enhanced_image = torch.clamp(enhanced_image, 0, 1)
    enhanced_image = enhanced_image.detach().numpy()
    enhanced_image = enhanced_image.squeeze(0)
    enhanced_image = enhanced_image.transpose(1, 2, 0)
    enhanced_image = (enhanced_image * 255).astype(np.uint8)
    # convert the numpy array back to image
    enhanced_image = Image.fromarray(enhanced_image)
    return enhanced_image