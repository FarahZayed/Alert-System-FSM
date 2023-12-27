import tkinter as tk
import tkinter.messagebox
from tkinter import *
import math
import simpleaudio as sa

class AlertFSM:
    def __init__(self):
        self.states = ['idle', 'DetectingFire', 'FireAlert', 'ownerNotification', 'buzzerRinging','water','fire on/off','911']
        self.current_state = 'idle'
        self.timer = 0  # Initialize timer for fire detection

    def transition(self, event):
        transitions = {
            'default':{'idle':'idle'},
            'smokeDetection': {'idle': 'DetectingFire'},
            'smokeended':{'DetectingFire':'idle'},
            'smokepresisted': {'DetectingFire': 'DetectingFire'},
            'Alert': {'DetectingFire': 'FireAlert'},
            'ringBuzzer': {'FireAlert': 'buzzerRinging'},
            'sendNotification': {'buzzerRinging': 'ownerNotification'},
            'sprinkleWater':{'ownerNotification':'water'},
            'checkfire':{'water':'fire on/off'},
            'fireoff':{'fire on/off':'idle'},
            'fireon':{'fire 0n/off':'911'},
            '911alerted':{'911':'idle'}
        }

        if self.current_state in transitions[event]:
            if self.current_state == 'idle':
                self.timer = 0
                self.current_state = transitions[event][self.current_state]
            elif(self.timer>100):
                self.current_state = transitions[event][self.current_state]
            #
            elif self.current_state == 'DetectingFire':
                # Update timer value based on the slider
                self.current_state = transitions[event][self.current_state]
            else:
                self.current_state = transitions[event][self.current_state]
            print(f"Transitioning to {self.current_state} state.")
        else:
            print(f"No transition defined for event {event} in {self.current_state} state.")

fsm = AlertFSM()

def on_slider_change(value):
    my_upd(value)
    # Update timer value in AlertFSM based on slider value
    fsm.timer = int(value)
    #print(f"Timer set to: {fsm.timer}")
    if (fsm.timer > 0 and fsm.timer < 58):
        labelGood.config(text="Idle")
        print("idle")
    elif(fsm.timer>=58 and fsm.timer<90):
        fsm.transition("smokeDetection")
        labelGood.config(text="Smoke Detection")
        labelGood.place(x=132, y=290)
        print("somked")
    elif(fsm.timer>=90 and fsm.timer<120):
        fsm.transition("smokepresisted")
        labelGood.config(text="Smoke Presisted")
        print("smokep")
    elif (fsm.timer >= 120 and fsm.timer <= 180):
        fsm.transition('Alert')
        fsm.transition('ringBuzzer')
        fsm.transition('sendNotification')
        if (fsm.timer >= 120 and fsm.timer < 155):
            fsm.transition("sprinkleWater")
            fsm.transition("checkfire")
            fsm.transition("fireoff")
            labelGood.config(text="Handled by water")
            labelGood.place(x=165, y=290)
            tkinter.messagebox.showinfo("Fire", "FIRE DETECTION")
            for i in range(10):
                if i==5:
                    break
            tkinter.messagebox.showinfo("Fire", "Fire is off")
            slider.set(0)
            my_upd(0)
        else:
            fsm.transition("sprinkleWater")
            fsm.transition("checkfire")
            fsm.transition("fireon")
            fsm.transition("911alerted")
            labelGood.config(text="Emergency")
            labelGood.place(x=175, y=290)
            tkinter.messagebox.showinfo("Fire", "FIRE DETECTION")
            for i in range(10):
                if i == 5:
                    break
            tkinter.messagebox.showwarning("Fire", "CALL 911")
            play_sound()
            slider.set(0)
            my_upd(0)
# Slider widget
root = tk.Tk()
root.geometry("686x391")
root.resizable(False, False)
root.title("Fire Alert")  # Set the title of the window
root.configure(bg='white')

width,height=410,310 # set the variables
d=str(width)+"x"+str(height+40)
root.geometry(d)

arc_w=50 # width of the arc
x1,y1,x2,y2=35,35,355,355 # dimensions for the arc
x,y,r=195,195,135
c1=tk.Canvas(root,width=width-10,height=height-50,bg='#FFFFFF',highlightbackground="white")
c1.grid(row=0,column=0)

res=1
def on_slider_click(event):
    # Calculate the slider position based on the click event
    position = event.x / slider_width
    print(event.x)
    if(position==0):
        slider.set(position)
    else:
        slider.set(position-30)

def my_upd(value):
    global line
    in_radian = math.radians(slider.get()) # scale value in radian
    if(slider.get()==0):
        labelGood.config(text="Idle")
    c1.delete(line) # delete the pointer
    line=c1.create_line(x,y,(x+r*-math.cos(in_radian)),(y-r*math.sin(in_radian)),width=6,arrow='last')

def my_updd(d):
    change=int((255/180)*d) # Jump in colour value
    color_c='#%02x%02x%02x' % (255-change, change,0)
    return color_c
res=1 # resolution or steps
for d in range(0,180,res):
    c1.create_arc(x1, y1,x2,y2, start=d, extent=res+1,outline=my_updd(d),
        width=arc_w,style=tk.ARC)

# small circle at center
c1.create_oval(x-10,y-10,x+10,y+10,fill='black')
in_radian=math.radians(180) # getting radian value
line=c1.create_line(x,y,(x+r*math.cos(in_radian)),(y-r*math.sin(in_radian)),width=6,arrow='last')

# Slider configuration
# length_label = Label(root, text="Fire")
slider = tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, command=on_slider_change,length=300,bg='white',showvalue=False,highlightbackground="white",troughcolor="red", activebackground="blue")
slider.grid(row=2,column=0)
slider_width = slider.winfo_width()
print(slider_width)
slider.bind("<Button-1>", on_slider_click)
labelGood=tk.Label(root,font=("Bernard MT Condensed", 16),bg='white')
labelGood.place(x=175, y=290)

def play_sound():
    try:
        wave_obj = sa.WaveObject.from_wave_file("buzzer.mp3")  # Replace with the path to your sound file
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait for the sound to finish playing before proceeding
    except Exception as e:
        print("Error occurred:", e)
root.mainloop()