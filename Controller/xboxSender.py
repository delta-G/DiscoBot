

###  Need to build up a string of hex digits in ascii representing the 14 bytes of the xbox message
###  Fills this union in the C++ code:

###        union {
# 
#         uint8_t rawBuffer[14];
#         struct {
# 
#             uint16_t checkBytes;
#             uint16_t buttonState;
#             uint8_t leftTrigger;
#             uint8_t rightTrigger;
#             int16_t hatValues[4];
# 
#         } values;
# 
# 
#     } readUnion;

#####   buttonState has the buttons in this order

# enum ButtonMaskEnum {
#         UP = 0x0100,
#         RIGHT = 0x0800,
#         DOWN = 0x0200,
#         LEFT = 0x0400,
#         BACK = 0x2000,
#         START = 0x1000,
#         L3 = 0x4000,
#         R3 = 0x8000,
#         L2 = 0,
#         R2 = 0,
#         L1 = 0x0001,
#         R1 = 0x0002,
# 
#         B = 0x0020,
#         A = 0x0010,
#         X = 0x0040,
#         Y = 0x0080,
# 
#         XBOX = 0x0004,
#         SYNC = 0x0008,
# };

buttonMasks = {
    'UP':0x0100,
    'RIGHT':0x0800,
    'DOWN':0x0200,
    'LEFT':0x0400,
    'BACK':0x2000,
    'START':0x1000,
    'L3':0x4000,
    'R3':0x8000,
    'L2':0,
    'R2':0,
    'L1':0x0001,
    'R1':0x0002,         
    'B':0x0020,
    'A':0x0010,
    'X':0x0040,
    'Y':0x0080,         
    'XBOX':0x0004,
    'SYNC':0x0008
    }



import xbox


def getReading(aJoystick):
    
    aJoystick.refresh()
    raw = aJoystick.reading
    return raw


def getRawString(aJoystick):
    
    raw = getReading(aJoystick)
    
    

    
    
    
    return
    
    
    