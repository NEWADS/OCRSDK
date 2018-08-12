from aip import AipOcr
from PyTencentAI.TencentAPI import *
from PyTencentAI.TencentAPIMsg import *

"""
Autor: Wilson.Zhang
Date: 2018/08/12
Usage: 该文件调用了百度以及腾讯的OCR服务，并将得到的内容以JSON形式（暂定）返回给开发者
"""

def GetOCRResult(**args):
    if args.get("APINAME") is "Baidu" :
        #选择百度API的情况：
        APP_ID = "11638437"
        API_KEY = "iNQHH8yb3CVBEw5hSZu8wtBe"
        SECRET_KEY = "Cb3w4VSjXzwHlGoVIQxbcDusSlqG554F"
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        filecontent = args.get("FILECONTENT")
        #读取图片
        if filecontent is None:
            result = {"result": "failed! No input pic..."}
            return result
        else:
            file = open(filecontent, "rb")
            if file is None:
                result = {"result": "failed! File content is wrong, please verify..."}
                return result
            bin = file.read()
            #强制开启位置检测，因为需要位置。。。
            options = {}
            options["language_type"] = "CHN_ENG"
            options["detect_direction"] = "true"
            options["detect_language"] = "true"
            options["probability"] = "true"

            result = client.basicGeneral(bin, options)
            result["result"] = "Success!"
            return result
    elif args.get("APINAME") is "Tencent":
        #选择腾讯API的情况：
        APP_ID = "2107641945"
        APP_KEY = "ONCdozjSNiDo1sZj"
    else:
        result = {"result": "Oops, seems that we don't support this platform(we only support Baidu now....)"}
        return result