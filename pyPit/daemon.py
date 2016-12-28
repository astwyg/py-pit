# coding:utf-8

import config
import commands, time
from checkgit import checkgit

def create_package(name, version):
    '''
    打包
    :param branch: str, 分支名
    :return:
    '''
    if config.SHELL_NAME and config.SHELL_CONTENT:
        (status, output) = commands.getstatusoutput('echo "{}" > {}'.format(config.SHELL_CONTENT, config.SHELL_NAME))

    (status, output) = commands.getstatusoutput('git checkout '+ name)
    (status, output) = commands.getstatusoutput('git pull ')
    (status, output) = commands.getstatusoutput('rm -r env/')
    (status, output) = commands.getstatusoutput('virtualenv env --no-site-packages')
    (status, output) = commands.getstatusoutput('env/bin/pip install -r requirments.txt -i http://pypi.douban.com/simple/')
    filename = "{}.zip".format(name.replace("/","_")+"__"+version+"__"+time.strftime("%Y%m%d%H%M%S", time.localtime()))
    (status, output) = commands.getstatusoutput('zip -r {} ./*'.format(filename))
    (status, pwd) = commands.getstatusoutput("pwd")
    (status, output) = commands.getstatusoutput("mkdir "+config.DIST_PATH+pwd.split("/")[-1]+"/")
    (status, output) = commands.getstatusoutput('mv {} {}'.format(filename, config.DIST_PATH+pwd.split("/")[-1]+"/"))

def start_daemon():
    while True:
        branches_to_update = checkgit()
        print("those features need pack up..")
        print(branches_to_update)
        for branch in branches_to_update:
            print("start to pack up:" + branch["name"])
            create_package(branch["name"], branch["version"])
            print("successful packed up:" + branch["name"])
        print("done! this program will wait {} seconds to next scan.".format(config.INTERVAL))
        time.sleep(config.INTERVAL)

if __name__ == "__main__":
    try:
        start_daemon()
    except KeyboardInterrupt:
        print("daemon will shut down immediately.")