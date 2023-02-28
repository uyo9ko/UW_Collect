import torchvision
import yaml
import argparse
from torch.utils.data import DataLoader
from URSCT_SESR_code.utils.model_utils import load_checkpoint
from URSCT_SESR_code.model.URSCT_model import URSCT
from tqdm import tqdm
from URSCT_SESR_code.utils.image_utils import torchPSNR, torchSSIM
import torchvision.transforms.functional as TF
import torch

class URSCT_SESR():
    def __init__(self, ):
        with open('./URSCT_SESR_code/configs/Enh_opt.yaml', 'r') as config:
            opt = yaml.safe_load(config)
            opt_test = opt['TEST']
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_detail_opt = opt['MODEL_DETAIL']
        self.model = URSCT(model_detail_opt).to(device)
        load_checkpoint(self.model, './pretrained_models/URSCT_SESR.pth')
        self.model.eval()

    def enhance(self, image):
        image = image.convert('RGB')
        # w = image.size[0]-image.size[0]%32
        # h = image.size[1]-image.size[1]%32
        image = TF.to_tensor(image)
        image = TF.resize(image, (256, 256))
        # image = TF.resize(image, (h, w))
        image = image.unsqueeze(0)
        with torch.no_grad():
            enhanced = self.model(image)
        enhanced = enhanced.squeeze(0)# ' bvbnm,./jhczx ft432`q1w21276tfb?'
        enhanced = torch.clamp(enhanced, 0, 1)
        enhanced = TF.to_pil_image(enhanced)
        return enhanced
