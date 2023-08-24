
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

#        self.operationMode = {
#            'No mode': 0,
#            'Position mode': 1,
#            'Velocity mode': 3,
#            'Homing mode': 6,
#            'Cyclic synchronous position mode': 8,
#            'Cyclic synchronous velocity mode': 9,
#            'Cyclic synchronous torque mode': 10,
#        }
#
#        self.instructions = {
#            'Control word': ['uint16', '0x6040'],
#            'Status word': ['uint16', '0x6041'],
#            'Operation mode': ['int8', '0x6060'],
#            'Display operation mode': ['int8', '0x6061'],
#            'Position actual value': ['int32', '0x6064'],
#            'Velocity actual value': ['int32', '0x606C'],
#            'Target position': ['int32', '0x607A'],
#            'Profile velocity': ['uint32', '0x6081'],
#            'Profile acceleration': ['uint32', '0x6083'],
#            'Profile deceleration': ['uint32', '0x6084'],
#            'Target velocity': ['int32', '0x60FF'],
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
                comando = subprocess.run(['ethercat', 'download', '-t', 'int16', '0x6040', f'{id}', '--', '15'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print('--- Fallo!!! --- Reintentando... ---')
                    print (comando.stderr)
                else:
                    print('--- Palabra de control inicializada en 15 : Habilitado')
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
                    print('--- Palabra de control devuelta a 0 : Deshabilitado')
                    break
            else:
                print('------------- Fallo al reconfigurar la palabra de control ------------')
        print('----------------------------------------------------------------------')

    def servoVelocityMode(self):
        for id in range(len(self.slaves)):
            comando = subprocess.run(['ethercat', 'download', '-t', 'int32', '0x60FF', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print (comando.stderr)
                return 
            else:
                print(f'--- Velocidad objetivo del dispositivo {id} inicializada en 0 rpm')
            
            comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '3'], stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print (comando.stderr)
                return
            else:
                print(f'--- Modo de operacion reconfigurado a 3 : Velocity mode')
        print('----------------------------------------------------------------------')
    
        while True:
            print('Ingresa el id del servo y la nueva velocidad. Ejemplo: 0 500')
            print('Ingresa el id del servo y ? para ver la posicion actual Ej: 0 ?')
            print('Ingresa r r para volver al menu')
            id, spd = input().split()
            if id == 'r' and spd == 'r':
                break
            elif spd == '?':
                comando = subprocess.run(['ethercat', 'upload', '-t', 'int32', '0x6064', f'{id}'], stderr=subprocess.PIPE, text=True)
            else:
                comando = subprocess.run(['ethercat', 'download', '-t', 'int32', '0x60FF', f'{id}', '--', f'{spd}'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print (comando.stderr)
                else:
                    print(f'--- Velocidad objetivo del dispositivo {id} actualizada a {spd} rpm')
        
        for id in range(len(self.slaves)):
            comando = subprocess.run(['ethercat', 'download', '-t', 'int32', '0x60FF', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print (comando.stderr)
                raise Exception('------ Fallo al reconfigurar velocidad. Saliendo del programa. ------')
            else:
                print(f'--- Velocidad objetivo del dispositivo {id} devuelta a 0 rpm')
            
            comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print (comando.stderr)
                raise Exception('--- Fallo al reconfigurar modo de operacion. Saliendo del programa. ---')
            else:
                print(f'--- Modo de operacion reconfigurado a 0 : No mode')
        print('----------------------------------------------------------------------')

    def servoPositionMode(self):
        for id in range(len(self.slaves)):
            comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '1'], stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print (comando.stderr)
                return
            else:
                print(f'--- Modo de operacion reconfigurado a 1 : Position mode')

        print('----------------------------------------------------------------------')

        while True:
            print('Ingresa el id del servo, la nueva posicion en grados y velocidad Ejemplo: 0 90 20')
            print('Ingresa el id del servo y ? ? para ver la posicion y velocidad actual Ej: 0 ? ?')
            print('Ingresa r r r para volver al menu')
            id, pos, spd = input().split()
            comando = subprocess.run(['ethercat', 'download', '-t', 'int16', '0x6040', f'{id}', '--', '15'], stderr=subprocess.PIPE, text=True)
            if id == 'r' and pos == 'r' and spd == 'r':
                break
            elif pos == '?' and spd == '?':
                comando = subprocess.run(['ethercat', 'upload', '-t', 'int32', '0x6064', f'{id}'], stderr=subprocess.PIPE, text=True)
                comando = subprocess.run(['ethercat', 'upload', '-t', 'int32', '0x3000', f'{id}'], stderr=subprocess.PIPE, text=True)
            else:
                try:
                    encoderPosition = int(int(pos) * 10000 / 360)
                except Exception as ex:
                    print(ex)

                comando = subprocess.run(['ethercat', 'download', '-t', 'uint32', '0x6081', f'{id}', '--', f'{spd}'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print (comando.stderr)
                    return 
                else:
                    print(f'--- Velocidad operativa del dispositivo {id} configurada en {spd} rpm')
            

                comando = subprocess.run(['ethercat', 'download', '-t', 'int32', '0x607A', f'{id}', '--', f'{encoderPosition}'], stderr=subprocess.PIPE, text=True)
                if comando.stderr:
                    print (comando.stderr)
                else:
                    comando = subprocess.run(['ethercat', 'download', '-t', 'int16', '0x6040', f'{id}', '--', '31'], stderr=subprocess.PIPE, text=True)
                    if comando.stderr:
                        print (comando.stderr)
                    else:
                        print(f'--- Posicion objetivo del dispositivo {id} actualizada a {encoderPosition} user units')
        
        for id in range(len(self.slaves)):
            comando = subprocess.run(['ethercat', 'download', '-t', 'int8', '0x6060', f'{id}', '--', '0'], stderr=subprocess.PIPE, text=True)
            if comando.stderr:
                print (comando.stderr)
                raise Exception('--- Fallo al reconfigurar modo de operacion. Saliendo del programa. ---')
            else:
                print(f'--- Modo de operacion reconfigurado a 0 : No mode')
        print('----------------------------------------------------------------------')


    def run(self):
        self.servoInitAll()

        while True:
            print('--- Ingresa v para entrar en control por velocidad ---')
            print('--- Ingresa p para entrar en control por posicion ---')
            print('--- Ingresa x para deshabilitar los dispositivos y cerrar el programa ---')
            option = input()

            if option == 'v':
                self.servoVelocityMode()
            if option == 'p':
                self.servoPositionMode()
            if option == 'x':
                self.servoCloseAll()
                sys.exit()
                

if __name__ == '__main__':
    print('--- Pruebas de ethercat ---')

    try:
        ServoConection().run()
    except Exception as ex:
        print(ex)
        sys.exit(1)
