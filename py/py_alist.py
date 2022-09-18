# coding=utf-8
# !/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import re

class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "Alist"

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "七米蓝": "https://al.chirmyram.com",
            "姬路白雪の资源小站": "https://pan.jlbx.xyz"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
				"type_flag": "1",
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        result = {
            'list': []
        }
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        num = tid.count('/')
        if num ==2:
            tid = tid + '/'
        url = re.findall(r"http.*://.*?/", tid)[0]
        pat = tid.replace(url,"")
        ifver = 'ver' in locals().keys()
        if ifver is False:
            param = {
                "path": '/'
            }
            ver = self.fetch(url + 'api/public/settings', param)
            vjo = json.loads(ver.text)['data']
            if type(vjo) is dict:
                ver = 3
            else:
                ver = 2
        param = {
            "path": '/' + pat
        }
        if ver == 2:
            rsp = self.postJson(url + 'api/public/path', param)
            jo = json.loads(rsp.text)
            vodList = jo['data']['files']
        else:
            rsp = self.postJson(url + 'api/fs/list', param)
            jo = json.loads(rsp.text)
            vodList = jo['data']['content']
        videos = []
        for vod in vodList:
            if ver == 2:
                img = vod['thumbnail']
            else:
                img = vod['thumb']
            if len(img) == 0:
                if vod['type'] == 1:
                    img = "http://img1.3png.com/281e284a670865a71d91515866552b5f172b.png"
            if pat != '':
                aid = pat + '/'
            else:
                aid = pat
            tag = "file"
            remark = "文件"
            if vod['type'] == 1:
                tag = "folder"
                remark = "文件夹"
            aid = url + aid + vod['name']
            videos.append({
                "vod_id":  aid,
                "vod_name": vod['name'],
                "vod_pic": img,
                "vod_tag": tag,
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = 1
        result['pagecount'] = 1
        result['limit'] = 999
        result['total'] = 999999
        return result

    def detailContent(self, array):
        id = array[0]
        url = re.findall(r"http.*://.*?/", id)[0]
        ifver = 'ver' in locals().keys()
        if ifver is False:
            param = {
                "path": '/'
            }
            ver = self.fetch(url + 'api/public/settings', param)
            vjo = json.loads(ver.text)['data']
            if type(vjo) is dict:
                ver = 3
            else:
                ver = 2
        fileName = id.replace(url, "")
        param = {
            "path": '/' + fileName,
            "password": "",
            "page_num": 1,
            "page_size": 100
        }
        if ver == 2:
            rsp = self.postJson(url + 'api/public/path', param)
            jo = json.loads(rsp.text)
            vodList = jo['data']['files'][0]
        else:
            rsp = self.postJson(url + 'api/fs/get', param)
            jo = json.loads(rsp.text)
            vodList = jo['data']
        if ver == 2:
            url = vodList['url']
            pic = vodList['thumbnail']
        else:
            url = vodList['raw_url']
            pic = vodList['thumb']
        vId = url + fileName
        name = vodList['name']
        tag = "file"
        if vodList['type'] == 1:
            tag = "folder"
        vod = {
            "vod_id": vId,
            "vod_name": name,
            "vod_pic": pic,
            "vod_tag": tag,
            "vod_play_from": "播放",
            "vod_play_url": name + '$' + url
        }
        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        result = {
            'list': []
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        url = id
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        return result

    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]