# working towards a module for 12c devives
# 17-12-12 pcf8574 working
# now working to read reliably on the Raspberry Pi with smbus, need to enable the DAC and
# read the channels sigly not with a block read 28/12/12

import smbus
import time
    
#next class
class pcf8574():
    # 8 bit port expander methods
    __i2c=smbus.SMBus(0)  #set up i2c bus
    
    def __init__(self,address): #checked
        self.__address=address
        # set up for input on all ports - set all bits low
        try:
            self.__inputs=0x00
            self.__i2c.write_byte(self.__address, self.__inputs)
        except IOError:
            self.ChipPresent=False
            #print 'PCF8574 chip not present at address ', address
        else:
            self.ChipPresent=True
                            
    def setinput(self,portnumber): #checked
        # set appropriate bit low and leave others as they are
        __mask = 1<<portnumber
        self.__inputs=self.__inputs ^ __mask
        self.__i2c.write_byte(self.__address, self.__inputs)
              
    def readall(self): #checked
    # read whole port
        return self.__i2c.read_byte(self.__address)

    def readport(self,portnumber): #checked
    # read whole port and extract appropriate bit
        __value=self.__i2c.read_byte(self.__address)
        return (__value & (1<<portnumber)) >> portnumber

    def writeall(self,actualbyte): #checked
    # write to all outputs
        self.__i2c.write_byte(self.__address, actualbyte)

    def writeport(self,portnumber,OneOrZero): #checked
    # write individual port
        if OneOrZero:#set appropriate output high
            self.__inputs=self.__inputs | (1 << portnumber)
        else:#set appropriate output low
            self.__inputs=self.__inputs & (~(1 << portnumber))
        self.__i2c.write_byte(self.__address,self.__inputs )
        
class pcf8591():
# adc and dac
# need to enable the DAC if reading more than one channel. This has implications for power consumption according
#to the data sheet

    __i2c=smbus.SMBus(0)  #set up i2c bus   

    def __init__(self,address,ADCconfig=0,DACenable=1):
        self.__address=address
        #set analogue input configuration , auto increment off for now
        #default is DAC enables and four single ended inputs
        try:
            self.__controlbyte=(DACenable<<6)+(ADCconfig<<4)
            self.__i2c.write_byte(self.__address, self.__controlbyte)
        except IOError:
            self.ChipPresent=False
            #print 'PCF8591 chip not present at address ', address
        else:
            self.ChipPresent=True
        
    def DACwrite(self,value):
        #write to DAC - not right yet 17.12.12
        #enable the DAC in the control register
        self.__controlbyte=(self.__controlbyte & 0x3F) +0x40
        self.__i2c.write_byte_data(self.__address, self.__controlbyte, value)

    def ADCread(self,channelno):
        #select the apprpriate channel in the control register
        self.__controlbyte = (self.__controlbyte & 0xFC) + channelno
        #print self.controlbyte
        self.__i2c.write_byte(self.__address, self.__controlbyte)
        #read first byte from last conversion and loose as it is the reult of a previous conversion
        __value=self.__i2c.read_byte(self.__address)
        #read required byte
        __value=self.__i2c.read_byte(self.__address)
        return __value

    
if __name__=="__main__":
    #set up the two chips, PCF8574 and PCF8591
    
    analogport=pcf8591(0x48)
    print 'PCF8591 chip present ',analogport.ChipPresent    
    digitalport=pcf8574(0x20)
    print 'PCF8574 chip present ',digitalport.ChipPresent    
   
    
        
