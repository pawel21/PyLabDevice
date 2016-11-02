import sys
sys.path.insert(0, "/home/pawel1/Pulpit/PyLabDevice/Device")

from BaseMeasureInfo import BaseMeasureInfo
from Device import Device


class MeasureDeviceConnect(BaseMeasureInfo):
    try:
        dev = Device()
        ldc = dev.get_ldc4005_instance()
        pm100 = dev.get_pm100_instance()
        BaseMeasureInfo.OUT_MSG += "Connections with device successful"
        BaseMeasureInfo.WAVELENGTH = str(pm100.get_current_wavelength_in_nm())
        BaseMeasureInfo.LD_CURRENT_LIMIT = str(ldc.get_current_limit_in_amper()*1000)
    except Exception as err:
        BaseMeasureInfo.logger.error(err)
        BaseMeasureInfo.OUT_MSG = ""
        BaseMeasureInfo.OUT_MSG += ("Error %s" % err)