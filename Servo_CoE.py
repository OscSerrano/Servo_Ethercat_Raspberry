
import sys 
import subprocess

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
            'No mode': 0,
            'Position mode': 1,     #<-- Has 4 inner modes
            'Velocity mode': 3,
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

#        self.instructions = {
#            'Control word': ['uint16', '0x6040'],          #Funcion agregada
#            'Status word': ['uint16', '0x6041'],           #Funcion agregada
#            'Operation mode': ['int8', '0x6060'],          #Funcion agregada
#            'Display operation mode': ['int8', '0x6061'],  #Funcion agregada
#            'Position actual value': ['int32', '0x6064'],  #Funcion agregada
#            'Velocity actual value': ['int32', '0x606C'],  #Funcion agregada
#            'Target position': ['int32', '0x607A'],        #Funcion agregada
#            'Profile velocity': ['uint32', '0x6081'],      #Funcion agregada
#            'Profile acceleration': ['uint32', '0x6083'],
#            'Profile deceleration': ['uint32', '0x6084'],
#            'Target velocity': ['int32', '0x60FF'],        #Funcion agregada
#        }

    def servoInitAll(self):
        print('------------------- Configurando los dispositivos --------------------')
        for id in range(len(self.slaves)):
            print(f'Inicializando el modo de operacion del dispositivo {id}:')
            for _ in range(self.retryAttempts):
                comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print('--- Fallo!!! --- Reintentando... ---')
                    print (comando.stderr)
                else:
                    print(f'--- Modo de operacion inicializado en 0 : No mode')
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

    def servoCloseAll(self):
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
        print(f'--- Modificando esclavo {id} ---')
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


    def get_Status_Word(self, id):
        comando = subprocess.run(['ethercat', 'upload', '-t', 'uint16', '0x6041', f'{id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comando.stderr:
            print (comando.stderr)
        else:
            print(f'--- Estado del dispositivo {id}: ')
            status = int(comando.stdout)
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
            print(f'--- Modo de operacion del dispositivo {id}: {comando.stdout}')
            #print(f'--- Modo de operacion: {list(self.operationModes.keys())[list(self.operationModes.values()).index(comando.stdout)]}')

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



    def servoVelocityMode(self):
        for id in range(len(self.slaves)):
            self.set_Operation_Mode(id, self.operationModes['Velocity mode'])
            self.set_Control_Word(id, self.controlWords['Enable operation'])
        print('----------------------------------------------------------------------')
    
        while True:
            print('Ingresa el id del servo y la nueva velocidad. Ejemplo: 0 500')
            print('Ingresa el id y ? para ver la posicion y velocidad actual Ej: 0 ?')
            print('Ingresa r r para volver al menu')
            try:
                id, spd = input().split()
                if id == 'r' and spd == 'r':
                    break
                elif spd == '?':
                    self.get_Actual_Position(id)
                    self.get_Actual_Velocity(id)
                else:
                    self.set_Target_Velocity(id, spd)
            except:
                print('---')
                print('¡¡¡ Ingresa los valores requeridos !!!')
                print('---')
        
        for id in range(len(self.slaves)):
            self.set_Target_Velocity(id, 0)
            self.set_Operation_Mode(id, self.operationModes['No mode'])
            self.set_Control_Word(id, self.controlWords['Shutdown'])
            
        print('----------------------------------------------------------------------')

    def servoPositionMode(self, operation, newSetPoint):
        for id in range(len(self.slaves)):
            self.set_Operation_Mode(id, self.operationModes['Position mode'])
            self.set_Control_Word(id, self.controlWords[operation])

        print('----------------------------------------------------------------------')

        while True:
            print('Ingresa el id del servo, la nueva posicion en grados y velocidad Ej: 0 90 20')
            print('Ingresa el id y ? ? para ver la posicion y velocidad actual Ej: 0 ? ?')
            print('Ingresa r r r para volver al menu')
            try:
                id, pos, spd = input().split()
                if id == 'r' and pos == 'r' and spd == 'r':
                    break
                elif pos == '?' and spd == '?':
                    self.get_Actual_Position(id)
                    self.get_Actual_Velocity(id)
                else:
                    try:
                        encoderPosition = int(int(pos) * 10000 / 360)
                    except Exception as ex:
                        print(ex)

                    self.set_Operative_Velocity(id, spd)            
                    self.set_Target_Position(id, encoderPosition)
                    self.set_Control_Word(id, self.controlWords[newSetPoint])
                    self.set_Control_Word(id, self.controlWords[operation])
            except:
                print('---')
                print('¡¡¡ Ingresa los valores requeridos !!!')
                print('---')

        for id in range(len(self.slaves)):
            self.set_Operation_Mode(id, self.operationModes['No mode'])
            self.set_Control_Word(id, self.controlWords['Shutdown'])
           
        print('----------------------------------------------------------------------')


    def run(self):
        self.servoInitAll()

        while True:
            print('--- Ingresa vel para entrar en control por velocidad ---')
            print('--- Ingresa pa para entrar en control por posicion absoluta ---')
            print('--- Ingresa pai para entrar en control por posicion absoluta inmediata---')
            print('--- Ingresa pr para entrar en control por posicion relativa ---')
            print('--- Ingresa pri para entrar en control por posicion relativa inmediata---')
            print('--- Ingresa exit para deshabilitar los dispositivos y cerrar el programa ---')
            option = input()

            if option == 'vel':
                #In this mode user only controls velocity
                self.servoVelocityMode()
            #Next modes control both position and velocity
            elif option == 'pa':
                #In this and next mode position is an absolute value between -2^31 -1 y 2^31 -1
                #A buffer on the servo-drive is used to save a list of the given positions
                self.servoPositionMode('Enable operation', 'New set-point')
            elif option == 'pai':
                #Similar to pa, but no buffer used because it changes target immediately
                self.servoPositionMode('Change set immediately', 'Change to new set-point')
            elif option == 'pr':
                #The last 2 modes work by adding the given position to final position
                #This mode finishes all the sums one by one
                self.servoPositionMode('Relative position operation', 'New relative set-point')
            elif option == 'pri':
                #This mode do all the adding first, so it goes to final position immediately
                self.servoPositionMode('Change relative set immediately', 'Change to new relative set-point')
            elif option == 'exit':
                self.servoCloseAll()
                sys.exit()
                

if __name__ == '__main__':
    print('--- Pruebas de ethercat ---')

    try:
        ServoConection().run()
    except Exception as ex:
        print(ex)
        sys.exit(1)
        
