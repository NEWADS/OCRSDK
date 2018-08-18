# OCRSDK
这是一个基于Python 3的，调用了腾讯及百度OCR服务的SDK包，
目前支持同时输入多张图片且支持自动选择服务。
腾讯的API接口的请求打包部分fork自：
https://github.com/jdstkxx/PyTencentAI

##How to use it?
首先，请将该文件夹下载或clone至您的项目目录下。<br>
调用该SDK的方法为：<br>
```from OCRSDK import OCRservice``` <br>
目前该SDK至包含一个接口：
```GetOCRResult()```<br>
该接口需要输入两个参数，分别为：<br>
API: 包含三个选项：Baidu, Tencent及AUTO <br>
CONTENT: 应输入一个包含文件路径的数组 <br>
返回见api_demo.py