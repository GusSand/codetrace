# encoding: utf-8
import base64
import json
import logging

import requests

from ssrd import const

base = const.MediaUrl
logger = logging.getLogger("default")
default_type = "default"


def get_password(__tmp3):
    return base64.b64encode(f"{__tmp3.name}".encode("utf8")).decode("utf8")


def __tmp0(name, type: <FILL>, __tmp3) :
    return f"{__tmp3.name}/{type}/{name}"


def destruct_name(name):
    nameSplited = name.split("/")
    projectName, type = nameSplited[0], nameSplited[1]
    fileName = "/".join(name)
    return fileName, type, projectName


def get_project(name):
    from ssrd.users.models import Project

    return Project(name=name)


def log_request(method, url, kwargs):
    logger.info("{:-^70}".format("Request begin"))
    logger.info("Request:")
    logger.info("{method} {url}".format(method=method.upper(), url=url))
    logger.info("kwargs: {kwargs}".format(kwargs=kwargs))


def log_response(response):
    logger.info("Response: %s" % response.text)
    logger.info("{:-^70}\n\n\n".format("Request done"))


class External(object):
    """
    请求外部api用的类
    """

    @staticmethod
    def get(url, **kwargs):
        return External.warpper("get", url, **kwargs)

    @staticmethod
    def post(url, **kwargs):
        return External.warpper("post", url, **kwargs)

    @staticmethod
    def warpper(method, url, **kwargs):
        # kwargs.update(verify=False)  # 不校验ssl证书
        try:
            response = result = getattr(requests, method)(url, **kwargs)
        except requests.exceptions.RequestException:
            from traceback import format_exc

            log_request(method, url, kwargs)
            logger.error("Request exception: \n%s" % format_exc())
            return dict()

        try:
            result = json.loads(response.text)
        except Exception:
            if response.status_code in (200, 403, 500):
                return response.text
            log_request(method, url, kwargs)
            from traceback import format_exc

            logger.error("Json error:%s" % format_exc())
            result = {}
        log_response(response)

        return result


class __typ0(object):
    resource = base + "/api/resource"
    users = base + "/api/users/"
    auth = base + "/api/auth/get"


class BaseFileBrowser(object):
    def create(__tmp1, __tmp2):
        return External.post(f"{__typ0.resource}/{__tmp2}", headers=__tmp1.headers)

    def list(__tmp1, __tmp2):
        return External.get(f"{__typ0.resource}/{__tmp2}", headers=__tmp1.headers)

    def auth(__tmp1, __tmp3=None, identify=None):
        if __tmp3:
            identify = {"username": __tmp3.name, "password": get_password(__tmp3)}
        return "Bearer " + External.get(f"{__typ0.auth}", json=identify)

    def deleteFile(__tmp1, __tmp2):
        pass

    def createUser(__tmp1, __tmp3):
        token = __tmp1.auth(identify=dict(username="admin", password="admin"))
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
                "password": get_password(__tmp3),
                "rules": [],
                "filesystem": f"/srv/{__tmp3.name}",
                "username": f"{__tmp3.name}",
                "viewMode": "mosaic",
            },
        }
        return External.post(f"{__typ0.users}", headers={"Authorization": token}, json=data)

    #  def createFile(self, project, type, file):
    #  token = self.auth(project)
    #  data = file.read()
    #  length = len(data)
    #  return requests.post(
    #  f"{Api.resource}/{type}/{file.name}", data=data,
    #  headers={"Authorization": token, "Content-Length": f"{length}"},
    #  )
    def downloadFile(__tmp1, name):
        pass

    def getFileUrl(__tmp1, name):
        pass

    def getFileMeta(__tmp1, name):
        return __tmp1.getFile(name)

    def createFile(__tmp1, name, __tmp4):
        from ssrd.users.models import Project

        type = default_type
        __tmp3 = get_project(name)
        token = __tmp1.auth(__tmp3)
        External.post(f"{__typ0.resource}/{type}/", headers={"Authorization": token})
        return External.post(f"{__typ0.resource}/{type}/{name}", data=__tmp4.file, headers={"Authorization": token})

    def createDirectory(__tmp1, __tmp3, name):
        token = __tmp1.auth(__tmp3)
        return External.post(f"{__typ0.resource}/{name}", headers={"Authorization": token, "Content-Length": "0"})

    #  def getFile(self, project, directory, attatchment):
    #  token = self.auth(project)
    #  directory = dict(const.DOCUMENTS).get(type, "")
    #  api = f"{Api.resource}/{project.name}/{directory}/{file.name}"
    #  resposne = requests.get(api, headers={"Authorization": token}).json()
    #  resposne["url"] = base + resposne["url"]
    #  return resposne
    def getFile(__tmp1, name):
        name = name.split("/")[-1]  # /Users/mum5/Documents/repo/ssrd/asd -> asd
        from ssrd.users.models import Project

        __tmp3 = get_project(name)
        __tmp1.createUser(__tmp3)
        token = __tmp1.auth(__tmp3)
        directory = dict(const.DOCUMENTS).get(type, default_type)
        api = f"{__typ0.resource}/{directory}/{name}"
        response = External.get(api, headers={"Authorization": token})
        if response.get("url"):
            response["url"] = base + response["url"]
            return response
        return


FileBrowser = BaseFileBrowser()
