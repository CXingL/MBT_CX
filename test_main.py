# coding=utf-8
import MBT_base
import pytest


class TestClass:
    # 默认配置
    options = {
        "file": "",  # 可以为多个
        "end_condition": "'\"weighted_random(edge_coverage(100))\"'",
        # 结束条件, 覆盖所有的路径: '"weighted_random(edge_coverage(100))"'
        # 到达某个顶点结束: '"weighted_random(reached_vertex(v_sureEdit))"'
        # 执行动作达到次数结束: '"weighted_random(length(200))"'
        "page_wait": 20,  # 页面加载最大等待时间，单位s
        "script": "page_script",
        "device": 1, # [1: Web, 2: Android, 3: Ios] 影响失败截图

        # Web 设置
        "speed": 0,  # 每个动作的间隔时间, 单位 s
        "has_images": 1,  # 页面是否要加载图片, 1 为加载, 2 为不加载

        # Android 设置
        "appLocation": "/Users/annesui/Downloads/REVINYL_debug_329_1.0.15.647.apk",
    }

    # @pytest.mark.skip("nothing")
    def test_example_android(self, AD):
        self.options['file'] = "AndroidExample"
        MBT_base.runs(self.options, AD)


    # @pytest.mark.skip("nothing")
    def test_example_web(self, WD):
        self.options['file'] = "WebExample"
        MBT_base.runs(self.options, WD)
