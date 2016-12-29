# coding:utf-8

import config
import commands, time

##
## 特别注意, 使用本功能需要自己配置好supervisor, 本程序只是重启supervisor监控对象.
##

def checkbrach(branch_name = config.WATCH_BRANCH):
    (status, output) = commands.getstatusoutput('git checkout {}'.format(branch_name))
    (status, output) = commands.getstatusoutput('git pull')
    return "Already" not in output

def start_renew():
    while True:
        if(checkbrach()):
            print("will update branch.") # pkill -f server_debug.py
            (status, output) = commands.getstatusoutput('pip install -r requirments.txt -i http://pypi.douban.com/simple/')
            (status, output) = commands.getstatusoutput('supervisorctl restart all')
            print("restart finish, result is:")
            print(output)

        print("done! this program will wait {} seconds to next scan.".format(config.INTERVAL))
        time.sleep(config.INTERVAL)

if __name__ == "__main__":
    try:
        start_renew()
    except KeyboardInterrupt:
        print("renew will shut down immediately.")