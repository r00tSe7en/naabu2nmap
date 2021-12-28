# naabu2nmap
对naabu的端口扫描结果，调用nmap进行指纹识别
```
127.0.0.1:22
127.0.0.1:80
127.0.0.1:8080
```

# 使用方法
需要root权限
```shell
➜ sudo python3 scan.py -h                           
usage: scan.py [-h] [-f FILE] [-o OUTPUT]

please enter two parameters ...

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
  -o OUTPUT, --output OUTPUT
```
```shell
➜ sudo python3 scan.py -f naabu_result.txt -o nmap_result.csv
```
# 结果
保存为csv格式的文件
|   ip   | port     | name     |   product   |  version    |   extrainfo   |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 127.0.0.1 | 8080 | http-proxy | Burp Suite Professional http proxy |      |      |

# 参考
https://github.com/7dog7/masscan_to_nmap

![](https://starchart.cc/r00tSe7en/naabu2nmap.svg)

