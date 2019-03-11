# MBT_CX
MBT (Model-based testing) 基于模型测试
## 概念：
属于一种测试方法：利用模型自动产生测试用例/测试套件，然后执行测试。
## 运行环境：
#### 1.	yEd 下载（非必须）：
查看和编辑模型图的软件，模型图文件全部在 model 文件夹下，后缀为 .graphml 的文件
下载地址： https://www.yworks.com/downloads - yEd
也可以在线使用：https://www.yworks.com/yed-live/
#### 2.	安装并配置 Java 环境（必须）：
安装并配置 Java 环境，推荐 Java8
#### 3.	python3（必须）：
安装并配置 Python3 环境
#### 4.	jq（必须）：
命令行 json 处理工具，对 graphwalker 生成的测试用例进行筛选，安装方法：``brew install jq``（需要先安装 brew）。其它安装方法请查看官方文档：https://stedolan.github.io/jq/
#### 5.	selenium环境（web 端测试必须，Android、 iOS 非必须）：
selenium：浏览器自动测试工具，安装 Python3后在终端输入 ``pip3 install selenium`` 即可安装
#### 6.	chromedriver（web 端测试 Chrome 浏览器必须）: 
1.	下载 https://sites.google.com/a/chromium.org/chromedriver/downloads
2. 将解压的 chromedriver 移动到/usr/local/bin目录下
#### 7.  Appium环境（Android、iOS 端测试必须）：
	内容比较多，Android 和 iOS 不同，具体请查看 Appium 官方文档安装：
	http://appium.io/docs/en/about-appium/getting-started/
## 使用
#### Web 端：
1.	修改test_main.py 中的内容，调整一些测试参数和选择要测试的内容等（不需要执行的测试取消 @pytest.mark.skip("nothing") 的注释即可）
2.	在MBT文件夹下执行：pytest 开始测试
3.	测试完成后在 report 文件夹下会生成本次的测试报告
#### Android、iOS 端：
1.	连接 Android、iOS 设备或模拟器，Android 准备好 REVINYL 测试 apk，iOS 安装好REVINYL
2.	启动 Appium 服务
3.	修改 test_main.py 中的内容，调整一些测试参数和选择要测试的内容（
Android 将测试 apk 放入 application 文件夹下，并将 test_main.py 中的 app 修改为 apk 的名字）
4.	在MBT文件夹下执行：pytest 开始测试
5.	测试完成后在 report 文件夹下会生成本次的测试报告
#### 其它
1.	iOS 使用中失败报错如果类似：
E       selenium.common.exceptions.WebDriverException: Message: An unknown server-side error occurred while processing the command. Original error: Error Domain=com.facebook.WebDriverAgent Code=1 "The element '"Cancel" Button' is not visible on the screen and thus is not interactable" UserInfo={NSLocalizedDescription=The element '"Cancel" Button' is not visible on the screen and thus is not interactable}
解决办法：尝试升级 Appium 或者 iOS 版本，具体见：
https://github.com/facebook/WebDriverAgent/issues/914

2.	@pytest.mark.skip("nothing") 会跳过该测试，测试中注释掉即可

