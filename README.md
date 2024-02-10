<p align="left">
  <img align="left" height="200" src="https://raw.githubusercontent.com/ravizhan/yangcong-dl/72618e7ee233c01bcc930fc62a456b4e74334c2c/logo2.svg" style="float: left;padding-right: 20px"/>
</p>

# yangcong-dl
洋葱学园视频下载器

![GitHub License](https://img.shields.io/github/license/ravizhan/yangcong-dl?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/ravizhan/yangcong-dl?style=for-the-badge)

## 使用方法
```shell
pip3 install -r ./requirements.txt
python3 ./main.py
```
或者[直接下载二进制版](https://github.com/ravizhan/yangcong-dl/releases)(不放心的可以自己编译)

>注：程序不存在任何后门(不放心的自己看源码)

>还是不放心输入账号密码的可以手动输入`authorization`, 获取方法👇
>![](https://i.mji.rip/2023/11/05/ee71beac66602915dca8a796c446d77b.png)
## 原理
这得从洋葱学园网站上的一个越权漏洞(或者说是逻辑漏洞，我也不太确定...偶然发现的)说起
一句话概括:这个漏洞可以让普通用户，即非vip用户，下载到vip视频
具体原理如下:
![](https://i.mij.rip/2024/01/20/7b46452cebbb681507b6bca70c5a70d6.png)
## 法律声明
本项目仅用于**学术研究**，由于使用本项目及其二进制文件等所产生的任何法律风险**与作者无关**。

## 关于开源
本项目于2020年10月17日开源，采用AGPLv3许可证，请自觉遵守。

## 鸣谢
- L 提供logo

## 相关开源库
### N_m3u8DL-CLI
>一个**简单易用**的m3u8下载器
>
>Github地址 [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI)
