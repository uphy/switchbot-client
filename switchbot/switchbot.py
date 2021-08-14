import requests
import os


class Device:

    def __init__(self, device_id: str, device_name: str, device_type: str):
        self._device_id = device_id
        self._device_name = device_name
        self._device_type = device_type

    @property
    def device_id(self):
        return self.device_id

    @property
    def device_name(self):
        return self.device_name

    @property
    def device_type(self):
        return self.device_type

class DeviceList:

    def __init__(self, device_list:list[Device], infrared_remote_list:list[Device]):
        self._device_list = device_list
        self._infrared_remote_list = infrared_remote_list
    
    @property
    def device_list(self):
        return self._device_list
    
    @property
    def infrared_remote_list(self):
        return self._infrared_remote_list

class SwitchBotClient:

    def __init__(self, token: str):
        self.token = token

    def devices(self):
        res = self._request("GET", "devices")
        device_list = res["deviceList"]
        infrared_remote_list = res["infraredRemoteList"]
        map(lambda d: Device(d["deviceId"],
            d["deviceName"], d["deviceType"]), device_list)
        map(lambda d: Device(d["deviceId"],
            d["deviceName"], d["deviceType"]), infrared_remote_list)
        return DeviceList(device_list, infrared_remote_list)

    def status(self, device_id: str):
        return self._request("GET", "devices/%s/status" % (device_id))

    def command(self, device_id: str, command: str, parameter: str, commandType="command"):
        return self._request("POST", "devices/%s/commands" % (device_id), body={
            "command": command,
            "parameter": parameter,
            "commandType": commandType
        })

    def _request(self, method: str, path: str, body=None):
        res = requests.request(
            method, "https://api.switch-bot.com/v1.0/"+path, headers={
                "Authorization": self.token
            }, json=body).json()
        statusCode = res["statusCode"]
        if statusCode == 100:
            return res["body"]
        else:
            raise Exception(res)
