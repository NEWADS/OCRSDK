from aip import AipOcr
from OCRSDK.TencentAPIMsg import *

"""
Autor: Wilson.Zhang
Date: 2018/08/12
Usage: 该文件调用了百度以及腾讯的OCR服务，并将得到的内容以字典形式返回给开发者
"""

"""
status状态字解释：
1：OCR成功接收图片且有字段返回
0：OCR成功接受了图片，但无字段返回
-1：文件路径出错
"""


def GetOCRResult(**args):
    result = {}
    # Baidu OCR：
    APP_ID = "11638437"
    API_KEY = "iNQHH8yb3CVBEw5hSZu8wtBe"
    SECRET_KEY = "Cb3w4VSjXzwHlGoVIQxbcDusSlqG554F"
    client_baidu = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # Tencent OCR：
    APP_ID = "2107641945"
    APP_KEY = "ONCdozjSNiDo1sZj"
    client_tencent = TencentAPIMsg(APP_ID, APP_KEY)
    if args.get("API") is "Baidu":
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
                        result[content] = {#"status": "failed, file content is wrong, please verify...",
                                           "status": -1,
                                           "wordlist": [],
                                           "wordposition": {}}
                        #return result
                    else:
                        bin = file.read()
                        #开启多余参数监测（虽然没什么用）
                        options = {}
                        options["language_type"] = "CHN_ENG"
                        options["detect_direction"] = "true"
                        options["detect_language"] = "true"
                        options["probability"] = "false"
                        tmp = client_baidu.basicGeneral(bin, options)
                        if not tmp["words_result_num"] is 0:
                            reslist = []
                            for resdict in tmp["words_result"]:
                                reslist.append(resdict["words"])
                            restmp = {"status": 1,
                                      "wordlist": reslist,
                                      "wordposition": {}}
                            result[content] = restmp
                        else:
                            restmp = {"status": 0,
                                      "wordlist": [],
                                      "wordposition": {}}
                            result[content] = restmp
        result["result"] = "Done!" #这里需要修改！！！
        return result
    elif args.get("API") is "Tencent":
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
                        result[content]={"status": -1,
                                         "wordlist": [],
                                         "wordposition": {}}
                    else:
                        file = client_tencent.get_img_base64str(content)
                        Req_Dict = {"image": file}
                        #生成请求包
                        Req_Dict = client_tencent.init_req_dict(req_dict=Req_Dict)
                        response = requests.post("https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr",
                                   data=Req_Dict)
                        restmp = response.json()
                        reslist = []
                        if restmp["ret"] == 0:
                            #result["result"] = "Success!"
                            resdata = restmp["data"]
                            if len(resdata["item_list"]) is 0:
                                resdict = {"status": 0,
                                           "wordlist": [],
                                           "wordposition": {}}
                                result[content] = resdict
                            else:
                                for tmp in resdata["item_list"]:
                                    reslist.append(tmp["itemstring"])
                                resdict = {"status": 1,
                                           "wordlist": reslist,
                                           "wordposition": {}}
                                result[content] = resdict
                        else:
                            result["result"] = "Failed! Http Response Error."
                            return result
            result["result"] = "Done!"
            return result
    elif args.get("API") is "AUTO":
        #让脚本选择的情况，默认优先采用腾讯的结果。若腾讯无字段返回，则采用百度的结果或无字段返回。
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
                        result[content] = {#"status": "failed, file content is wrong, please verify...",
                                           "status": -1,
                                           "wordlist": [],
                                           "wordposition": {}}
                        #return result
                    else:
                        #百度的OCR请求发送
                        bin = file.read()
                        # 开启多余参数监测（虽然没什么用）
                        options = {}
                        options["language_type"] = "CHN_ENG"
                        options["detect_direction"] = "true"
                        options["detect_language"] = "true"
                        options["probability"] = "false"
                        baidu = client_baidu.basicGeneral(bin, options)
                        #腾讯的OCR请求发送
                        file = client_tencent.get_img_base64str(content)
                        Req_Dict = {"image": file}
                        # 生成请求包
                        Req_Dict = client_tencent.init_req_dict(req_dict=Req_Dict)
                        response = requests.post("https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr",
                                                 data=Req_Dict)
                        tencent = response.json()
                        reslist = []
                        #开始分情况处理：
                        if tencent["ret"] is 0 and baidu["words_result_num"] is not 0:
                            resdata = tencent["data"]
                            if len(resdata["item_list"]) is not 0:
                                for tmp in resdata["item_list"]:
                                    reslist.append(tmp["itemstring"])
                                resdict = {"status": 1,
                                           "wordlist": reslist,
                                           "wordposition": {}}
                                result[content] = resdict
                            else:
                                for tmp in baidu["words_result"]:
                                    reslist.append(tmp["words"])
                                resdict = {"status": 1,
                                          "wordlist": reslist,
                                          "wordposition": {}}
                                result[content] = resdict
                        elif tencent["ret"] is not 0 and baidu["words_result_num"] is not 0:
                            for tmp in baidu["words_result"]:
                                reslist.append(tmp["words"])
                            resdict = {"status": 1,
                                       "wordlist": reslist,
                                       "wordposition": {}}
                            result[content] = resdict
                        elif tencent["ret"] is 0 and baidu["words_result_num"] is 0:
                            resdata = tencent["data"]
                            if len(resdata["item_list"]) is not 0:
                                for tmp in resdata["item_list"]:
                                    reslist.append(tmp["itemstring"])
                                resdict = {"status": 1,
                                           "wordlist": reslist,
                                           "wordposition": {}}
                                result[content] = resdict
                            else:
                                resdict = {"status": 0,
                                           "wordlist": [],
                                           "wordposition": {}}
                                result[content] = resdict
                        else:
                            result["result"] = "Failed! Http Response Error."
                            return result
            result["result"] = "Done!"
            return result
    else:
        result = {"result": "Oops, seems that we don't support this platform(we only support Baidu and Tencent now....)"}
        return result