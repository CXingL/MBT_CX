import subprocess
import sys
import os
import getopt
import re

file = 'model/Example.graphml'
end_condition = '"weighted_random(edge_coverage(100))"'
# 结束条件, 一般: '"weighted_random(edge_coverage(100))"'
# 到达某个顶点结束: '"weighted_random(reached_vertex(v_sureEdit))"'
# 执行动作达到次数结束: '"weighted_random(length(200))"'


def run_model():
    file1 = '-m ' + file + ' ' + end_condition

    gw = "java -jar graphwalker-cli-4.0.0-SNAPSHOT.jar offline " + file1 + \
         " -o | jq -r '. | .currentElementName, .actions[0].Action, .modelName'"

    # 获取脚本生成类型
    a = input("请输入脚本生成类型( Web=1, Android=2, Ios=3) :")
    while True:
        if a in ["1", "2", "3"]:
            break
        else:
            a = input("请输入脚本生成类型( Web: 1, Android: 2, Ios: 3) :")
    A = ["web", "android", "ios"]
    B = ["Web", "Android", "Ios"]

    # 根据输入生成不同的脚本名称
    file_name = re.search(r'/(.*?)\.', file).group(1)
    script_name = file_name + '_' + A[int(a) - 1] + '.py'

    # 将 model 运行结果保存至 model.log 文件中
    def run_cmd2file(cmd):
        fdout = open('page_script/model.log', 'w+')
        p = subprocess.Popen(cmd, stdout=fdout, shell=True)
        if p.poll():
            return
        p.wait()
        return

    run_cmd2file(gw)

    with open('page_script/model.log', "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 去重顺便检查文件是否为空, 为空则表示生成测试用例失败，退出
        if len(lines) == 0:
            sys.exit(2)
        lines2 = []
        for i in lines:
            if i not in lines2:
                lines2.append(i)
        lines = lines2

    with open('page_script/model.log', "w", encoding="utf-8") as f_w:
        # 默认文件头，import，class，init 等
        cla = 'import helper\nimport random\nfrom time import sleep\n\n\nclass Action(helper.' + B[int(a) - 1] + '):' \
                                                            '\n    def __init__(self, driver):\n        helper.' + \
              B[int(a) - 1] + '.__init__(self, driver)\n'
        f_w.write(cla)

        # 将 e_ 对应函数
        find_way = {"web": "find_element_by_xpath('')",
                    "android": "find_element_by_id('')",
                    "ios": "find_element_by_ios_predicate('')"}

        # 生成测试脚本的装饰器函数
        def script_method(platform):
            def method(fn):
                def wrapper(name):
                    if "input" in name.lower():
                        if platform in ["web", "ios"]:
                            return """
    def {}(self):
        self.driver.{find_way}.clear()
        self.driver.{find_way}.send_keys('')\n""".format(fn(name), find_way=find_way[platform])
                        else:
                            return """
    def {}(self):
        self.driver.{find_way}.send_keys('')\n""".format(fn(name), find_way=find_way[platform])
                    elif "alert" in name.lower():
                        return """
    def {}(self):
        sleep(0.5)
        self.driver.switch_to_alert().accept()
        self.driver.switch_to_alert().dismiss()\n""".format(fn(name))
                    else:
                        return """
    def {}(self):
        self.driver.{find_way}.click()\n""".format(fn(name), find_way=find_way[platform])
                return wrapper
            return method

        # 生成测试脚本的方法，name 应该是 e_ 动作
        @script_method(platform=A[int(a)-1])
        def create(name):
            return name

        # 逐行读取，对 e_ 生成并写入到测试脚本中
        for line in lines:
            if line[:2] == "e_":
                result = create(line.replace("\n", ""))
                f_w.write(result)
            else:
                continue

    # test_main.py 中要写入的内容
    content = '\n    # @pytest.mark.skip("nothing")\n    def test_' + file_name + "(self, " + A[int(a) - 1] + "):\n" \
              + "        self.options['file'] = '" + file_name + "'\n" \
              + "        self.options['device'] = " + str(a) + "\n" \
              + "        MBT_base.runs(self.options, " + A[int(a) - 1] + ")\n"

    # 将 model.Log 的内容转移到脚本文件中，若脚本已存在则报错
    try:
        with open('page_script/' + script_name, "r"):
            print(script_name + " 文件已存在，请手动删除后重试！")
    except FileNotFoundError:
        # 打开文件，cNames读取所有行，储存在列表中
        with open('page_script/model.log', "r") as f1:
            lines = f1.readlines()
        # 将处理过的 lines 写入新的文件中
        with open('page_script/' + script_name, "w") as f2:
            f2.writelines(lines)
        # test_main 文件中写入新的测试内容
        with open('test_main.py', "a+") as f3:
            f3.write(content)


def verify_model():
    # 测试模型图是否正确的方法
    file2 = '-m ' + file + ' ' + end_condition
    gw = "java -jar graphwalker-cli-4.0.0-SNAPSHOT.jar offline " + file2
    try:
        os.system(gw)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 命令行参数获取
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:", ["help", "filename=", "test="])
        for opt_name, opt_value in opts:
            if opt_name in ('-h', '--help'):
                print('\n-h --help       查看帮助'
                      '-f --filename   后加执行的 model 文件名, 运行。多个文件用 "," 隔开'
                      '-t --test   后加测试的 model 文件名, 测试 model 是否可用。多个文件用 "," 隔开')
                sys.exit()
            elif opt_name in ('-f', '--filename'):
                file = opt_value
                run_model()
            elif opt_name in ('-t', '--test'):
                file = opt_value
                verify_model()
    except getopt.GetoptError:
        print('\n-h --help       查看帮助\n'
              '-f --filename   后加测试 model 文件名, 执行测试。\n')
        sys.exit(2)
