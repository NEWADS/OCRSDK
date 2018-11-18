import OCRservice
"""
Autor: Wilson.Zhang
Date: 2018/08/06
Usage: This is a demo using Baidu & Tencet OCR service, the picture is in CONTENT array
Documentation: http://ai.baidu.com/docs#/OCR-Python-SDK/top
               https://ai.qq.com/doc/ocrgeneralocr.shtml
"""

# result = OCRservice.GetOCRResult(API="Tencent", CONTENT=["./timg4.jpg",
#                                                          "./timg.jpg"])
# print(result)
result = OCRservice.GetOCRResult(API="AUTO", CONTENT=["./pan.jpg"])
print(result)