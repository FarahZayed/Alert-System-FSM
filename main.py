# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class AlertFSM:

    def __init__(self):
        self.states = ['idle', 'DetectingFire', 'FireAlert','ownerNotification','buzzerRinging']
        self.current_state = 'idle'

    def transition(self,event):
       transitions = {
            'smokeDetection': {'idle': 'DetectingFire'},
            'smokepresisted': {'DetectingFire': 'DetectingFire'},
            'Alert':{'DetectingFire':'FireAlert'},
            'ringBuzzer':{'FireAlert':'buzzerRinging'},
            'sendNotification':{'buzzerRinging':'ownerNotification'},
            'reset':{'ownerNotification':'idle'},
       }
       if self.current_state in transitions[event]:
        if(self.current_state=='idle'):
            self.timer=0
            self.current_state = transitions[event][self.current_state]
        elif (self.current_state=='DetectingFire'):
            self.timer +=1
            if(self.timer<3):
                self.current_state == 'DetectingFire'
            else:
                self.current_state = transitions[event][self.current_state]
        else:
            self.current_state = transitions[event][self.current_state]
        #self.current_state = transitions[event][self.current_state]
        print(f"Transitioning to {self.current_state} state.")
       else:
        print(f"No transition defined for event {event} in {self.current_state} state.")

fsm= AlertFSM()

fsm.transition('smokeDetection')
fsm.transition('smokepresisted')
fsm.transition('smokepresisted')
fsm.transition('smokepresisted')
fsm.transition('smokepresisted')
fsm.transition('smokepresisted')
fsm.transition('smokepresisted')
fsm.transition('Alert')
fsm.transition('ringBuzzer')
fsm.transition('sendNotification')
fsm.transition('reset')


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
