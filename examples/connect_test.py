import time
from pytactor import VibrotactorArray

ble = VibrotactorArray.get_ble_instance()
vta_1 = VibrotactorArray(ble)
vta_2 = VibrotactorArray(ble)

vta_1.set_all_motors(5)
vta_1.trigger_vib()

vta_1.start_imu()

time.sleep(10)

VibrotactorArray.disconnect_ble_devices(ble)

vta_1 = VibrotactorArray(ble)

time.sleep(10)
