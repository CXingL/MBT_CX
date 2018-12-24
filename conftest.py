# coding=utf-8
import test_main
import pytest
import os
import re
from appium import webdriver as aw
from selenium import webdriver as sw

# import allure
# import yaml
options = test_main.TestClass().options

"""
Web Selenium
"""
# 启动浏览器前设置一些参数
images = options["has_images"]
chrome_opt = sw.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": images}
chrome_opt.add_experimental_option("prefs", prefs)


@pytest.fixture(scope='function')
def WD():
    global wd
    # 启动 Chrome 浏览器进行测试, 并设置最大等待时间
    wd = sw.Chrome(chrome_options=chrome_opt)
    wd.implicitly_wait(options["page_wait"])
    yield wd
    wd.quit()


"""
Android Appium
"""
# 测试的包的路径和包名
appLocation = options["appLocation"]
# 读取设备系统版本号
deviceAndroidVersion = list(os.popen('adb shell getprop ro.build.version.release').readlines())
deviceVersion = re.findall(r'^\w*\b', deviceAndroidVersion[0])[0]
# 读取 APK 的 package 信息
appPackageAdb = list(os.popen('aapt dump badging ' + appLocation).readlines())
appPackage = re.findall(r'\'com\w*.*?\'', appPackageAdb[0])[0]
# 删除以前的安装包
try:
    os.system('adb uninstall ' + appPackage)
except:
    pass

command_executor = 'http://localhost:4723/wd/hub'
desired_capabilities = {
    'platformName': 'Android',
    'platformVersion': deviceVersion,
    'deviceName': 'Android',
    'appPackage': appPackage,
    'appWaitPackage': appPackage,
    'app': appLocation,
    'appActivity': ".activity.authentication.SplashActivity",
    # 'noReset': True,
    'automationName': 'uiautomator2',
}


@pytest.fixture(scope='function')
def AD():
    global ad
    # 删除以前的安装包
    try:
        os.system('adb uninstall ' + appPackage)
    except:
        pass
    ad = aw.Remote(command_executor, desired_capabilities)
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
    # if options['device'] == 1:
    return wd.get_screenshot_as_base64()
    # elif options['device'] == 2:
    #     return ad.get_screenshot_as_base64()
    # else:
    #     pass


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
