import time
from pytactor import VibrotactorArray

ble = VibrotactorArray.get_ble_instance()
vta_1 = VibrotactorArray(ble)

vta_1.set_motor_level(1, 200)
vta_1.trigger_vib()

time.sleep(2)

# motor_level = 5
# for i in range(0, 10):
#     print(f"Writing motor 1 with {motor_level}")
#     vta_1.write_motor_level(1, motor_level)
#     motor_level += 25
#     time.sleep(2)
