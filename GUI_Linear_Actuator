     
import sys 
import subprocess
import tkinter as tk
from tkinter import messagebox

class Aplication(tk.Tk):
    def __init__(self):
        #Set important stuff
        tk.Tk.__init__(self)
        self.protocol('WM_DELETE_WINDOW', self.quitApp)
        self.servo = ServoConection()

        #Window configuration
        self.title('GUI test')
        self.geometry('800x500')    #Height x Width
        #self.resizable(False,False)
        self.config(background='gray')
        self.rowconfigure([0,1,2,4,5], weight=1)
        self.columnconfigure(tuple(range(7)), weight=1)

        self.createWidgets()

    def createWidgets(self):
        self.inputSpd = tk.StringVar(self)
        self.speed = tk.StringVar(self, 'Actual speed: 0 rpm')
        self.inputPos = tk.StringVar(self)
        self.position = tk.StringVar(self, 'Actual position: 0 deg')

        #Widgets (window elements)
        #Title
        self.title = tk.Label(
            self,
            text='Linear actuator control',
            font=("Comic Sans MS", 18, "bold"),
            background='gray'
        ).grid(
            row=0, column=0,
            columnspan=7,
            sticky=tk.EW
        )

        #Speed modification section
        self.spdTitle = tk.Label(
            self,
            text='Set motor speed in rpm',
            font=("Comic Sans MS", 14, "bold"),
            background='gray'
        ).grid(
            row=1, column=0,
            columnspan=7,
            sticky=tk.EW
        )

        self.inSpd = tk.Entry(
            self,
            width=6,
            textvariable=self.inputSpd,
            font=("Comic Sans MS", 14, "bold"),
            justify='right'
        )
        self.inSpd.grid(
            row=2, column=3,
            sticky=tk.S
        )
        self.inSpd.bind('<Return>', self.setSpd)

        self.spdBar = tk.Scale(
            self,
            variable=self.inputSpd,
            from_=0, to=5000,
            orient='horizontal',
            cursor='hand2',
            command=self.setSpd
        ).grid(
            row=3, column=0,
            columnspan=7,
            sticky=tk.EW
        )

        #Position modification section

        self.posTitle = tk.Label(
            self,
            text='Set position in deg',
            font=("Comic Sans MS", 14, "bold"),
            background='gray'
        ).grid(
            row=4, column=0,
            columnspan=7,
            sticky=tk.EW
        )

        self.inPos = tk.Entry(
            self,
            width=6,
            textvariable=self.inputPos,
            font=("Comic Sans MS", 14, "bold"),
            justify='right'
        )
        self.inPos.grid(
            row=5, column=3,
            sticky=tk.S
        )
        self.inPos.bind('<Return>', self.setPos)

        self.posBar = tk.Scale(
            self,
            variable=self.inputPos,
            from_=0, to=14400,
            orient='horizontal',
            cursor='hand2',
            command=self.setPos
        ).grid(
            row=6, column=0,
            columnspan=7,
            sticky=tk.EW
        )

    def setSpd(self, _):
        print(f'velocidad: {self.inputSpd.get()}')
        self.servo.set_Operative_Velocity(0,self.inputSpd.get())
        #self.speed.set(f'Velocidad actual: {self.inputSpd.get()} rpm')

    def setPos(self, _):
        print(f'Posicion: {self.inputPos.get()}')
        self.servo.gotoPosition(0,self.inputPos.get())
        #self.speed.set(f'Posicion actual: {self.inputPos.get()} rpm')

    def runApp(self):
        self.servo.initAll()
        self.mainloop()
    
    def quitApp(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.servo.closeAll
            self.destroy()


class ServoConection:
    def __init__(self):
        self.ifname = 'eth0'
        self.retryAttempts = 5
        self.slaves = []

        print('------------------ Buscando dispositivos conectados ------------------')
        for _ in range(self.retryAttempts):
            comando = subprocess.run(['ethercat', 'slaves'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print('--- Fallo!!! --- Reintentando... ---')
                print (comando.stderr)
            else:
                break
        else:
            raise Exception('------- Fallo al detectar dispositivos. Saliendo del programa. -------')

        if not comando.stdout:
            raise Exception('------- No se detectaron dispositivos. Saliendo del programa.  -------')


        self.slaves = comando.stdout.splitlines()
        
        print(self.slaves)
        print('----------------------------------------------------------------------')

        self.operationModes = {
            'No mode': 0,           #Added
            'Position mode': 1,     #<-- Has 4 inner modes, all added
            'Velocity mode': 3,     #Added
            'Homing mode': 6,
            'Cyclic synchronous position mode': 8,
            'Cyclic synchronous velocity mode': 9,
            'Cyclic synchronous torque mode': 10,
        }

        self.controlWords = {
            'Switch off': 0,                        #No on, No voltage, No quick stop, No operation
            'Shutdown': 6,                          #No on, No operation, With voltage, With quick stop
            'Disable operation': 7,                 #No operation, On, With voltage, With quick stop
            'Enable operation': 15,                 #Operative, On, With voltage, With quick stop

            'New set-point': 31,                    #Add target position to queue while operative in position or homing mode

            'Change set immediately': 47,           #Go to next position while operative in position mode
            'Change to new set-point': 63,          #Add target position and go there immediately

            'Relative position operation': 79,      #Operate with relative positions in position mode
            'New relative set-point': 95,           #Add target relative position to queue while operative in position mode

            'Change relative set immediately': 111, #Go to next position in queue while in relative position mode
            'Change to new relative set-point': 127 #Add target relative position and go there immediately
        }


    #Read/Write intructions
    def set_Operation_Mode(self, id, mode):
        #Check self.operationModes for availale modes
        comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', f'{mode}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Modo de operacion del dispositivo {id} actualizado a {mode} : {list(self.operationModes.keys())[list(self.operationModes.values()).index(mode)]}')

    def set_Control_Word(self, id, word):
        comando = subprocess.run(['ethercat', 'download', '-t', 'uint16', '0x6040', f'{id}', '--', f'{word}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Palabra de control del dispositivo {id} actualizada a {word} : {list(self.controlWords.keys())[list(self.controlWords.values()).index(word)]}')

    def set_Target_Velocity(self, id, spd):
        #Slave's index and speed in rpm while in speed mode
        comando = subprocess.run(['ethercat', 'download', '-t', 'int32', '0x60FF', f'{id}', '--', f'{spd}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Velocidad objetivo del dispositivo {id} actualizada a {spd} rpm')

    def set_Operative_Velocity(self, id, spd):
        #Slave's index and speed in rpm while in position mode
        comando = subprocess.run(['ethercat', 'download', '-t', 'uint32', '0x6081', f'{id}', '--', f'{spd}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Velocidad operativa del dispositivo {id} configurada en {spd} rpm')

    def set_Target_Position(self, id, pos):
        comando = subprocess.run(['ethercat', 'download', '-t', 'int32', '0x607A', f'{id}', '--', f'{pos}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Posicion objetivo del dispositivo {id} actualizada a {pos} user units')

    def set_Acceleration(self, id, acc):
        #Works in any mode, but has to be configured when entering new mode 
        comando = subprocess.run(['ethercat', 'download', '-t', 'uint32', '0x6083', f'{id}', '--', f'{acc}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Aceleracion operativa del dispositivo {id} configurada en {acc}')

    def set_Deceleration(self, id, dec):
        #Works in any mode, but has to be configured when entering new mode 
        comando = subprocess.run(['ethercat', 'download', '-t', 'uint32', '0x6084', f'{id}', '--', f'{dec}'], stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Desaceleracion operativa del dispositivo {id} configurada en {dec}')

    #Read only instructions
    def get_Error_Code(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'uint16', '0x603F', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Codigo de error del dispositivo {id}: {comando.stdout}')

    def get_Status_Word(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'uint16', '0x6041', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Estado del dispositivo {id}: ')
            status = int(comando.stdout.split()[1])
            status1 = status & 111
            status2 = status & 79
            if status1 == 33:
                print('- Ready to switch on')
            elif status1 == 35:
                print('- Switched on')
            elif status1 == 39:
                print('- Operation enabled')
            elif status1 == 7:
                print('- Quick stop active')
            elif status2 == 0:
                print('- Not ready to switch on')
            elif status2 == 64:
                print('- Switch on disabled')
            elif status2 == 15:
                print('- Fault reaction active')
            elif status2 == 8:
                print('- Fault')
            else:
                print('!! Unidentified')
            
            #The next ones describe speed, position or torque dependin on mode
            if status & 1024 == 1024:
                print('- Target reached')           
            if status & 2048 == 2048:
                print('- Internal limit active')
            if status & 4096 == 4096:
                print('- Set-point Acknowledge or Speed zero state')
            if status & 8192 == 8192:
                print('- Following or slippage Error')
                   
    def get_Operation_Mode(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'int8', '0x6061', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Modo de operacion del dispositivo {id}: {list(self.operationModes.keys())[list(self.operationModes.values()).index(int(comando.stdout.split()[1]))]}')

    def get_Actual_Velocity(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'int32', '0x606C', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Velocidad actual del dispositivo {id} en rpm: {comando.stdout}')

    def get_Actual_Position(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'int32', '0x6064', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Posicion actual del dispositivo {id} en user units: {comando.stdout}')

    def get_Actual_Torque(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'int16', '0x6077', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Torque actual del dispositivo {id} : {comando.stdout}')

    #Operation examples
    def initAll(self):
        print('------------------- Configurando los dispositivos --------------------')
        for id in range(len(self.slaves)):
            print(f'Inicializando el modo de operacion del dispositivo {id}:')
            for _ in range(self.retryAttempts):
                comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '1'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print('--- Fallo!!! --- Reintentando... ---')
                    print (comando.stderr)
                else:
                    print(f'--- Modo de operacion inicializado en 1 : Position mode')
                    break
            else:
                print('------------- Fallo al inicializar el modo de operacion --------------')

            print(f'Inicializando la palabra de control del dispositivo {id}:')
            for _ in range(self.retryAttempts):
                comando = subprocess.run(['ethercat', 'download', '-t', 'int16', '0x6040', f'{id}', '--', '6'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print('--- Fallo!!! --- Reintentando... ---')
                    print (comando.stderr)
                else:
                    print('--- Palabra de control inicializada en 6 : Shutdown')
                    break
            else:
                print('------------- Fallo al inicializar la palabra de control -------------')
        print('----------------------------------------------------------------------')

    def closeAll(self):
        print('------------------ Reconfigurando los dispositivos -------------------')
        for id in range(len(self.slaves)):
            print(f'Reconfigurando el modo de operacion del dispositivo {id}:')
            for _ in range(self.retryAttempts):
                comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print('--- Fallo!!! --- Reintentando... ---')
                    print (comando.stderr)
                else:
                    print(f'--- Modo de operacion devuelto a 0 : No mode')
                    break
            else:
                print('------------- Fallo al reconfigurar el modo de operacion -------------')


            print(f'Reconfigurando la palabra de control del dispositivo {id}:')
            for _ in range(self.retryAttempts):
                comando = subprocess.run(['ethercat', 'download', '-t', 'int16', '0x6040', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print('--- Fallo!!! --- Reintentando... ---')
                    print (comando.stderr)
                else:
                    print('--- Palabra de control devuelta a 0 : Switch off')
                    break
            else:
                print('------------- Fallo al reconfigurar la palabra de control ------------')
        print('----------------------------------------------------------------------')

    def gotoPosition(self, id, pos):
            try:
                encoderPosition = int(int(pos) * 10000 / 360) #To convert input in grades to reference units where 10000 is a turn
                self.set_Target_Position(id, encoderPosition)
            except Exception as ex:
                print(ex)
        
            self.set_Control_Word(id, self.controlWords['Change to new set-point'])
            self.set_Control_Word(id, self.controlWords['Change set immediately'])

                      
if __name__ == '__main__':
    print('--- Pruebas para el actuador linear ---')

    try:
        gui = Aplication().runApp()
    except Exception as ex:
        print(ex)
        sys.exit(1)
