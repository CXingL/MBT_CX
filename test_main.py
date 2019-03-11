# coding=utf-8
import MBT_base
import pytest
import os


class TestClass:
    # 默认配置
    path = os.path.abspath('')
    options = {
        "file": "example",  # 可以为多个, 用逗号隔开
        "end_condition": "'\"weighted_random(edge_coverage(100))\"'",
        # 结束条件, 覆盖所有的路径: '"weighted_random(edge_coverage(100))"'
        # 到达某个顶点结束: '"weighted_random(reached_vertex(v_sureEdit))"'
        # 执行动作达到次数结束: '"weighted_random(length(200))"'
        "page_wait": 10,  # 页面加载最大等待时间，单位s
        # "script": "page_script",
        "device": 1,  # [1: Web, 2: Android, 3: iOS] 影响失败截图
        "speed": 1,  # 每个动作的间隔时间, 单位 s

        # Web 设置
        "browser": 1,  # [1: Chrome, 2: Safari, 3: Firefox, 4: IE11, 5: browserstack]
        "has_images": 1,  # 页面是否要加载图片, 1 为加载, 2 为不加载

        # Android 设置
        "appLocation": "example.apk",

        # ios 设置
        "bundleId": "com.Monstarbukka.cn",
        "platformVersion": "10.1",
    }
    # # 可以传参，依次执行
    # @pytest.fixture(params=["NO", "PT", "SE"])
    # def eu_country(self, request):
    #     return request.param
    #
    # # @pytest.mark.skip("nothing")
    # def test_Example_EU(self, android, eu_country):
    #     self.options['file'] = 'Example_EU'
    #     self.options['device'] = 2
    #     MBT_base.runs(self.options, android, e_EUselectCountry=eu_country)

    # @pytest.mark.skip("nothing")
    def test_example(self, web):
        self.options['file'] = 'example'
        self.options['device'] = 1
        MBT_base.runs(self.options, web)
