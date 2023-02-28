from PIL import Image
import os
import numpy as np

from UDCP_code.RefinedTramsmission import Refinedtransmission
from UDCP_code.getAtomsphericLight import getAtomsphericLight
from UDCP_code.getGbDarkChannel import getDarkChannel
from UDCP_code.getTM import getTransmission
from UDCP_code.sceneRadiance import sceneRadianceRGB

class UDCP():
    def __init__(self, ):
        pass

    def enhance(self,img):
        img = np.array(img)
        blockSize = 9
        GB_Darkchannel = getDarkChannel(img, blockSize)
        AtomsphericLight = getAtomsphericLight(GB_Darkchannel, img)
        transmission = getTransmission(img, AtomsphericLight, blockSize)
        transmission = Refinedtransmission(transmission, img)
        sceneRadiance = sceneRadianceRGB(img, transmission, AtomsphericLight)
        return Image.fromarray(np.uint8(sceneRadiance))



# test_img = Image.open('./test.png')
# res_img = enhance(test_img)
# res_img.save('res.png')