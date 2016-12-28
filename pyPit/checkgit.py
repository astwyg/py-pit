# coding:utf-8

import commands, re, logging, pymongo
import config

def get_branches(output):
    '''
    整理分支信息
    :param output: str, git输出信息
    :return: dict: key为分支名称, value.version为版本号
    '''
    def blank_filter(nodes):
        '''
        整理每行元素, 剔除空白信息
        :param nodes: list, 空格分割后每行的信息
        :return: list, 剔除空白信息的每行信息
        '''
        infos = []
        for node in nodes:
            if node:
                infos.append(node)
        return infos

    def feature_filter(feature_name):
        '''
        根据规则过滤需要监控的分支
        :param feature_name:
        :return: bool, 是否满足过滤条件
        '''
        if not config.FEATURE_RE:
            return True
        return not not len(re.findall(config.FEATURE_RE, feature_name))

    branches = {}
    lines = output.split("\n")
    for line in lines:
        nodes = blank_filter(line.split(" "))
        if nodes[1] != "->" and feature_filter(nodes[0]): # 忽略HEAD等分支, 根据规则过滤分支
            branches[nodes[0]] = nodes[1]
    return branches

def get_host_mark():
    '''
    得到主机标志
    :return:
    '''
    (status, hostname) = commands.getstatusoutput('hostname')
    (status, pwd) = commands.getstatusoutput('pwd')
    return hostname + "|" + pwd

def checkgit():
    '''
    检查git, 并与mongo中记录对比, 返回需要更新的分支列表.
    :return: list
        eg:['origin/biz_zhp', 'origin/feature/chentaihai', 'origin/wanghaisheng', 'origin/feature/guo
k', 'origin/feature/develop_billing_hull', 'origin/zhouxb', 'origin/feature/wangyq', 'origin/master', 'origin/chentaihai_new', 'origin/feature/lixiaoxiao', 'origin/develop', 'origin/feature/wangyonggang', 'origin/feature/user_manage', 'origin/ondemand', 'origin/feature/account_bind_contract']
    '''
    # 得到git信息
    (status, output) = commands.getstatusoutput('git checkout master | git pull')
    (status, output) = commands.getstatusoutput('git branch -vr')
    assert (not status)
    branches = get_branches(output)
    # 连接到mongodb, 获取上一次版本记录
    client = pymongo.MongoClient(config.MONGO_SERVER_HOST, config.MONGO_SERVER_PORT)
    db =client["pyPit"]
    coll = db["watchers"]
    host_mark = get_host_mark()
    record = coll.find_one({"host_mark":host_mark})
    # 比较现在状态和上一次记录
    branches_to_update = []
    if record is None: # 如果数据库中没有记录, 则全部存入, 更新全部分支.
        for k,v in branches.items():
            branches_to_update.append({"name":k, "version":v})
        coll.insert({
            "host_mark": host_mark,
            "branches": branches
        })
    else:
        for k,v in branches.items():
            if not record["branches"].get(k) or record["branches"][k] != v:
                branches_to_update.append({"name":k, "version":v})
        record["branches"] = branches
        coll.save(record)
    return branches_to_update


if __name__ == "__main__":
    branches_to_update = checkgit()
