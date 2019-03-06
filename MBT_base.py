# -*- coding: utf-8 -*-
import subprocess
import time
import re


def runs(opt, driver, **kwargs):
    a = {1: "web", 2: "android", 3: "ios", }
    file = opt["file"]  # 执行的模型图
    script_file = "{}_{}".format(file, a[opt["device"]])
    end_condition = opt["end_condition"]
    speed = opt["speed"]  # 执行速度, 每个操作后的等待时间, 单位为秒
    model_log = "log/{}_model.log".format(file)  # 模型生成的测试用例保存 log
    test_log = "log/{}_test.log".format(file)  # 测试执行的 log
    exec('from page_script import ' + script_file)  # 导入指定文件的包, 即脚本文件

    # 对要执行的模型图名处理, 对中英文逗号进行处理
    file = file.replace(',', '.graphml ' + end_condition + ' -m model/')
    file = file.replace('，', '.graphml ' + end_condition + ' -m model/')
    model = '-m model/' + str(file) + '.graphml ' + end_condition

    # gw 为要执行的 graphwalker 指令
    gw = "java -jar graphwalker-cli-4.0.0-SNAPSHOT.jar offline " + model + \
         " -o | jq -r '. | .currentElementName, .actions[0].Action, .modelName'"

    # 将 model 运行结果保存至文件的方法
    def run_cmd2file(cmd):
        fdout = open(model_log, 'w+')
        fdout.write("This is model log")
        fderr = open("model_err.log", 'w+')
        p = subprocess.Popen(cmd, stdout=fdout, stderr=fderr, shell=True)
        if p.poll():
            return
        p.wait()
        return

    # 将要执行的操作记录进入 test_log
    def editLog(content):
        with open(test_log, 'a+') as f2:
            f2.write("begin........" + content)

    # 生成测试用例
    run_cmd2file(gw)

    # 创建测试结果保存文件 test_log
    with open(test_log, 'w+') as f1:
        f1.write(time.asctime(time.localtime(time.time())) + "\n")

    # 按 model 文件生成的测试用例执行测试,测试结果保存至 test_log 文件
    with open(model_log, 'r+') as f:
        for line in f:
            editLog(line)
            # 执行以 e_ 开头的路径并获取传入参数和模块
            if line[:2] == "e_":
                value = next(f)
                # 因为执行了 next 操作,所以需要再记录一次要执行的操作
                editLog(value)
                obj = next(f)
                # 因为执行了 next 操作,所以需要再记录一次要执行的操作
                editLog(obj)
                # sub_module = getattr(eval(file), "Action")(driver)
                sub_module = eval(script_file).Action(driver)
                if kwargs:
                    ''' 
                    特殊方法，获取从 test_main 中传过来的参数，平时可以注释不用
                    '''
                    for key, value in kwargs.items():
                        if str(key) in line.strip('\n'):
                            getattr(sub_module, line.strip('\n'))(value)
                        else:
                            # 判断是否有值要传入
                            try:
                                getattr(sub_module, line.strip('\n'))(re.search(r"['\"](|.+?)['\"]", value).group(1))
                            except AttributeError:
                                getattr(sub_module, line.strip('\n'))()
                        time.sleep(speed)
                else:
                    try:
                        getattr(sub_module, line.strip('\n'))(re.search(r"['\"](|.+?)['\"]", value).group(1))
                    except AttributeError:
                        getattr(sub_module, line.strip('\n'))()
                    time.sleep(speed)
            else:
                pass
