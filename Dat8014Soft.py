# Import the required modules
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet import reactor
from threading import Thread
# from rtdSoft import updating_writer


# Initialize your data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17] * 100),  # 100 discrete inputs initialized to 17
    co=ModbusSequentialDataBlock(0, [17] * 100),  # 100 coils initialized to 17
    hr=ModbusSequentialDataBlock(0, [17] * 100),  # 100 holding registers initialized to 17
    ir=ModbusSequentialDataBlock(0, [17] * 100),  # 100 input registers initialized to 17
    zero_mode=True  # use zero-based addressing
)

context = ModbusServerContext(slaves=store, single=True)  # Create a server context

# Initialize the server information
identity = ModbusDeviceIdentification()  # Create an identity object
identity.VendorName = 'Datexel'  # Set the vendor name
identity.ProductCode = 'DAT8014'  # Set the product code
identity.VendorUrl = 'https://www.datexel.it/en/'  # Set the vendor url
identity.ProductName = 'ADC Datexel DAT8014 - Modbus'  # Set the product name
identity.ModelName = 'DAT8014'  # Set the model name
identity.MajorMinorRevision = '1.6'  # Set the revision

# Run the server
StartTcpServer(context, identity=identity, address=("127.0.0.1", 5020),
               allow_reuse_address=True, defer_reactor_run=True)

# Start a background thread to update the context every second
# thread = Thread(target=updating_writer, args=(context,))
# thread.start()

from rtdSoft import UpdatingWriter
rtd_thread = UpdatingWriter(context)
rtd_thread.start()

# Start the reactor loop
reactor.run()
