import RPi.GPIO as GPIO
from flask import Flask,render_template
import time
import requests

# pin number
switch = 12
led = 11
servo = 3
flag=1

# set up
app = Flask(__name__,template_folder='templates')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(servo,GPIO.OUT)
GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(servo,50)
pwm.start(7.5)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/clicked")
def clicked():
    LightTurnOn()
    LightTurnOff()
    

def LightTurnOn():
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.5)

def LightTurnOff():
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.5)

def ServoMove():
    global flag
    pwm.start(7.5)
    if flag==1:
        pwm.ChangeDutyCycle(7.5)
        time.sleep(0.2)
        flag=0
    else:
        #pwm.ChangeDutyCycle(2.5)
        #time.sleep(0.2)
        pwm.ChangeDutyCycle(12.5)
        time.sleep(1)
        flag=1
    pwm.stop()


def SwitchSetup():
    while True:
        input_state = GPIO.input(switch)
        if input_state == False:
            print("move");
            ServoMove()
            time.sleep(0.2)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)
    SwitchSetup()


# cleanup
pwm.stop()
GPIO.cleanup()
