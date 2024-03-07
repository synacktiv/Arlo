# Arlo

Extract executable binaries from Arlo dump & updates

See blogpost at https://www.synacktiv.com/publications/arlo-im-watching-you

## Parser

`arlo.py` is used to parse a Flash memory dump, download and parse updates or
list knwon models. It requires `cryptography`, `asn1crypto` and `requests` pip
packages and optinally uses `fastcrc` package.

### Known models

```
$ arlo.py list
- Cameras
  - VMC3030 : Arlo Wire-Free
  - VMC4030 : Arlo Pro
  - VMC4030P: Arlo Pro 2
  - VMC4040P: Arlo Pro 3
  - VMC4050P: Arlo Pro 4 (VMC4050P)
  - VMC4041P: Arlo Pro 4 (VMC4041P)
  - VMC4060P: Arlo Pro 5S
  - VMC5040 : Arlo Ultra / Ultra 2
  - VMC2050 : Arlo Essential Outdoor 2nd Gen (VMC2050)
  - VMC3050 : Arlo Essential Outdoor 2nd Gen (VMC3050)
  - VMC2052 : Arlo Essential XL Outdoor 2nd Gen (VMC2052)
  - VMC3052 : Arlo Essential XL Outdoor 2nd Gen (VMC3052)
  - VMC2020 : Arlo Essential
  - VMC2030 : Arlo Essential Spotlight
  - VMC2032 : Arlo Essential XL Spotlight
  - VMC3040 : Arlo Q
  - VMC3040S: Arlo Q+
  - VMC2060 : Arlo Essential Indoor 2nd Gen (VMC2060)
  - VMC3060 : Arlo Essential Indoor 2nd Gen (VMC3060)
  - VMC2040 : Arlo Essential Indoor
  - ABC1000 : Arlo Baby
- Base_Station_SmartHub
  - VMB3010 : Arlo Base Station (VMB3010)
  - VMB3500 : Arlo Base Station (VMB3500)
  - VMB4000 : Arlo Pro Base Station (VMB4000)
  - VMB4500 : Arlo Pro Base Station (VMB4500)
  - VMB4540 : Arlo Pro 3 SmartHub
  - VMB5000 : Arlo Ultra Smarthub
- Doorbells
  - AVD3001 : Arlo Video Doorbell 2nd Gen (AVD3001)
  - AVD4001 : Arlo Video Doorbell 2nd Gen (AVD4001)
  - AVD1001 : Arlo Video Doorbell - Wired
  - AVD2001 : Arlo Video Doorbell Wire-Free
  - AAD1001 : Arlo Audio Doorbell
  - AC2001  : Arlo Chime V2
  - AC1001  : Arlo Chime
- Floodlights
  - FB1001  : Arlo Pro 3 Floodlight
  - ABB1000 : Arlo Security Light
- Arlo_Home_Security_System
  - SH1001  : Arlo Keypad Hub
  - SLB1001 : Arlo Siren
  - MS1001  : Arlo All-in-One Sensor
  - ASB1001 : Arlo Safe Button
```

### Usage

```
usage: arlo.py [-h] [-d [PREFIX]]
               [-m [{VMC3030,VMC4030,VMC4030P,VMC4040P,VMC4050P,VMC4041P,VMC4060P,VMC5040,VMC2050,VMC3050,VMC2052,VMC3052,VMC2020,VMC2030,VMC2032,VMC3040,VMC3040S,VMC2060,VMC3060,VMC2040,ABC1000,VMB3010,VMB3500,VMB4000,VMB4500,VMB4540,VMB5000,AVD3001,AVD4001,AVD1001,AVD2001,AAD1001,AC2001,AC1001,FB1001,ABB1000,SH1001,SLB1001,MS1001,ASB1001}]]
               {update,parse,list} ...

options:
  -h, --help            show this help message and exit
  -d [PREFIX]           folder where files will be written
  -m [{VMC3030,VMC4030,VMC4030P,VMC4040P,VMC4050P,VMC4041P,VMC4060P,VMC5040,VMC2050,VMC3050,VMC2052,VMC3052,VMC2020,VMC2030,VMC2032,VMC3040,VMC3040S,VMC2060,VMC3060,VMC2040,ABC1000,VMB3010,VMB3500,VMB4000,VMB4500,VMB4540,VMB5000,AVD3001,AVD4001,AVD1001,AVD2001,AAD1001,AC2001,AC1001,FB1001,ABB1000,SH1001,SLB1001,MS1001,ASB1001}]
                        Treat file as this model dump. See list command

commands:
  valid commands

  {update,parse,list}   commands specific help
    update              update help
    parse               parse help
    list                list help
```

### Output

```
- Cameras
  - Arlo Wire-Free
    - NTGR_1.5.295_WiFi_upgrade.bin.enc                       cimg: v1, 2021-08-31T21:07:27 / part: kernel, encrypted / OVTW: (v1.5.295)
  - Arlo Pro
    - VMC4030_1.092.1.0_9_120d8b7.bin.enc                     cimg: v1, 2021-08-25T07:36:52 / part: kernel, encrypted
  - Arlo Pro 2
    - VMC4030P_1.125.17.1_11_de8490d.bin.enc                  cimg: v1, 2021-09-04T01:39:52 / part: kernel, encrypted
  - Arlo Pro 3
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC4040P_UpdateRules.json HTTP 404
  - Arlo Pro 4 (VMC4050P)
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC4050P_UpdateRules.json HTTP 404
  - Arlo Pro 4 (VMC4041P)
    - VMC4041P_1.080.20.1_23_d50a19d.bin.enc                  cimg: v1, 2023-08-08T00:27:03 / part: kernel, encrypted
  - Arlo Pro 5S
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC4060P_UpdateRules.json HTTP 404
  - Arlo Ultra / Ultra 2
    - VMC5040_1.070.52.1_35_1bdb65f.bin.enc                   cimg: v1, 2021-09-04T01:44:14 / part: kernel, encrypted
  - Arlo Essential Outdoor 2nd Gen (VMC2050)
    - VMC2050-1.2.2_512_9955b13.prod-pd.enc                   cimg: v2, 2023-10-24T01:10:44, (VMC2050), signature unsupported, decryption unsupported / part: kernel, encrypted
    - VMC2050-1.2.2_512_9955b13.prod-pp.enc                   cimg: v2, 2023-10-24T02:22:05, (VMC2050), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Essential Outdoor 2nd Gen (VMC3050)
    - VMC3050-1.2.2_512_9955b13.prod-pd.enc                   cimg: v2, 2023-10-24T01:14:26, (VMC3050), signature unsupported, decryption unsupported / part: kernel, encrypted
    - VMC3050-1.2.2_512_9955b13.prod-pp.enc                   cimg: v2, 2023-10-24T02:21:55, (VMC3050), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Essential XL Outdoor 2nd Gen (VMC2052)
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC2052_UpdateRules.json HTTP 404
  - Arlo Essential XL Outdoor 2nd Gen (VMC3052)
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC3052_UpdateRules.json HTTP 404
  - Arlo Essential
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/VMC2020/VMC2020_1.090.33.0_28_449310d.bin.enc HTTP 404
  - Arlo Essential Spotlight
    - VMC2030_1.090.32.1_55_07e3402.bin.enc                   cimg: v1, 2023-08-03T03:21:49 / part: kernel, encrypted / BTVO: long
  - Arlo Essential XL Spotlight
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC2032_UpdateRules.json HTTP 404
  - Arlo Q
    - VMC3040-1.7.4_5517.prod.upgrade                         cimg: v1, 2016-04-02T02:06:03 / part: rootfs, compressed+encrypted, zlib, unknown magic b'\x00\x90\x0f\xe1' / part: generic, encrypted, SquashFS
    - VMC3040-1.13.0.0_95_a58d08a_db3500e.prod.upgrade        cimg: v1, 2023-03-14T06:47:10 / part: rootfs, compressed+encrypted, zlib, unknown magic b'\x00\x90\x0f\xe1' / part: generic, encrypted, SquashFS
  - Arlo Q+
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/VMC3040S_UpdateRules.json HTTP 404
  - Arlo Essential Indoor 2nd Gen (VMC2060)
    - VMC2060-1.2.2_515_b1ea04e.prod-pd.enc                   cimg: v2, 2023-11-07T18:02:16, (VMC2060), signature unsupported, decryption unsupported / part: kernel, encrypted
    - VMC2060-1.2.2_515_b1ea04e.prod-pp.enc                   cimg: v2, 2023-11-07T18:33:54, (VMC2060), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Essential Indoor 2nd Gen (VMC3060)
    - VMC3060-1.2.2_515_b1ea04e.prod-pd.enc                   cimg: v2, 2023-11-07T18:05:58, (VMC3060), signature unsupported, decryption unsupported / part: kernel, encrypted
    - VMC3060-1.2.2_515_b1ea04e.prod-pp.enc                   cimg: v2, 2023-11-07T18:34:01, (VMC3060), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Essential Indoor
    - VMC2040_OTA-1.19.0.0_1182_900c0a4_d2776d0.prod.enc      cimg: v1, 2023-09-26T17:27:15 / part: kernel, encrypted, SquashFS
    - VMC2040_OTA-1.19.0.0_1182_900c0a4_d2776d0.prod.sig.enc  cimg: v1, 2023-09-26T17:27:15 / part: kernel, encrypted, SquashFS
  - Arlo Baby
    - ABC1000-1.14.0.0_124_a58d08a_b7792aa.prod.upgrade       cimg: v1, 2023-03-14T06:27:36 / part: rootfs, compressed+encrypted, zlib, unknown magic b'\xf6)\x00\xeb' / part: generic, encrypted, SquashFS
- Base_Station_SmartHub
  - Arlo Base Station (VMB3010)
    - VMB3010-1.21.0.2_1540_8a519c8.prod.chk.enc              cimg: v1, 2023-05-20T08:43:18 / part: kernel, encrypted, NETGEARHDR0
  - Arlo Base Station (VMB3500)
    - VMB3500-1.21.0.2_1296_8a519c8.prod.upgrade              cimg: v1, 2023-05-20T08:57:59 / part: rootfs, compressed+encrypted, zlib, unknown magic b"'\x05\x19V" / part: generic, encrypted, UBI
  - Arlo Pro Base Station (VMB4000)
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/VMB4000/VMB4000-1.23.0.0_4353_f8a2b18.prod.chk.enc HTTP 404
  - Arlo Pro Base Station (VMB4500)
    - VMB4500-1.21.1.0_4167_9611cf3.prod.upgrade              cimg: v1, 2023-06-16T08:05:18 / part: rootfs, compressed+encrypted, zlib, unknown magic b"'\x05\x19V" / part: generic, encrypted, UBI
  - Arlo Pro 3 SmartHub
    - VMB4540-1.21.1.0_1399_9611cf3.prod.upgrade              cimg: v1, 2023-06-16T09:39:26 / part: rootfs, compressed+encrypted, zlib, unknown magic b"'\x05\x19V" / part: generic, encrypted, UBI
  - Arlo Ultra Smarthub
    - VMB5000-1.21.1.0_1431_9611cf3.prod.upgrade.enc          cimg: v1, 2023-06-16T12:38:58 / part: kernel, encrypted, pkgtb
- Doorbells
  - Arlo Video Doorbell 2nd Gen (AVD3001)
    - AVD3001-1.2.1_435_abb9732.prod-pd.enc                   cimg: v2, 2023-10-18T23:54:56, (AVD3001), signature unsupported, decryption unsupported / part: kernel, encrypted
    - AVD3001-1.2.1_435_abb9732.prod-pp.enc                   cimg: v2, 2023-10-19T02:13:43, (AVD3001), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Video Doorbell 2nd Gen (AVD4001)
    - AVD4001-1.2.1_435_abb9732.prod-pd.enc                   cimg: v2, 2023-10-19T00:00:14, (AVD4001), signature unsupported, decryption unsupported / part: kernel, encrypted
    - AVD4001-1.2.1_435_abb9732.prod-pp.enc                   cimg: v2, 2023-10-19T01:37:06, (AVD4001), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Video Doorbell - Wired
    - AVD1001_OTA-1.19.0.0_3_098d492_3567407.prod.enc         cimg: v1, 2023-09-13T20:01:39 / part: kernel, encrypted, SquashFS
    - AVD1001_OTA-1.19.0.0_3_098d492_3567407.prod.sig.enc     cimg: v1, 2023-09-13T20:01:39 / part: kernel, encrypted, SquashFS
  - Arlo Video Doorbell Wire-Free
    - AVD2001_OTA1-1.8.0.0_4_4a16fed_758744c.prod.enc         cimg: v1, 2023-10-27T16:00:51 / part: kernel, encrypted, SquashFS
    - AVD2001_OTA2-1.8.0.0_4_4a16fed_758744c.prod.enc         cimg: v1, 2023-10-27T16:00:51 / part: kernel, encrypted, SquashFS
    - AVD2001_OTA2-1.8.0.0_4_4a16fed_758744c.prod.sig.enc     cimg: v1, 2023-10-27T16:00:52 / part: kernel, encrypted, SquashFS
  - Arlo Audio Doorbell
    - AAD1001_1.2.0.0_320_401_DV1.bin                         unexpected container b'MMM\x00'
    - AAD1001_1.2.0.0_320_401_DV1.bin.enc                     cimg: v1, 2021-08-18T00:16:46 / part: kernel, encrypted, MMM
    - AAD1001_1.2.0.0_320_401_DV2.bin                         unexpected container b'MMM\x00'
    - AAD1001_1.2.0.0_320_401_DV2.bin.enc                     cimg: v1, 2021-08-18T00:18:13 / part: kernel, encrypted, MMM
  - Arlo Chime V2
    - AC2001_OTA-1.1.0.0_314_d36790b.prod.enc                 cimg: v1, 2023-05-03T18:09:53 / part: kernel, encrypted, MMM
    - AC2001_OTA-1.1.0.0_314_d36790b.prod.sig.enc             cimg: v1, 2023-05-03T18:09:53 / part: kernel, encrypted, MMM
  - Arlo Chime
    - AC1001_1.2.0.0_320_392_DV1.bin                          unexpected container b'MMM\x00'
    - AC1001_1.2.0.0_320_392_DV1.bin.enc                      cimg: v1, 2021-08-18T00:16:37 / part: kernel, encrypted, MMM
    - AC1001_1.2.0.0_320_392_DV2.bin                          unexpected container b'MMM\x00'
    - AC1001_1.2.0.0_320_392_DV2.bin.enc                      cimg: v1, 2021-08-18T00:17:55 / part: kernel, encrypted, MMM
- Floodlights
  - Arlo Pro 3 Floodlight
    - FB1001_1.080.28.0_12_590aec8.bin.enc                    cimg: v1, 2023-06-15T04:00:28 / part: kernel, encrypted
  - Arlo Security Light
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/updaterules/ABB1000_UpdateRules.json HTTP 404
- Arlo_Home_Security_System
  - Arlo Keypad Hub
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/SH1001/SH1001-1.10.9_e79f153.enc HTTP 404
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/LBB1001 HTTP 404
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/LBB1001 HTTP 404
  - Arlo Siren
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/SLB1001/SLB1001-1.0.156_f767856.enc HTTP 404
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/SLB1001/SLB1001-1.0.156_f767856.devsig.enc HTTP 404
    - http://updates.arlo.com/arlo/fw/fw_deployed/production/binaries/SLB1001/SLB1001-1.0.156_f767856.sig.enc HTTP 404
  - Arlo All-in-One Sensor
    - MS1001-2.1.246_e8e8e84.enc                              cimg: v2, 2023-09-20T22:16:02, (MS1001), signature unsupported, decryption unsupported / part: kernel, encrypted
    - MS1001-2.1.246_e8e8e84.sig.enc                          cimg: v2, 2023-09-20T22:16:02, (MS1001), signature unsupported, decryption unsupported / part: kernel, encrypted
  - Arlo Safe Button
    - FG_FW-0.0.26.2-apploader-signed.gbl                     unexpected container b'\xeb\x17\xa6\x03'
    - FG_FW-0.0.26.2-application-signed.gbl                   unexpected container b'\xeb\x17\xa6\x03'
```

## Helper

in ida folder:
* `openssl_err.py` parses <openssl/err.h> to generate a dict of libraries ID and
  functions ID to functions name. It needs to be executed from the <openssl>
  include directory
* `ossl_rename_ida.py` is the python script to be executed in IDA to rename
  function based on `ERR_put_error` (it already includes the information from
  `openssl_err.py`)
* `rename.py` is a python script to be executed in IDA to rename function based
  on log parameters.
