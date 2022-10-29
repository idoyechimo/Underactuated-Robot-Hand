from sympy import sin, cos, pi
import numpy as np



class Finger:

    def __init__(self,ra,rd,rp,kd,kp,pLink,dLink,start_pang,start_dang,c=0,pAngle = 0,dAngle = 0):
        self.rd = rd
        self.rp = rp
        self.pLink = pLink
        self.dLink = dLink
        self.pAngle = start_pang
        self.dAngle = start_dang
        self.kp = kp
        self.kd = kd
        self.ra = ra
        self.start_dang = start_dang
        self.start_pang = start_pang
        self.C = self.ccalc()
        self.checkRatioOfSpringConstants()
        # if not self.EnergyIsMin():
        #     raise Exception("Potential Energy of starting state is not minimal")




    # prints finger's atributes
    def printt(self):
        print([self.ra,self.rd,self.rp,self.pLink,self.dLink,self.pAngle,self.dAngle,self.kp,self.kd])


    def ccalc(self):
        return self.rp * self.start_pang + self.rd * self.start_dang


    #cheks if potential energy of start state is minimal
    def EnergyIsMin(self,tolerance = 0.1):
        # self.cCalc()
        #calculating wanted angles based on C and asuming actuating is the same as at the starting state while using
        # the assumption of minimal potential energy.

        wanted_dang = (self.kp*self.C) / ((self.rp ** 2 / self.rd) * (self.kd + self.kp * (self.rd / self.rp) ** 2))
        wanted_pang = (-self.rd * wanted_dang + self.C) / self.rp

        dangle_term = (self.dAngle >=wanted_dang - tolerance) and (self.dAngle <= wanted_dang + tolerance)
        pangle_term = (self.pAngle >=wanted_pang - tolerance) and (self.pAngle <= wanted_pang + tolerance)

        return dangle_term and pangle_term

    #updating joint angles.
    def actuation(self,aAngle):
        self.dAngle = (self.kp * (self.ra * aAngle + self.C)) / (
                    (self.rp ** 2 / self.rd) * (self.kd + self.kp * (self.rd / self.rp) ** 2))
        self.pAngle = (self.ra * aAngle - self.rd * self.dAngle + self.C) / self.rp

    # option 1: getting angles from a finger object. returns angles for each joint as a resault of a given motor angle change.
    def jointPos(self,aAngle):
        # updating angles
        self.actuation(aAngle)
        return [self.pAngle,self.dAngle]

    # returns fingertip position in reference to the finger's frame
    def fingerTipPos(self,aAngle):
        # updating angles
        self.actuation(aAngle)

        bd = float(self.pAngle + self.dAngle - (pi/2))
        xPos = (self.dLink * cos(bd)) - (self.pLink * sin(self.pAngle))
        yPos = (self.dLink * sin(bd)) + (self.pLink * cos(self.pAngle))
        return np.array([xPos,yPos])


    def fingerJointPos(self,aAngle):
        self.actuation(aAngle)
        x_pos = -self.pLink * sin(self.pAngle)
        y_pos = self.pLink * cos(self.pAngle)
        return np.array([x_pos,y_pos])
        pass


    # option2: the same as the function above but now getting angles from a function input.
    # def fingertippos(self,pangle,dangle):
    #     xPos = (self.pLink * sin(pangle)) + (self.dLink * sin(pangle + dangle))
    #     yPos = (self.pLink * cos(pangle)) + (self.dLink * cos(pangle + dangle))
    #     return np.array([xPos, yPos])


    def wantedSpringConstans(self):
        # (kd/kp)
        # ratio = ((self.C * self.rd) / (abs(self.start_pang) * (self.rp**2)))-(((self.rd)**3)/((self.rp)**4))
        ratio = ((self.C / self.start_dang) -self.rd) * (self.rd/(self.rp**2))
        return ratio

    def checkRatioOfSpringConstants(self,tolerance = 0.1):
        ratio_is_good = ((self.kd / self.kp) <= self.wantedSpringConstans() + tolerance) and ((self.kp / self.kd) >= self.wantedSpringConstans() - tolerance)
        if  ratio_is_good:
            pass
        else:
            self.kd = self.kp * self.wantedSpringConstans()
            # print(f"ratio of spring constants is not right - calculating new kd...")
            # print(f"--> new kd = {self.kd}")
