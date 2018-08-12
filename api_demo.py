from aip import AipOcr
import numpy as np
from OCRSDK import OCRservice
"""
Autor: Wilson.Zhang
Date: 2018/08/06
Usage: This is a demo using Baidu OCR service, the picture is in URL
Documentation: http://ai.baidu.com/docs#/OCR-Python-SDK/top
"""

# #APP_ID, API_KEY, SECRET_KEY, 若您有付费版百度云AI账号，可以自行创建后更换。
# APP_ID = "11638437"
# API_KEY = "iNQHH8yb3CVBEw5hSZu8wtBe"
# SECRET_KEY = "Cb3w4VSjXzwHlGoVIQxbcDusSlqG554F"
#
# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
# #以URL形式调用图片。。。
# url = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1534070480995&di=436ce4597a0e5d785091360d1f920cc0&imgtype=jpg&src=http%3A%2F%2Fimg0.imgtn.bdimg.com%2Fit%2Fu%3D3014325480%2C889709218%26fm%3D214%26gp%3D0.jpg"
#
# #如果有可选参数
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
#
# result = client.basicGeneralUrl(url, options)
# print(result)

result = OCRservice.GetOCRResult(APINAME="Tencent", FILECONTENT="./timg.jpg")
print(result)
result = OCRservice.GetOCRResult(APINAME="Baidu", FILECONTENT="./timg.jpg")
print(result)