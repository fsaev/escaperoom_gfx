import serial
from enum import Enum

class com_states(Enum):
    START_BYTE = 0
    COMMAND = 1
    PAYLOAD_SIZE = 2
    PAYLOAD = 3
    CHECKSUM_MSB = 4
    CHECKSUM_LSB = 5


def fletcher16_checksum(data):
    sum1 = 0
    sum2 = 0

    for d in data:
        sum1 = (sum1 + d) % 255
        sum2 = (sum2 + sum1) % 255

    checksum = (sum2 << 8) | sum1

    return checksum

class Com(object):
    com_state = com_states.START_BYTE
    command = 0
    payload_size = 0
    payload = []
    recv_checksum = 0

    package_queue = []

    def __init__(self, comport):
        self.ser = serial.Serial(comport, 115200, timeout=0)

    def get_package(self):
        if(len(self.package_queue)):
            return self.package_queue.pop()
        else:
            return None


    def tick_com(self):
        dat = self.ser.read(1)
        if(dat == b''):
            return

        if(self.com_state == com_states.START_BYTE):
            if dat == b'\xfe':
                self.payload_size = 0
                self.com_state = com_states.COMMAND
        elif(self.com_state == com_states.COMMAND):
            self.command = int.from_bytes(dat, byteorder='little', signed=False)
            self.com_state = com_states.PAYLOAD_SIZE
        elif(self.com_state == com_states.PAYLOAD_SIZE):
            self.payload_size = int.from_bytes(dat, byteorder='little', signed=False)
            self.payload = []
            self.com_state = com_states.PAYLOAD
        elif(self.com_state == com_states.PAYLOAD):
            self.payload.append(int.from_bytes(dat, byteorder='little', signed=False))
            if(len(self.payload) == self.payload_size):
                self.recv_checksum = 0
                self.com_state = com_states.CHECKSUM_LSB
        elif(self.com_state == com_states.CHECKSUM_LSB):
            self.recv_checksum = int.from_bytes(dat, byteorder='little', signed=False)
            self.com_state = com_states.CHECKSUM_MSB
        elif(self.com_state == com_states.CHECKSUM_MSB):
            self.recv_checksum = self.recv_checksum | (int.from_bytes(dat, byteorder='little', signed=False) << 8)
            if(fletcher16_checksum(self.payload) == self.recv_checksum):
                if(len(self.package_queue) < 1024):
                    self.package_queue.append((self.command, self.payload)) # Store as tuple on the queue
                else:
                    print("Queue overflow, dropping package")
            else:
                print("Rejected package")

            self.com_state = com_states.START_BYTE