"""
 > Script for testing .pth models  
    * set model_name ('funiegan'/'ugan') and  model path
    * set data_dir (input) and sample_dir (output) 
"""
# py libs
import os
import numpy as np
from PIL import Image
from glob import glob
from ntpath import basename
from os.path import join, exists
# pytorch libs
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision.utils import save_image
import torchvision.transforms as transforms
from Funie_GAN_code.PyTorch.nets import funiegan


class FunieGAN():
    def __init__(self):
        self.model_name = 'funiegan'
        self.model_path = 'pretrained_models/funie_generator.pth'
        self.is_cuda = torch.cuda.is_available()
        self.Tensor = torch.cuda.FloatTensor if self.is_cuda else torch.FloatTensor
        self.model = funiegan.GeneratorFunieGAN()
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
        if self.is_cuda: self.model.cuda()
        self.model.eval()
        self.img_width, self.img_height, self.channels = 256, 256, 3
        self.transforms_ = [transforms.Resize((self.img_height, self.img_width), Image.BICUBIC),
                            transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), ]
        self.transform = transforms.Compose(self.transforms_)

    def enhance(self, image):
        inp_img = self.transform(image)
        inp_img = Variable(inp_img).type(self.Tensor).unsqueeze(0)
        # generate enhanced image
        gen_img = self.model(inp_img)
        # to PIL image
        gen_img = gen_img.squeeze(0).cpu().detach().numpy()
        gen_img = (gen_img + 1) / 2
        gen_img = np.transpose(gen_img, (1, 2, 0))
        gen_img = Image.fromarray((gen_img * 255).astype(np.uint8))
        return gen_img



