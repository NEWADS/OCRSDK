from aip import AipOcr
from OCRSDK.TencentAPIMsg import *

"""
Autor: Wilson.Zhang
Date: 2018/08/12
Usage: 该文件调用了百度以及腾讯的OCR服务，并将得到的内容以字典形式返回给开发者
"""

def GetOCRResult(**args):
    result = {}
    if args.get("API") is "Baidu":
        #选择百度API的情况：
        APP_ID = "11638437"
        API_KEY = "iNQHH8yb3CVBEw5hSZu8wtBe"
        SECRET_KEY = "Cb3w4VSjXzwHlGoVIQxbcDusSlqG554F"
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        #filecontent = args.get("FILECONTENT") This is old version
        #读取图片
        if not "CONTENT" in args:
            result = {"result": "Failed! No input pic."}
            return result
        else:
            for content in args["CONTENT"]:
                if content:
                    #return content
                    try:
                        file = open(content, "rb")
                    except IOError:
                        result[content] = {"status": "failed, file content is wrong, please verify...",
                                           "wordlist": [],
                                           "wordposition": []}
                        #return result
                    else:
                        bin = file.read()
                        #开启多余参数监测（虽然没什么用）
                        options = {}
                        options["language_type"] = "CHN_ENG"
                        options["detect_direction"] = "true"
                        options["detect_language"] = "true"
                        options["probability"] = "false"
                        tmp = client.basicGeneral(bin, options)
                        if not tmp["words_result_num"] is 0:
                            reslist = []
                            for resdict in tmp["words_result"]:
                                reslist.append(resdict["words"])
                            restmp = {"status": "success",
                                      "wordlist": reslist,
                                      "wordposition": []}
                            result[content] = restmp
                        else:
                            restmp = {"status": "failed, no words are recognized.", "wordlist": [], "wordposition": []}
                            result[content] = restmp
        result["result"] = "Done!" #这里需要修改！！！
        return result
    elif args.get("API") is "Tencent":
        #选择腾讯API的情况：
        APP_ID = "2107641945"
        APP_KEY = "ONCdozjSNiDo1sZj"
        client = TencentAPIMsg(APP_ID, APP_KEY)
        #filecontent = args.get("FILECONTENT")
        if not "CONTENT" in args:
            result = {"result": "failed! No input pic."}
            return result
        else:
            for content in args["CONTENT"]:
                if content:
                    try:
                        file = open(content, "rb")
                    except IOError:
                        #result = {"result": "failed! File content is wrong, please verify..."}
                        result[content]={"status": "failed, file content is wrong",
                                         "wordlist": [],
                                         "wordposition": []}
                    else:
                        file = client.get_img_base64str(content)
                        Req_Dict = {"image": file}
                        #生成请求包
                        Req_Dict = client.init_req_dict(req_dict=Req_Dict)
                        response = requests.post("https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr",
                                   data=Req_Dict)
                        restmp = response.json()
                        reslist = []
                        if restmp["ret"] == 0:
                            #result["result"] = "Success!"
                            resdata = restmp["data"]
                            if len(resdata["item_list"]) is 0:
                                resdict = {"status": "failed, no words are recognized.",
                                           "wordlist": [],
                                           "wordpostiion": []}
                                result[content] = resdict
                            else:
                                for tmp in resdata["item_list"]:
                                    reslist.append(tmp["itemstring"])
                                resdict = {"status": "success",
                                           "wordlist": reslist,
                                           "wordposition": []}
                                result[content] = resdict
                        else:
                            result["result"] = "Failed! Http Response Error."
                            return result
            result["result"] = "Done!."
            return result
    elif args.get("API") is "AUTO":
        #让脚本选择的情况，默认优先调用百度，若百度出现超时或QPS上限，换用腾讯。
        APP_ID = "11638437"
        API_KEY = "iNQHH8yb3CVBEw5hSZu8wtBe"
        SECRET_KEY = "Cb3w4VSjXzwHlGoVIQxbcDusSlqG554F"
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    else:
        result = {"result": "Oops, seems that we don't support this platform(we only support Baidu now....)"}
        return result