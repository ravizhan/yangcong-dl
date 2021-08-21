# yangcong-dl
洋葱学院视频下载(无视VIP)
# 关于开源
本项目于2020年10月17日开源，采用MIT许可证，请自觉遵守。
## 相关开源库
### N_m3u8DL-CLI
>一个**简单易用**的m3u8下载器
Github地址 [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI)

# 使用方法
```shell
pip3 install -r ./requirements.txt
python3 ./main.py
```
或者[直接下载二进制版](https://github.com/ravizhan/yangcong-dl/releases)(不放心的可以自己编译)

>注：程序不存在任何后门(不放心的自己看源码)

>还是不放心输入账号密码的可以手动输入`authorization`, 获取方法👇
>![](https://ci.cncn3.cn/4da2ba818c0d6f6624b80a19602bbc53.png)
# 原理
这得从洋葱学院网站上的一个越权漏洞(或者说是逻辑漏洞，我也不太确定...偶然发现的)说起
一句话概括:这个漏洞可以让普通用户，即非vip用户，下载到vip视频
具体原理如下:
![](https://cdn.cncn3.cn/webstatic/2021_cO4S4DJ6/yangcong-dl.svg)
# 法律声明
本项目仅用于**学术研究**，由于使用本项目及其二进制文件等所产生的任何法律风险**与作者无关**。
