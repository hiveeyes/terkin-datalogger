import time

from machine import I2C, Pin

# Get I2C bus
i2c = I2C(scl = Pin(22), sda = Pin(21), freq=400000)

MAX17043_ADDR = 0x36
MAX17043_VCELL = 0x02
MAX17043_SOC = 0x04
MAX17043_MODE = 0x06
MAX17043_VERSION = 0x08
MAX17043_CONFIG = 0x0c
MAX17043_COMMAND = 0xfe

class DFRobot_MAX17043():
  
  def __init__(self):
    pass
  
  def begin(self):
    self.write16(MAX17043_COMMAND, 0x5400)
    time.sleep(0.01)
    if self.read16(MAX17043_CONFIG) == 0x971c:
      self.write16(MAX17043_MODE, 0x4000)
      time.sleep(0.01)
      self.write16(MAX17043_CONFIG, 0x9700)
      return 0
    else:
      return -1
      
  def readVoltage(self):
    return (1.25 * (self.read16(MAX17043_VCELL) >> 4))
  
  def readPercentage(self):
    tmp = self.read16(MAX17043_SOC)
    return ((tmp >> 8) + 0.003906 * (tmp & 0x00ff))

  def setInterrupt(self, per):
    if per > 32:
      per = 32
    elif per < 1:
      per = 1
    per = 32 - int(per)
    self.writeRegBits(MAX17043_CONFIG, per, 0x01f, 0)

  def clearInterrupt(self):
    self.writeRegBits(MAX17043_CONFIG, 0, 0x01, 5)
    
  def setSleep(self):
    self.writeRegBits(MAX17043_CONFIG, 1, 0x01, 7)
    
  def setWakeUp(self):
    self.writeRegBits(MAX17043_CONFIG, 0, 0x01, 7)
  
  def write16(self, reg, dat):
    buf = bytearray(2)
    buf[0] = dat >> 8
    buf[1] = dat & 0x00ff
    i2c.writeto_mem(MAX17043_ADDR, reg, buf)
    
  def read16(self, reg):
    buf = i2c.readfrom_mem(MAX17043_ADDR, reg, 2)
    return ((buf[0] << 8) | buf[1])
  
  def writeRegBits(self, reg, dat, bits, offset):
    tmp = self.read16(reg)
    tmp = (tmp & (~(bits << offset))) | (dat << offset)
    self.write16(reg, tmp)

