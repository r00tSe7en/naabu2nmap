import nmap
from queue import Queue
from multiprocessing import Process, Lock
from rich.console import Console
import argparse

console = Console()

# 创建进程互斥锁
lock = Lock()
task_queue = Queue()

# 调用naabu result
def port_scan(file):
    ip_port_list = []
    
    for ip_port in open(file, mode='r'):
        ip_port_list.append(ip_port.replace("\n", ""))

    for i in ip_port_list:
        task_queue.put(i)

def write_result(file_name,content):
    fp = open(file_name, "a+", encoding="utf-8")
    fp.write(content + "\n")
    fp.close()

def service_scan(ip_port):
    scan_ip_port = ip_port.split(':')
    ip = scan_ip_port[0]
    port = scan_ip_port[1]
    try:
        nm = nmap.PortScanner()
        ret = nm.scan(ip, port, arguments='-Pn -sSV')
        for key in ret["scan"]:
            info = ret['scan'][key]['tcp'][int(port)]
            name = info['name']
            product = info['product']
            version = info['version']
            extrainfo = info['extrainfo']
            content = ip + "," + str(port) + "," + name + "," + product + "," + version + "," + extrainfo
            if(info['state'] == "open"):
                lock.acquire()
                write_result(args.output,content)
                lock.release()
                print(ip + ":" + str(port) + "  " +
                      "name：" + name + "  " +
                      "product：" + product + "  " +
                      "version：" + version + "  " +
                      "extrainfo：" + extrainfo)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'please enter two parameters ...'
    parser.add_argument("-f", "--file")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    port_scan(args.file)
    write_result(args.output,"ip,port,name,product,version,extrainfo")
    console.print('[+]端口加载完毕，即将进行服务识别...',style="#ADFF2F")
    process_list = []
    while not task_queue.empty():
        # 修改进程数请在此处修改range(10)
        for i in range(10):
            try:
                ip_port = task_queue.get(timeout=10)
                p = Process(target=service_scan, args=(ip_port,))
                p.start()
                process_list.append(p)
            except:
                pass
        for j in process_list:
            j.join()
        process_list.clear()
