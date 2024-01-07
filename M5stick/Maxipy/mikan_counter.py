import time, sensor, image,lcd
from fpioa_manager import fm, board_info
import KPU as kpu
from machine import UART

# init camera
clock = time.clock()
lcd.init()
lcd.direction(lcd.YX_LRUD)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.run(1)

# GPIO_UART
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len=4096)

#classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
#task = kpu.load("/sd/model/20class.kmodel")
z
classes = ['aeroplane', 'bicycle', 'mikan', 'mikan1', 'bottle', 'bus', 'car', 'mikan2', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task = kpu.load("/sd/model/20class.kmodel")

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
# Anchor data is for bbox, extracted from the training sets.
kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

while True:
    clock.tick()
    img = sensor.snapshot()
    code_obj = kpu.run_yolo2(task, img)
    count=0
    if code_obj: # object detected
        max_id = 0
        max_rect = 0
        for i in code_obj:
            if classes[i.classid()] == 'mikan':
                count+=1
            if classes[i.classid()] == 'mikan1':
                count+=1
            if classes[i.classid()] == 'mikan2':
                count+=1
            img.draw_rectangle(i.rect())
            text = ' ' + classes[i.classid()] + ' (' + str(int(i.value()*100)) + '%) '
            for x in range(-1,2):
                for y in range(-1,2):
                    img.draw_string(x+i.x(), y+i.y()+(i.h()>>1), text, color=(250,205,137), scale=2,mono_space=False)
            img.draw_string(i.x(), i.y()+(i.h()>>1), text, color=(119,48,48), scale=2,mono_space=False)
            id = i.classid()
            rect_size = i.w() * i.h()
            if rect_size > max_rect:
                max_rect = rect_size
                max_id = id
        lcd.draw_string(10,20,str(count))
    # Identification packets
    data_packet = bytearray([0xFF,0xD8,0xEA])
    uart_Port.write(data_packet)
    data = bytearray([count])
    uart_Port.write(data)

    lcd.display(img)
#   Send UART End
uart_Port.deinit()
del uart_Portu
