from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
import random
import time
from threading import Thread


class UpdatingWriter(Thread):
    def __init__(self, context):
        super().__init__()
        self.daemon = True
        self.context = context

    def run(self):
        while True:
            random_float_1 = random.uniform(1077.9, 1136.1)  # returns a random float between 1077.9 and 1136.1
            new_float = random.uniform(0.2, 1)  # returns a random float between 0.2 and 1.5
            random_float_2 = random_float_1 + new_float

            # Add random_float_1 and random_float_1 as a 16-bit integer to the payload_1 and payload_2
            builder_1 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            builder_2 = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            builder_1.add_16bit_float(random_float_1)
            builder_2.add_16bit_float(random_float_2)
            payload_1 = builder_1.to_registers()
            payload_2 = builder_2.to_registers()
            # Write the payload to register 0
            # context.setValues(3, 0, payload_1)
            self.context[0x00].setValues(3, 0, payload_1)
            # Write the payload to register 1
            # context.setValues(3, 1, payload_2)
            self.context[0x00].setValues(3, 1, payload_2)
            print(f"DAT8014 running... {payload_1} | {payload_2}")
            time.sleep(0.5)
