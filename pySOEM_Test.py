
import sys
import ctypes
import pysoem
import dataclasses
import typing
import time
import threading


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
#        ('torque_actual_value', ctypes.c_int16),            #0x6077
        ('op_mode_display', ctypes.c_int8),                #0x6061
#        ('current_actual_value', ctypes.c_int16),           #0x6078
#        ('touch_probe_status', ctypes.c_uint16),            #0x60B9
#        ('touch_probe_1_positive_value', ctypes.c_int16),   #0x60BA
        ('digital_inputs', ctypes.c_uint16),                #0x60FD
    ]

class OutputPdo(ctypes.Structure):      #0x1600 DO RxPDO-Map
    _pack_ = 1
    _fields_ = [
        ('control_word', ctypes.c_uint16),                   #0x6040
        ('target_position', ctypes.c_int32),                 #0x607A
        ('target_velocity', ctypes.c_int32),                 #0x60FF
        ('op_mode', ctypes.c_int8),                          #0x6060
#        ('target_torque', ctypes.c_int16),                   #0x6071
#        ('touch_probe_control', ctypes.c_uint16),            #0x60B8
#        ('positive_torque_limit', ctypes.c_uint16),          #0x60E0
#        ('negative_torque_limit', ctypes.c_uint16),          #0x60E1
#        ('max_profile_velocity', ctypes.c_uint32),           #0x607F
    ]

class ServoConection:
    def __init__(self):
        self.ifname = 'eth0'
        self.stopPDO_Thread = threading.Event()
        self.actualWKC = 0
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

        servo.sdo_write(index=0x1C12, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1C13, subindex=0, data=bytes(ctypes.c_int8(0)))

        servo.sdo_write(index=0x1600, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1601, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1602, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1603, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1A00, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1A01, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1A02, subindex=0, data=bytes(ctypes.c_int8(0)))
        servo.sdo_write(index=0x1A03, subindex=0, data=bytes(ctypes.c_int8(0)))

        servo.sdo_write(index=0x1600, subindex=1, data=bytes(ctypes.c_int32(1614807056)))#0x60400010 - control word
        servo.sdo_write(index=0x1600, subindex=2, data=bytes(ctypes.c_int32(1618608160)))#0x607A0020 - target position
        servo.sdo_write(index=0x1600, subindex=3, data=bytes(ctypes.c_int32(1627324448)))#0x60FF0020 - target velocity
        servo.sdo_write(index=0x1600, subindex=4, data=bytes(ctypes.c_int32(1616904200)))#0x60600008 - op mode
#        servo.sdo_write(index=0x1600, subindex=5, data=bytes(ctypes.c_int32(1618018320)))#0x60710010 - target torque
#        servo.sdo_write(index=0x1600, subindex=6, data=bytes(ctypes.c_int32(1622671376)))#0x60B80010 - t probe ctrl value
#        servo.sdo_write(index=0x1600, subindex=7, data=bytes(ctypes.c_int32(1625292816)))#0x60E00010 - +torque limit
#        servo.sdo_write(index=0x1600, subindex=8, data=bytes(ctypes.c_int32(1625358352)))#0x60E10010 - -torque limit
#        servo.sdo_write(index=0x1600, subindex=9, data=bytes(ctypes.c_int32(1618935840)))#0x607F0020 - max profile velocity
        servo.sdo_write(index=0x1600, subindex=0, data=bytes(ctypes.c_int8(4)))

        servo.sdo_write(index=0x1A00, subindex=1, data=bytes(ctypes.c_int32(1614872592)))#0x60410010 - status word
        servo.sdo_write(index=0x1A00, subindex=2, data=bytes(ctypes.c_int32(1617166368)))#0x60640020 - actual position
        servo.sdo_write(index=0x1A00, subindex=3, data=bytes(ctypes.c_int32(1617690656)))#0x606C0020 - actual velocity
#        servo.sdo_write(index=0x1A00, subindex=4, data=bytes(ctypes.c_int32(1618411536)))#0x60770010 - actual torque
        servo.sdo_write(index=0x1A00, subindex=4, data=bytes(ctypes.c_int32(1616969736)))#0x60610008 - display op mode
#        servo.sdo_write(index=0x1A00, subindex=6, data=bytes(ctypes.c_int32(1618477072)))#0x60780010 - current value
#        servo.sdo_write(index=0x1A00, subindex=7, data=bytes(ctypes.c_int32(1622736912)))#0x60B90010 - t probe status val
#        servo.sdo_write(index=0x1A00, subindex=8, data=bytes(ctypes.c_int32(1622802464)))#0x60BA0020 - t probe 1+ value
        servo.sdo_write(index=0x1A00, subindex=5, data=bytes(ctypes.c_int32(1627193376)))#0x60FD0020 - digital inputs
        servo.sdo_write(index=0x1A00, subindex=0, data=bytes(ctypes.c_int8(5)))

        servo.sdo_write(index=0x1C12, subindex=1, data=bytes(ctypes.c_uint16(5632)))#0x1600
        servo.sdo_write(index=0x1C13, subindex=1, data=bytes(ctypes.c_uint16(6656)))#0x1A00

        servo.sdo_write(index=0x1C12, subindex=0, data=bytes(ctypes.c_int8(1)))
        servo.sdo_write(index=0x1C13, subindex=0, data=bytes(ctypes.c_int8(1)))

        print('Termino la config')


        #servo.dc_sync(True, 1_000_000)

    def processData_Thread(self):
        while not self.stopPDO_Thread.is_set():
            self.master.send_processdata()
            self.actualWKC = self.master.receive_processdata(10000)
            if not self.actualWKC == self.master.expected_wkc:
                print('Incorrect wkc')
            time.sleep(0.001)

    def run(self):
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

        self.master.config_map()

        #print(f'Status code: {pysoem.al_status_code_to_string(self.master.slaves[0].al_status)}')

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
                    print(f'Status code: {hex(device.al_status)} ({pysoem.al_status_code_to_string(device.al_status)})')
            raise Exception('Not all devices reached SAFEOP state')
        
        self.master.state = pysoem.OP_STATE


        procThread = threading.Thread(target=self.processData_Thread)
        procThread.start()


        self.master.write_state()
        self.master.state_check(pysoem.OP_STATE, 50_000)

        if self.master.state != pysoem.OP_STATE:
            self.master.read_state()
            for device in self.master.slaves:
                if not device.state == pysoem.OP_STATE:
                    print(f'{device.name} did not reach OP state')
                    print(f'Status code: {hex(device.al_status)} ({pysoem.al_status_code_to_string(device.al_status)})')
            self.stopPDO_Thread.set()
            procThread.join()
            self.master.state = pysoem.INIT_STATE
            self.master.write_state()
            self.master.close()
            raise Exception('Not all devices reached OP state')

        for i, device in enumerate(self.master.slaves):
            print(f'id: {i}, name: {device.name}, state: maybe OP, status: {pysoem.al_status_code_to_string(device.al_status)}')
        print('----------------------------------------------------------------------')

        inputData = InputPdo()
        outputData = OutputPdo()
        outputData.control_word = 47
        outputData.op_mode = self.modes_of_operation['Profile position mode']
        self.master.slaves[0].output = bytes(outputData)

        try:
            while True:
                print('Ingresa la nueva posicion en grados y velocidad Ej: 90 20')
                print('Ingresa ? ? para ver el estatus del dispositivo Ejemplo: ? ?')
                print('Ingresa ctrl C para finalizar')
                if pos == '?' and spd == '?':
                    inputData = self.convertInputData(self.master.slaves[0].input)
                    print(f'--- Status: {inputData.status_word}')
                    print(f'--- Position: {inputData.position_actual_value}')
                    print(f'--- Velocity: {inputData.velocity_actual_value}')
                    print(f'--- Dig inpts: {inputData.digital_inputs}')
                else:
                    try:
                        pos, spd = int(input().split())
                        encoderPosition = int(pos * 10000 / 360)
                    except:
                        print('---')
                        print('¡¡¡ Ingresa los valores requeridos !!!')
                        print('---')

                    outputData.target_velocity = spd
                    outputData.target_position = encoderPosition
                    outputData.control_word = 67
                    time.sleep(0.001)
                    outputData.control_word = 47

        except KeyboardInterrupt:
            # ctrl + c
            print('Stopped')

        outputData.control_word = 0
        outputData.op_mode = self.modes_of_operation['No mode']
        self.master.slaves[0].output = bytes(outputData)
        self.master.send_processdata()
        self.master.receive_processdata(1000)
        inputData = self.convertInputData(self.master.slaves[0].input)
        print(f'--- Status: {inputData.status_word}')
        print(f'--- OP Mode: {inputData.op_mode_display}')
    

        self.master.state = pysoem.INIT_STATE
        self.master.write_state()
        self.master.close()


if __name__ == '__main__':
    print('--- Pruebas de ethercat ---')

    try:
        ServoConection().run()
    except Exception as ex:
        print(ex)
        sys.exit(1)
