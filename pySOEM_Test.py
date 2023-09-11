
import sys
import ctypes
import pysoem
import dataclasses
import typing


@dataclasses.dataclass
class Device:
    name: str
    vendor_id: int
    product_code: int
    config_func: typing.Callable = None


class InputPdo(ctypes.Structure):       #0x1A00 DI TxPDO-Map
    _pack_ = 1
    _fields_ = [
        ('status_word', ctypes.c_uint16),                   #0x6041
        ('position_actual_value', ctypes.c_int32),          #0x6064
        ('velocity_actual_value', ctypes.c_int16),          #0x606C
        ('torque_actual_value', ctypes.c_int16),            #0x6077
        ('op_mode_display', ctypes.c_int16),                #0x6061
        ('current_actual_value', ctypes.c_int16),           #0x6078
        ('touch_probe_status', ctypes.c_uint16),            #0x60B9
        ('touch_probe_1_positive_value', ctypes.c_int16),   #0x60BA
        ('digital_inputs', ctypes.c_uint16),                #0x60FD
    ]

class OutputPdo(ctypes.Structure):      #0x1600 DO RxPDO-Map
    _pack_ = 1
    _fields_ = [
        ('control_word', ctypes.c_uint16),                   #0x6040
        ('target_position', ctypes.c_int32),                 #0x607A
        ('target_velocity', ctypes.c_int32),                 #0x60FF
        ('op_mode', ctypes.c_int8),                          #0x6060
        ('target_torque', ctypes.c_int16),                   #0x6071
        ('touch_probe_control', ctypes.c_uint16),            #0x60B8
        ('positive_torque_limit', ctypes.c_uint16),          #0x60E0
        ('negative_torque_limit', ctypes.c_uint16),          #0x60E1
        ('max_profile_velocity', ctypes.c_uint32),           #0x607F
    ]


class ServoConection:
    def __init__(self):
        self.ifname = 'eth0'
        self.master = pysoem.Master()
        self.expectedSlaves = {
            0: Device('INVT_DA200_262', 0x0000_0616, 0x0000_0000, self.servoConfig)
        }
        self.modes_of_operation = {
            'No mode': 0,
            'Profile position mode': 1,
            'Profile velocity mode': 3,
            'Homing mode': 6,
            'Cyclic synchronous position mode': 8,
            'Cyclic synchronous velocity mode': 9,
            'Cyclic synchronous torque mode': 10,
        }

    def convertInputData(self, data):
        return InputPdo.from_buffer_copy(data)

    def servoConfig(self, id):
        servo = self.master.slaves[id]
        print('Entro en config')

        servo.sdo_write(index=0x1C12, subindex=0, data=bytes(ctypes.c_uint16(0)))
        print('1')
        servo.sdo_write(index=0x1C13, subindex=0, data=bytes(ctypes.c_uint16(0)))
        print('2')

        servo.sdo_write(index=0x1600, subindex=0, data=bytes(0))
        print('3')
        servo.sdo_write(index=0x1601, subindex=0, data=bytes(0))
        print('4')
        servo.sdo_write(index=0x1602, subindex=0, data=bytes(0))
        print('5')
        servo.sdo_write(index=0x1603, subindex=0, data=bytes(0))
        print('6')
        servo.sdo_write(index=0x1A00, subindex=0, data=bytes(0))
        print('7')
        servo.sdo_write(index=0x1A01, subindex=0, data=bytes(0))
        print('8')
        servo.sdo_write(index=0x1A02, subindex=0, data=bytes(0))
        print('9')
        servo.sdo_write(index=0x1A03, subindex=0, data=bytes(0))
        print('10')

        servo.sdo_write(index=0x1600, subindex=1, data=bytes(1640807056))#0x60400010
        print('almenos pasa el primero')
        servo.sdo_write(index=0x1600, subindex=2, data=bytes(1618608160))#0x607A0020
        servo.sdo_write(index=0x1600, subindex=3, data=bytes(1627324448))#0x60FF0020
        servo.sdo_write(index=0x1600, subindex=4, data=bytes(1616904200))#0x60600008
        servo.sdo_write(index=0x1600, subindex=5, data=bytes(1618018320))#0x60710010
        servo.sdo_write(index=0x1600, subindex=6, data=bytes(1622671376))#0x60B80010
        servo.sdo_write(index=0x1600, subindex=7, data=bytes(1625292816))#0x60E00010
        servo.sdo_write(index=0x1600, subindex=8, data=bytes(1625358352))#0x60E10010
        servo.sdo_write(index=0x1600, subindex=9, data=bytes(1618935840))#0x607F0020
        servo.sdo_write(index=0x1600, subindex=0, data=bytes(9))
        print('12')

        servo.sdo_write(index=0x1A00, subindex=1, data=0x60410010)
        servo.sdo_write(index=0x1A00, subindex=2, data=0x60640020)
        servo.sdo_write(index=0x1A00, subindex=3, data=0x606C0020)
        servo.sdo_write(index=0x1A00, subindex=4, data=0x60770010)
        servo.sdo_write(index=0x1A00, subindex=5, data=0x60610008)
        servo.sdo_write(index=0x1A00, subindex=6, data=0x60780010)
        servo.sdo_write(index=0x1A00, subindex=7, data=0x60B90010)
        servo.sdo_write(index=0x1A00, subindex=8, data=0x60BA0020)
        servo.sdo_write(index=0x1A00, subindex=9, data=0x60FD0020)
        servo.sdo_write(index=0x1A00, subindex=0, data=9)
        print('13')

        servo.sdo_write(index=0x1C12, subindex=1, data=0x1600)
        servo.sdo_write(index=0x1C13, subindex=1, data=0x1A00)
        print('14')

        servo.sdo_write(index=0x1C12, subindex=0, data=1)
        servo.sdo_write(index=0x1C13, subindex=0, data=1)

        print('Termino la config')


        #servo.sdo_write(index=0x1C12, subindex=0, data=bytes(ctypes.c_int16(0)))

        #servo.dc_sync(True, 1_000_000)

        #da200.sdo_write(0x6060, 0, bytes(ctypes.c_int8(3)))

    
    def run(self):
        global da200
        self.master.open(self.ifname)

        if self.master.config_init() <= 0:
            self.master.close()
            raise Exception("No devices found")
        
        for i, device in enumerate(self.master.slaves):
            if not ((device.man == self.expectedSlaves[i].vendor_id) and
                    (device.id == self.expectedSlaves[i].product_code)):
                self.master.close()
                raise Exception('Unexpected slaves layout')
            device.config_func = self.expectedSlaves[i].config_func

        print(f'Status code: {pysoem.al_status_code_to_string(self.master.slaves[0].al_status)}')

        self.master.config_map()

        print(f'Status code: {pysoem.al_status_code_to_string(self.master.slaves[0].al_status)}')


        #print(f'Esto es SAFEOP {pysoem.SAFEOP_STATE}')  #4
        #print(f'Esto es OP {pysoem.OP_STATE}')          #8
        #print(f'Esto es INIT {pysoem.INIT_STATE}')      #1
        #print(f'Esto es PREOP {pysoem.PREOP_STATE}')    #2
        #print(f'Esto es BOOT {pysoem.BOOT_STATE}')      #3
        #print(f'Esto es NONE STATE {pysoem.NONE_STATE}') #0
        

        if self.master.state_check(pysoem.SAFEOP_STATE, 50_000) != pysoem.SAFEOP_STATE:
            self.master.read_state()
            for device in self.master.slaves:
                if not device.state == pysoem.SAFEOP_STATE:
                    print(f'{device.name} did not reach SAFEOP state')
                    print(f'Status code: {(device.al_status)} ({pysoem.al_status_code_to_string(device.al_status)})')
            raise Exception('Not all devices reached SAFEOP state')
        
        self.master.state = pysoem.OP_STATE
        self.master.write_state()
        self.master.state_check(pysoem.OP_STATE, 50_000)

        if self.master.state != pysoem.OP_STATE:
            self.master.read_state()
            for device in self.master.slaves:
                if not device.state == pysoem.OP_STATE:
                    print(f'{device.name} did not reach OP state')
                    print(f'Status code: {hex(device.al_status)}')
            raise Exception('Not all devices reached OP state')
        
        for i, device in enumerate(self.master.slaves):
            print(f'Index = {i} : Device = {device.name} : Status = {device.al_status}')
 
        print('-------------------------------------')


        
        print('FIN :)')
        self.master.close()


if __name__ == '__main__':
    print('--- Pruebas de ethercat ---')

    try:
        ServoConection().run()
    except Exception as ex:
        print(ex)
        sys.exit(1)
