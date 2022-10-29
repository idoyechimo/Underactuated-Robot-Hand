from finger import *
from hand import *


# sizes and constants
#----------------------------------------
#----------------------------------------

#link length
pLink = 63.5
dLink = 37.5

#radius sizes
rp = 8
rd = 8
ra = 10.5

#given spring constants
kp = 1
kd = 5.0

#distans of each finger base from the origin
h1 = 30
h2 = 48
h3 = 48

#angle between fingers
teta = 0.95

#starting angles from the solidworks model
pAng = float(pi - 2.21)
dAng = 2.77
#----------------------------------------
#----------------------------------------

# creating 3finger objects
# def __init__(self,ra,rd,rp,kd,kp,pLink,dLink,start_pang,start_dang,c=0,pAngle = 0,dAngle = 0):
fing1 = Finger(ra,rd,rp,kd,kp,pLink,dLink,pAng,dAng)
fing2 = Finger(ra,rd,rp,kd,kp,pLink,dLink,pAng,dAng)
fing3 = Finger(ra,rd,rp,kd,kp,pLink,dLink,pAng,dAng)



#creating a hand object from the 3 finger objects
hand = Hand(teta, fing1, fing2, fing3, h1, h2, h3)

#seting actuation angles for the second state
start1 = 0
start2 = 0
start3 = 0

teta1 = -1
teta2 = -1.5
teta3 = -0.5


state1 = [start1,start2,start3]
state2 = [teta1,teta2,teta3]


hand.step(state1,state2)