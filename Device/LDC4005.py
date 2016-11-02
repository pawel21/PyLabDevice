from IODevice import IODevice, BadDeviceException


class LDC4005:
    def __init__(self, usb_port):
        try:
            self.device = IODevice(usb_port)
            self._check_if_device_is_correct()
        except BadDeviceException:
            print("Bad device. This is not LDC4005")

    def _check_if_device_is_correct(self):
        correct_name =b'Thorlabs,LDC4005,M00298547,1.5.0/1.5.0\n'
        device_name = self.device.get_name()
        if correct_name != device_name:
            raise BadDeviceException

    def on(self):
        self.device.write("OUTPut ON")

    def off(self):
        self.device.write("OUTPut OFF")

    def set_ld_current_in_amper(self, value):
        self.device.write("SOURce:CURRent:LEVel:AMPLitude %s" % value)

    def ld_current_reading(self):
        self.device.write("INITiate")
        self.device.write("MEASure:CURRent")
        self.device.write("FETCh:CURRent?")
        value = self.device.read(100)
        return float(value)

    def ld_voltage_reading(self):
        self.device.write("INITiate")
        self.device.write("MEASure:VOLTage")
        self.device.write("FETCh:VOLTage?")
        value = self.device.read(100)
        return float(value)

    def get_current_limit_in_amper(self):
        self.device.write("SOURce:CURRent:LIMit:AMPLitude?")
        value = self.device.read(100)
        return float(value)

    def set_current_limit_in_amper(self, value):
        self.device.write("SOURce:CURRent:LIMit:AMPLitude %s" % str(value))

    def query_shape(self):
        self.device.write("SOURce:FUNCtion:SHAPe?")
        shape = self.device.read(100)
        return str(shape)

    def set_shape_dc(self):
        self.device.write("SOURce:FUNCtion:SHAPe DC")

    def set_shape_pulse(self):
        self.device.write("SOURce:FUNCtion:SHAPe PULSe")

    def get_period(self):
        self.device.write("SOURce:PULSe:PERiod?")
        period = self.device.read(100)
        return float(period)

    def set_period_in_seconds(self, level):  #
        self.device.write("SOURce:PULSe:PERiod " + str(level))
