# coding:utf-8

import commands, re, logging
import config

logger = logging.getLogger(__file__)

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



def checkgit():
    '''
    检查git, 并与mongo中记录对比, 返回需要更新的分支列表.
    :return: list
    '''
    (status, output) = commands.getstatusoutput('git branch -vr')
    assert (status)
    branches = get_branches(output)
    logger.info(branches)

if __name__ == "__main__":
    checkgit()
