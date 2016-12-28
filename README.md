# py-pit

这是一个pyhton打包服务器项目, 将监视git服务器, 并生成最新的发布包, 使用发布包可以一键启动项目, 非常适合需要把python用出java味道的公司.

# 工作原理

1. *daemon.py* 启动的守护程序将每分钟轮询一次git服务器, 如果发现有新分支, 或者受控分支版本有更新, 则将该分支加入待打包队列, 并将新的git服务器状态存入mongo.
2. 如果待打包队列不为空, 则依次切换至待打包分支, 拉取最新代码, 然后安装 *virtualenv* , 生成启动脚本, 打包, 并将打包文件移动到归档目录.
 
# 咋用

**待更新**

1. `pip install git+https://github.com/astwyg/py-pit.git`
2. 装好virtualenv
3. 去你的git目录, 先把git配置好, 然后`python -m pyPit.daemon`

# TIPS

1. 记得改 *config.py*
