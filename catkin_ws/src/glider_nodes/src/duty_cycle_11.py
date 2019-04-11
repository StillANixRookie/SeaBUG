import RPi.GPIO as GPIO

pin = 11


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, True)

while (1):
    pwm_11 = GPIO.PWM(pin, 1000)
    pwm_11.start(50)
#pwm_11.ChangeDutyCycle(100)
#pwm_11.ChangeDutyCycle(0)
#pwm_11.stop()

GPIO.cleanup()
