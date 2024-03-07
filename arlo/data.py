#!/usr/bin/python
"""
Arlo firmware extractor
data
"""

class _Arlo():
    """ arlo models """
    # https://www.arlo.com/en-us/support/docs
    # https://kb.arlo.com/2160/What-do-I-need-to-know-about-Arlo-camera-firmware-updates
    # https://community.arlo.com/t5/Firmware-Release-Notes/Arlo-Firmware-Release-Table/td-p/1920885
    _MODELS = {
            "Cameras" : {
                "VMC3030":  {"name": "Arlo Wire-Free"},
                "VMC4030":  {"name": "Arlo Pro"},
                "VMC4030P": {"name": "Arlo Pro 2"},
                "VMC4040P": {"name": "Arlo Pro 3"},
                "VMC4050P": {"name": "Arlo Pro 4 (VMC4050P)"},
                "VMC4041P": {"name": "Arlo Pro 4 (VMC4041P)",
                             "config": {
                                    "uploading":[
                                        { "id": 2, "addr": 0x100a0000, },
                                        #{ "id": 3, "addr": 0x100a0000, },
                                    ],
                                    "liveview": [
                                        { "id":  4, "addr": 0x20000000,},
                                        { "id":  5, "addr": 0x20100000,},
                                    ],
                                    "upgrade": [
                                        { "id":  9, "addr": 0x10000000,},
                                        { "id": 10, "addr": 0x20000000,},
                                    ],
                                    #"setup": [
                                    #    { "id": 12, "addr": ,},
                                    #i   { "id": 13, "addr": ,},
                                    #],
                                    #"calfw": [
                                    #    { "id": 14, "addr": ,},
                                    #],
                                    "setupqr": [
                                        { "id": 15, "addr": 0x10000000,},
                                        { "id": 16, "addr": 0x20000000,},
                                    ],
                                    "ukn_20": [
                                        { "id": 20, "addr": 0x20000000,},
                                    ],
                                    "recovery": [
                                        { "id": 24, "addr": 0x10000000,},
                                    ],
                                    "arlogw": [
                                        { "id": 36, "addr": 0x20000000,},
                                        { "id": 37, "addr": 0x20100000,},
                                    ],
                                },
                            },
                "VMC4060P": {"name": "Arlo Pro 5S"},
                "VMC5040":  {"name": "Arlo Ultra / Ultra 2"},
                "VMC2050":  {"name": "Arlo Essential Outdoor 2nd Gen (VMC2050)"},
                "VMC3050":  {"name": "Arlo Essential Outdoor 2nd Gen (VMC3050)"},
                "VMC2052":  {"name": "Arlo Essential XL Outdoor 2nd Gen (VMC2052)"},
                "VMC3052":  {"name": "Arlo Essential XL Outdoor 2nd Gen (VMC3052)"},
                "VMC2020":  {"name": "Arlo Essential"},
                "VMC2030":  {"name": "Arlo Essential Spotlight"},
                "VMC2032":  {"name": "Arlo Essential XL Spotlight"},
                "VMC3040":  {"name": "Arlo Q"},
                "VMC3040S": {"name": "Arlo Q+"},
                "VMC2060":  {"name": "Arlo Essential Indoor 2nd Gen (VMC2060)"},
                "VMC3060":  {"name": "Arlo Essential Indoor 2nd Gen (VMC3060)"},
                "VMC2040":  {"name": "Arlo Essential Indoor"},
                "ABC1000":  {"name": "Arlo Baby"},
            },
            "Base_Station_SmartHub" : {
                "VMB3010": {"name": "Arlo Base Station (VMB3010)"},
                "VMB3500": {"name": "Arlo Base Station (VMB3500)"},
                "VMB4000": {"name": "Arlo Pro Base Station (VMB4000)"},
                "VMB4500": {"name": "Arlo Pro Base Station (VMB4500)"},
                "VMB4540": {"name": "Arlo Pro 3 SmartHub"},
                "VMB5000": {"name": "Arlo Ultra Smarthub"},
            },
            "Doorbells" : {
                "AVD3001": {"name": "Arlo Video Doorbell 2nd Gen (AVD3001)"},
                "AVD4001": {"name": "Arlo Video Doorbell 2nd Gen (AVD4001)"},
                "AVD1001": {"name": "Arlo Video Doorbell - Wired"},
                "AVD2001": {"name": "Arlo Video Doorbell Wire-Free"},
                "AAD1001": {"name": "Arlo Audio Doorbell"},
                "AC2001":  {"name": "Arlo Chime V2"},
                "AC1001":  {"name": "Arlo Chime"},
            },
            "Floodlights" : {
                "FB1001":  {"name": "Arlo Pro 3 Floodlight"},
                "ABB1000": {"name": "Arlo Security Light"},
            },
            "Arlo_Home_Security_System" : {
                "SH1001":  {"name": "Arlo Keypad Hub"},
                "SLB1001": {"name": "Arlo Siren"},
                "MS1001":  {"name": "Arlo All-in-One Sensor"},
                "ASB1001": {"name": "Arlo Safe Button"},
            },
        # Devices
        #"VMC5042": {"name": "Arlo Ultra / Ultra 2 XL"},
        #"VMC4052P": {"name": "Arlo Pro 4 XL Spotlight"},
        #"VML2030": {"name": "Arlo Go 2"},
        #"VML4030": {"name": "Arlo Go"},
        #"AL1101": {"name": "Arlo Security Light"},
        # Accessories
        #"LBB1001": {"name": "Arlo Home Security System Battery Backup"},
        #"VMA4400": {"name": "Arlo Pro Rechargeable Battery"},
        #"VMA4410": {"name": "Arlo Go Rechargeable Battery"},
        #"VMA5410": {"name": "XL Rechargeable Battery"},
        #"VMA4400C": {"name": "Charging Station"},
        #"VMA5400C": {"name": "Arlo Dual Charger"},
        #"VMA2400": {"name": "Arlo Doorbell Wire-Free Battery Charger"},
        #"VMA5600": {"name": "Arlo Magnetic Solar Panel"},
        #"VMA4600": {"name": "Arlo Solar Panel"},
        #"VMA3600": {"name": "Arlo Essential Solar Panel"},
        #"VMA5100": {"name": "Total Security Mount"},
        #"VMA4500": {"name": "Quadpod"},
        #"VMA4000": {"name": "Outdoor Camera Mount"},
        #"VMA1100": {"name": "Ceiling Mount"},
        #"VMA1000": {"name": "Adjustable Mount"},
        #"FBA1001": {"name": "Arlo Pro3 Ultra Ceiling Adapter"},
        #"ABA1500": {"name": "Arlo Baby Table/Wall Stand"},
        #"VMA4800": {"name": "Indoor Power Cable and Adapter"},
        #"VMA4900": {"name": "Outdoor Power Cable and Adapter"},
        #"VMA4900": {"name": "Arlo Go Outdoor Power Adapter"},
        #"ABB1000": {"name": "Arlo Bridge"}, # ??? Floodlights
        #"VNB4000": {"name": "Arlo FlexPower Base Station"},
        #"AYS1000": {"name": "Arlo Security Sign"},
        #"VMB3000": {"name": "VMB3000"},
    }

    _ENV_DEV        = ['dev', 'qa', 'goldenft']
    _BASE_URL_DEV   = 'http://arloupdates.arlo.com/arlo/fw/fw_deployed/{env}/'

    _ENV            = ['staging', 'fieldtrial', 'production']
    _BASE_URL       = 'http://updates.arlo.com/arlo/fw/fw_deployed/{env}/'

    _JSON_URL       = 'updaterules/{model}_UpdateRules.json'

    @property
    def models(self):
        """ get all models info """
        return self._MODELS

    def model(self, key, name):
        """ get info for model """
        return self.models[key][name]

    def device_types(self):
        """ get all types """
        return self.models.keys()

    def find_model(self, name):
        """ find info for model """
        for key in self.device_types():
            if name in self.models[key]:
                return (key, name)
        return (None, None)

    def list_models(self, key=None):
        """ return models ids & names """
        if key is not None:
            for cid in self.models[key]:
                yield (cid, self.models[key][cid]["name"])
        else:
            # pylint: disable=redefined-argument-from-local
            for key in self.device_types():
                for cid in self.models[key]:
                    yield (cid, self.models[key][cid]["name"])

    def base_url(self, env='production'):
        """ get base update url """
        if env in self._ENV:
            return self._BASE_URL.format(env=env)
        if env in self._ENV_DEV:
            return self._BASE_URL_DEV.format(env=env)
        return None

    def json_url(self, model, env='production'):
        """ get json update info url for model """
        return self.base_url(env) + self._JSON_URL.format(model=model)

Arlo = _Arlo()
