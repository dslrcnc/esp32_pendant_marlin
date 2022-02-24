from machine import Pin, SoftI2C, UART
import ssd1306
import time

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
b_up = Pin(18, Pin.IN, Pin.PULL_UP)
b_down = Pin(19, Pin.IN, Pin.PULL_UP)
b_left = Pin(23, Pin.IN, Pin.PULL_UP)
b_right = Pin(14, Pin.IN, Pin.PULL_UP)
b_mid = Pin(27, Pin.IN, Pin.PULL_UP)
b_set = Pin(26, Pin.IN, Pin.PULL_UP)
b_reset = Pin(25, Pin.IN, Pin.PULL_UP)
letra_x = 88
letra_y = 89
letra_z = 90
letra_e = 69
letra_c = 67
letra_space = 32
letra_minus = 45


# ESP8266 Pin assignment
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

uart = UART(2, 250000)
uart.init(250000, bits=8, parity=None, stop=1)
uart.read()
uart.write('M121\n')
uart.read()

INCREMENT = 1.0
X_P = 0.0
Y_P = 0.0
Z_P = 0.0
E_P = 0.0
SPEED_P = 300
X_A = 0.0
Y_A = 0.0
Z_A = 0.0
E_A = 0.0
X_B = 0.0
Y_B = 0.0
Z_B = 0.0
E_B = 0.0
X_C = 0
Y_C = 0
Z_C = 0
E_C = 0
MI_X = 'G0X'
MI_Y = 'G0Y'
MI_Z = 'G0Z'
MI_E = 'G0E'
MY = 'Y'
MZ = 'Z'
MEX = 'E'
MS =  'F'
ML = '\n'
ME = 'F300\n'
XM = ' X:'
YM = ' Y:'
ZM = ' Z:'
EM = ' E:'
SPEEDM = ' SPEED:'
JOGM = ' JOG:'
SC = '*'
NSC = '_'
axis_status = 0
menu_status = 0

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('EDELCLONE', 0, 0)       
oled.show()
time.sleep(2)

def updatedisplay():
    oled.fill(0)
    oled.show()
    if menu_status == 0:
        if axis_status == 0:
            xy_string = SC + XM + str(X_P) + YM + str (Y_P)
        else:
            xy_string = NSC + XM + str(X_P) + YM + str (Y_P)
        oled.text(xy_string, 0, 0)
        if axis_status == 0:
            ze_string = NSC + ZM + str(Z_P) + EM + str (E_P)
        else:
            ze_string = SC + ZM + str(Z_P) + EM + str (E_P)
        oled.text(ze_string, 0, 10)
        oled.show()
    if menu_status == 1:
        speed_string = SPEEDM + str(SPEED_P)
        oled.text(speed_string, 0, 20)
        jog_string = JOGM + str(INCREMENT)
        oled.text(jog_string, 0, 30)
        oled.show()
    if menu_status == 2:
        oled.text('Save POS A?', 0, 20)
        oled.show()
    if menu_status == 3:
        oled.text('Save POS B?', 0, 20)
        oled.show()
    if menu_status == 4:
        oled.text('MOVE A', 0, 20)
        oled.show()
    if menu_status == 5:
        oled.text('MOVE B', 0, 20)
        oled.show()
    if menu_status == 6:
        oled.text('MOVE A-B', 0, 20)
        oled.show()
    if menu_status == 7:
        oled.text('MOVE A-B-A', 0, 20)
        oled.show()
    if menu_status == 8:
        oled.text('RESET ENDSTOPS?', 0, 20)
        oled.show()
    if menu_status == 9:
        oled.text('PWROFF STEPPERS?', 0, 20)
        oled.show()

def getposition():
    uart.write('M114\n')
    time.sleep(0.2)
    posicion = uart.read()
    pos_x = 0
    pos_y = 0
    pos_z = 0
    pos_e = 0
    pos_c = 0
    #print(posicion)
    for index in range(len(posicion)):
        if posicion[index] == letra_x:
            pos_x = index
        elif posicion[index] == letra_y:
            pos_y = index
        elif posicion[index] == letra_z:
            pos_z = index
        elif posicion[index] == letra_e:
            pos_e = index
        elif posicion[index] == letra_c:
            pos_c = index
            break
    posicion_xstr = ''
    posicion_ystr = ''
    posicion_zstr = ''
    posicion_estr = ''
    
    for index_x in range(pos_x+2,pos_y-1):
        posicion_xstr = posicion_xstr + chr(posicion[index_x])
    X_Pa = float(posicion_xstr)
    
    for index_y in range(pos_y+2,pos_z-1):
        posicion_ystr = posicion_ystr + chr(posicion[index_y])
    Y_Pa = float(posicion_ystr)
    for index_z in range(pos_z+2,pos_e-1):
        posicion_zstr = posicion_zstr + chr(posicion[index_z])
    Z_Pa = float(posicion_zstr)
    for index_e in range(pos_e+2,pos_c-1):
        posicion_estr = posicion_estr + chr(posicion[index_e])
    E_Pa = float(posicion_estr)
    return X_Pa,Y_Pa,Z_Pa,E_Pa
        
X_P,Y_P,Z_P,E_P = getposition()
updatedisplay()
            
while True:
    
    if not b_up.value():
        if menu_status == 0:
            if axis_status == 0:
                Y_P = Y_P + INCREMENT
                ALLMSG = MI_Y + str(Y_P) + ME
                uart.write(ALLMSG)
                uart.read()
            if axis_status == 1:
                E_P = E_P + INCREMENT
                ALLMSG = MI_E + str(E_P) + ME
                uart.write(ALLMSG)
                uart.read()
        if menu_status == 1:
            SPEED_P = SPEED_P + 10
        updatedisplay()
        time.sleep(0.2)
        
    if not b_down.value():
        if menu_status == 0:
            if axis_status == 0:
                Y_P = Y_P - INCREMENT
                ALLMSG = MI_Y + str(Y_P) + ME
                uart.write(ALLMSG)
                uart.read()
            if axis_status == 1:
                E_P = E_P - INCREMENT
                ALLMSG = MI_E + str(E_P) + ME
                uart.write(ALLMSG)
                uart.read()
        if menu_status == 1:
            SPEED_P = SPEED_P - 10
        updatedisplay()
        time.sleep(0.2)
        
    if not b_right.value():
        if menu_status == 0:
            if axis_status == 0:
                X_P = X_P + INCREMENT
                ALLMSG = MI_X + str(X_P) + ME
                uart.write(ALLMSG)
                uart.read()
            if axis_status == 1:
                Z_P = Z_P + INCREMENT
                ALLMSG = MI_Z + str(Z_P) + ME
                uart.write(ALLMSG)
                uart.read()
        if menu_status == 1:
            if INCREMENT == 1.0:
                INCREMENT = 10.0
            elif INCREMENT == 10.0:
                INCREMENT = 0.1
            elif INCREMENT == 0.1:
                INCREMENT = 1.0
        updatedisplay()
        time.sleep(0.2)
        
    if not b_left.value():
        if menu_status == 0:
            if axis_status == 0:
                X_P = X_P - INCREMENT
                ALLMSG = MI_X + str(X_P) + ME
                uart.write(ALLMSG)
                uart.read()
            if axis_status == 1:
                Z_P = Z_P - INCREMENT
                ALLMSG = MI_Z + str(Z_P) + ME
                uart.write(ALLMSG)
                uart.read()
        if menu_status == 1:
            if INCREMENT == 1.0:
                INCREMENT = 0.1
            elif INCREMENT == 10.0:
                INCREMENT = 1.0
            elif INCREMENT == 0.1:
                INCREMENT = 10.0
        updatedisplay()
        time.sleep(0.2)
        
    if not b_mid.value():
        if menu_status == 0:
            if axis_status == 0:
                axis_status = 1
            else:
                axis_status = 0
        elif menu_status == 1:
            donot = 0
        elif menu_status == 2:
            X_A = X_P
            Y_A = Y_P
            Z_A = Z_P
            E_A = E_P
            oled.text('POS A SAVED', 0, 30)
            oled.show()
            time.sleep(1)
            menu_status = 0
        elif menu_status == 3:
            X_B = X_P
            Y_B = Y_P
            Z_B = Z_P
            E_B = E_P
            oled.text('POS B SAVED', 0, 30)
            oled.show()
            time.sleep(1)
            menu_status = 0
        elif menu_status == 4:
            ALLMSG = 'G0E' + str(E_A) + 'F' + str(SPEED_P) + 'X' + str(X_A) + 'Y' + str(Y_A) + 'Z' + str(Z_A) + '\n'
            uart.write(ALLMSG)
            uart.read()
            X_P = X_A
            Y_P = Y_A
            Z_P = Z_A
            E_P = E_A
            menu_status = 5
        
        elif menu_status == 5:
            ALLMSG = 'G0X' + str(X_B) + 'Y' + str(Y_B) + 'Z' + str(Z_B) + 'E' + str(E_B) + 'F' + str(SPEED_P) + '\n'
            uart.write(ALLMSG)
            uart.read()
            X_P = X_B
            Y_P = Y_B
            Z_P = Z_B
            E_P = E_B
            menu_status = 4
        
        elif menu_status == 6:
            ALLMSG = 'G0X' + str(X_A) + 'Y' + str(Y_A) + 'Z' + str(Z_A) + 'E' + str(E_A) + 'F' + str(SPEED_P) + '\n'
            uart.write(ALLMSG)
            uart.read()
            time.sleep(1)
            ALLMSG = 'G0X' + str(X_B) + 'Y' + str(Y_B) + 'Z' + str(Z_B) + 'E' + str(E_B) + 'F' + str(SPEED_P) + '\n'
            uart.write(ALLMSG)
            uart.read()
            X_P = X_B
            Y_P = Y_B
            Z_P = Z_B
            E_P = E_B
        
        elif menu_status == 7:
            ALLMSG = 'G0X' + str(X_A) + 'Y' + str(Y_A) + 'Z' + str(Z_A) + 'E' + str(E_A) + 'F' + str(SPEED_P) + '\n'
            uart.write(ALLMSG)
            uart.read()
            time.sleep(1)
            ALLMSG = 'G0X' + str(X_B) + 'Y' + str(Y_B) + 'Z' + str(Z_B) + 'E' + str(E_B) + 'F' + str(SPEED_P) + '\n'
            uart.write(ALLMSG)
            uart.read()
            time.sleep(1)
            ALLMSG = 'G0X' + str(X_A) + 'Y' + str(Y_A) + 'Z' + str(Z_A) + 'E' + str(E_A) + 'F' + str(SPEED_P) + '\n'
            uart.write(ALLMSG)
            uart.read()
            X_P = X_A
            Y_P = Y_A
            Z_P = Z_A
            E_P = E_A
        
        elif menu_status == 8:
            ALLMSG = 'M121\n'
            uart.write(ALLMSG)
            uart.read()
            menu_status = 0
            
        elif menu_status == 9:
            ALLMSG = 'M18\n'
            uart.write(ALLMSG)
            uart.read()
            menu_status = 0
        
        updatedisplay()
        time.sleep(0.5)
        
    if not b_reset.value():
        menu_status = menu_status + 1
        if menu_status > 10:
            menu_status = 10
        updatedisplay()
        time.sleep(0.5)
    
    if not b_set.value():
        menu_status = menu_status - 1
        if menu_status < 0:
            menu_status = 0
        updatedisplay()
        time.sleep(0.5)
