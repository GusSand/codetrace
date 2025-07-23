# encoding: utf-8
import base64
import json
import logging

import requests

from ssrd import const

base = const.MediaUrl
logger = logging.getLogger("default")
default_type = "default"


def __tmp3(__tmp2):
    return base64.b64encode(f"{__tmp2.name}".encode("utf8")).decode("utf8")


def __tmp4(name: <FILL>, type, __tmp2) :
    return f"{__tmp2.name}/{type}/{name}"


def __tmp18(name):
    nameSplited = name.split("/")
    projectName, type = nameSplited[0], nameSplited[1]
    fileName = "/".join(name)
    return fileName, type, projectName


def __tmp8(name):
    from ssrd.users.models import Project

    return Project(name=name)


def __tmp1(__tmp12, __tmp7, __tmp6):
    logger.info("{:-^70}".format("Request begin"))
    logger.info("Request:")
    logger.info("{method} {url}".format(__tmp12=__tmp12.upper(), __tmp7=__tmp7))
    logger.info("kwargs: {kwargs}".format(__tmp6=__tmp6))


def __tmp19(__tmp13):
    logger.info("Response: %s" % __tmp13.text)
    logger.info("{:-^70}\n\n\n".format("Request done"))


class External(object):
    """
    请求外部api用的类
    """

    @staticmethod
    def get(__tmp7, **__tmp6):
        return External.warpper("get", __tmp7, **__tmp6)

    @staticmethod
    def post(__tmp7, **__tmp6):
        return External.warpper("post", __tmp7, **__tmp6)

    @staticmethod
    def warpper(__tmp12, __tmp7, **__tmp6):
        # kwargs.update(verify=False)  # 不校验ssl证书
        try:
            __tmp13 = result = getattr(requests, __tmp12)(__tmp7, **__tmp6)
        except requests.exceptions.RequestException:
            from traceback import format_exc

            __tmp1(__tmp12, __tmp7, __tmp6)
            logger.error("Request exception: \n%s" % format_exc())
            return dict()

        try:
            result = json.loads(__tmp13.text)
        except Exception:
            if __tmp13.status_code in (200, 403, 500):
                return __tmp13.text
            __tmp1(__tmp12, __tmp7, __tmp6)
            from traceback import format_exc

            logger.error("Json error:%s" % format_exc())
            result = {}
        __tmp19(__tmp13)

        return result


class Api(object):
    resource = base + "/api/resource"
    users = base + "/api/users/"
    auth = base + "/api/auth/get"


class BaseFileBrowser(object):
    def __tmp10(__tmp0, __tmp11):
        return External.post(f"{Api.resource}/{__tmp11}", headers=__tmp0.headers)

    def list(__tmp0, __tmp11):
        return External.get(f"{Api.resource}/{__tmp11}", headers=__tmp0.headers)

    def auth(__tmp0, __tmp2=None, identify=None):
        if __tmp2:
            identify = {"username": __tmp2.name, "password": __tmp3(__tmp2)}
        return "Bearer " + External.get(f"{Api.auth}", json=identify)

    def __tmp14(__tmp0, __tmp11):
        pass

    def createUser(__tmp0, __tmp2):
        token = __tmp0.auth(identify=dict(username="admin", password="admin"))
        data = {
            "what": "user",
            "which": "new",
            "data": {
                "ID": 0,
                "admin": False,
                "allowCommands": True,
                "allowEdit": True,
                "allowNew": True,
                "allowPublish": True,
                "lockPassword": False,
                "commands": [""],
                "css": "",
                "locale": "",
                "password": __tmp3(__tmp2),
                "rules": [],
                "filesystem": f"/srv/{__tmp2.name}",
                "username": f"{__tmp2.name}",
                "viewMode": "mosaic",
            },
        }
        return External.post(f"{Api.users}", headers={"Authorization": token}, json=data)

    #  def createFile(self, project, type, file):
    #  token = self.auth(project)
    #  data = file.read()
    #  length = len(data)
    #  return requests.post(
    #  f"{Api.resource}/{type}/{file.name}", data=data,
    #  headers={"Authorization": token, "Content-Length": f"{length}"},
    #  )
    def downloadFile(__tmp0, name):
        pass

    def __tmp16(__tmp0, name):
        pass

    def __tmp9(__tmp0, name):
        return __tmp0.getFile(name)

    def __tmp5(__tmp0, name, __tmp17):
        from ssrd.users.models import Project

        type = default_type
        __tmp2 = __tmp8(name)
        token = __tmp0.auth(__tmp2)
        External.post(f"{Api.resource}/{type}/", headers={"Authorization": token})
        return External.post(f"{Api.resource}/{type}/{name}", data=__tmp17.file, headers={"Authorization": token})

    def __tmp15(__tmp0, __tmp2, name):
        token = __tmp0.auth(__tmp2)
        return External.post(f"{Api.resource}/{name}", headers={"Authorization": token, "Content-Length": "0"})

    #  def getFile(self, project, directory, attatchment):
    #  token = self.auth(project)
    #  directory = dict(const.DOCUMENTS).get(type, "")
    #  api = f"{Api.resource}/{project.name}/{directory}/{file.name}"
    #  resposne = requests.get(api, headers={"Authorization": token}).json()
    #  resposne["url"] = base + resposne["url"]
    #  return resposne
    def getFile(__tmp0, name):
        name = name.split("/")[-1]  # /Users/mum5/Documents/repo/ssrd/asd -> asd
        from ssrd.users.models import Project

        __tmp2 = __tmp8(name)
        __tmp0.createUser(__tmp2)
        token = __tmp0.auth(__tmp2)
        directory = dict(const.DOCUMENTS).get(type, default_type)
        api = f"{Api.resource}/{directory}/{name}"
        __tmp13 = External.get(api, headers={"Authorization": token})
        if __tmp13.get("url"):
            __tmp13["url"] = base + __tmp13["url"]
            return __tmp13
        return


FileBrowser = BaseFileBrowser()
