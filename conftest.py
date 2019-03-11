# coding=utf-8
import test_main
import pytest
import os
import re
import base64
import subprocess
from appium import webdriver as aw
from selenium import webdriver as sw

# import allure
# import yaml
options = test_main.TestClass().options
platformVersion = []


@pytest.fixture(scope='function')
def web():
    """
    Web Selenium
    """
    browsers = {1: "Chrome", 2: "Safari", 3: "Firefox", 4: "Ie"}
    global wd
    if options["browser"] == 1:
        # 如果是 Chrome ，则可以设置一些参数
        images = options["has_images"]  # 是否加载图片, 1 为加载, 2为不加载
        # 配置 Chrome 的设置,例如不加载图片, 模拟移动设备, 添加扩展程序等
        chrome_opt = sw.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": images}
        chrome_opt.add_experimental_option("prefs", prefs)
        # 启动浏览器进行测试, 并设置最大等待时间
        wd = sw.Chrome(chrome_options=chrome_opt)
    elif options["browser"] == 5:
        # 按 browserstack 中的脚本替换内容：https://www.browserstack.com/automate/python
        desired_cap = {
            'browser': 'IE',
            'browser_version': '11.0',
            'os': 'Windows',
            'os_version': '10',
            'resolution': '1024x768'
        }
        wd = sw.Remote(
            command_executor='http://monstarlab1:qDypWv9guhHUHNDjAWqY@hub.browserstack.com:80/wd/hub',
            desired_capabilities=desired_cap)
    else:
        # 其他浏览器
        wd = getattr(sw, browsers[options["browser"]])()
    wd.implicitly_wait(options["page_wait"])
    yield wd
    wd.quit()


@pytest.fixture(scope='function')
def ios():
    """
    iOS Appium
    """
    uuid = subprocess.getoutput('idevice_id -l')
    command_executor1 = 'http://127.0.0.1:4723/wd/hub'
    desired_capabilities1 = {
        'platformName': 'iOS',
        'platformVersion': options["platformVersion"],
        'deviceName': 'iPhone',
        'bundleId': options["bundleId"],
        'udid': uuid,
        "automationName": "XCUITest",
    }
    global iosd
    iosd = aw.Remote(command_executor1, desired_capabilities1)
    iosd.implicitly_wait(10)  # find element timeout
    yield iosd
    iosd.quit()


@pytest.fixture(scope='function')
def android():
    """
    Android Appium
    """
    # 测试的包的路径和包名
    path = os.path.abspath('')
    appLocation = "{}/application/{}".format(path, options["app"])
    # 读取设备系统版本号，多个设备时默认选择第一个设备
    devices = subprocess.getoutput('adb devices')
    devices_list = re.findall(re.compile("\n(.+?)\t"), devices)
    deviceVersion = subprocess.getoutput('adb -s {} shell getprop ro.build.version.release'.format(devices_list[0]))
    # 读取 APK 的 package 信息
    appPackageAdb = subprocess.getoutput('aapt dump badging ' + appLocation)
    appPackage = re.findall(re.compile("package: name='(.*?)'"), appPackageAdb)[0]
    appPackageActivity = re.findall(re.compile("launchable-activity: name='(.*?)'"), appPackageAdb)[0]
    # 删除以前的安装包
    try:
        os.system('adb uninstall ' + appPackage)
    except Exception:
        pass

    command_executor2 = 'http://localhost:4723/wd/hub'
    desired_capabilities2 = {
        'platformName': 'Android',
        'platformVersion': deviceVersion,
        # 'platformVersion': "7.1",
        'deviceName': 'Android',
        'appPackage': appPackage,
        'appWaitPackage': appPackage,
        'app': appLocation,
        'appActivity': appPackageActivity,
        # 'noReset': True,
        'automationName': 'uiautomator2',
    }
    global ad, platformVersion
    platformVersion.append(desired_capabilities2["platformVersion"])
    ad = aw.Remote(command_executor2, desired_capabilities2)
    ad.implicitly_wait(options['page_wait'])
    yield ad
    ad.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    测试失败自动截图, 展示到 html 报告中
    :param item:
    :return:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:20%%;height:20%%;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot():
    """
    截图保存为base64，展示到html中
    """
    if options['device'] == 1:
        return wd.get_screenshot_as_base64()
    elif options['device'] == 2:
        # 读取设备版本号和运行的设备版本号对比，然后获取该设备的截图
        devices = subprocess.getoutput('adb devices')
        devices_list = re.findall(re.compile("\n(.+?)\t"), devices)
        for i in devices_list:
            if str(platformVersion[-1]) in \
                    str(subprocess.getoutput('adb -s {} shell getprop ro.build.version.release'.format(i))):
                os.system('adb -s {} shell screencap -p /sdcard/screen.png && adb -s {} pull /sdcard/screen.png report/'
                          .format(i, i))
                break
        with open("report/screen.png", "rb") as f:
            base64_Data = base64.b64encode(f.read())
        return base64_Data.decode()
    elif options['device'] == 3:
        return iosd.get_screenshot_as_base64()
    else:
        pass


# @pytest.fixture(scope="session", autouse=True)
# def env(request):
#     """
#     Parse env config info
#     """
#     root_dir = request.config.rootdir
#     config_path = '{0}/config/env_config.yml'.format(root_dir)
#     with open(config_path) as f:
#         env_config = yaml.load(f)  # 读取配置文件
#
#     allure.environment(host=env_config['host']['domain'])  # 测试报告中展示host
#     allure.environment(browser=env_config['host']['browser'])  # 测试报告中展示browser
#
#     return env_config
