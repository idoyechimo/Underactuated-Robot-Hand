import numpy as np
from sympy import sin, cos, pi
import matplotlib.pyplot as plt


class Hand:

    def __init__(self,teta,finger1,finger2,finger3,h1,h2,h3):
        self.h1 = h1
        self.h3 = h3
        self.h2 = h2
        self.teta = teta
        self.finger1 = finger1
        self.finger2 = finger2
        self.finger3 = finger3

    # updating joints positions resaulting from the motor inputs (teta1,teta2,teta3)
    def actionUdate(self,teta1,teta2,teta3):
        self.finger1.actuation(teta1)
        self.finger2.actuation(teta2)
        self.finger3.actuation(teta3)

    # returns a 3x3 np array with each finger's tip pos
    def handTipPos(self,teta1,teta2,teta3):
        # updating joints

        #finger 1 pos:
        x1 = 0
        y1 = self.finger1.fingerTipPos(teta1)[0] - self.h1
        z1 = self.finger1.fingerTipPos(teta1)[1]

        # finger 2:
        x2 = -(-self.finger2.fingerTipPos(teta2)[0] + self.h2) * sin(self.teta)
        y2 = (-self.finger2.fingerTipPos(teta2)[0] + self.h2) * cos(self.teta)
        z2 = self.finger2.fingerTipPos(teta2)[1]

        #finger 3:
        x3 = (-self.finger3.fingerTipPos(teta3)[0] + self.h2) * sin(self.teta)
        y3 = (-self.finger3.fingerTipPos(teta3)[0] + self.h2) * cos(self.teta)
        z3 = self.finger3.fingerTipPos(teta3)[1]

        # returns 3x3 numpy array with each finger's tip pos
        posMat = np.array([[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]])
        return posMat

    def handJointsPos(self,teta1,teta2,teta3):
        # finger1:
        x1 = 0
        y1 = self.finger1.fingerJointPos(teta1)[0] - self.h1
        z1 = self.finger1.fingerJointPos(teta1)[1]

        # finger 2:
        x2 = -(-self.finger2.fingerJointPos(teta2)[0] + self.h2) * sin(self.teta)
        y2 = (-self.finger2.fingerJointPos(teta2)[0] + self.h2) * cos(self.teta)
        z2 = self.finger2.fingerJointPos(teta2)[1]

        # finger 3:
        x3 = (-self.finger3.fingerJointPos(teta3)[0] + self.h2) * sin(self.teta)
        y3 = (-self.finger3.fingerJointPos(teta3)[0] + self.h2) * cos(self.teta)
        z3 = self.finger3.fingerJointPos(teta3)[1]

        jointPosMat = np.array([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]])
        return jointPosMat

    def baseCordinates(self,teta1,teta2,teta3):
        # finger1:
        x1 = 0
        y1 = -self.h1
        z1 = 0

        #finger2:
        x2 = -(self.h2) * sin(self.teta)
        y2 = (self.h2) * cos(self.teta)
        z2 = 0

        #finger3:
        x3 = (self.h2) * sin(self.teta)
        y3 = (self.h2) * cos(self.teta)
        z3 = 0
        basepose = np.array([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]])

        return basepose

    #plot the state of the hand after actuating the motors with the given angles
    def plotData(self,teta1,teta2,teta3):
        x_tip_data = [line[0] for line in self.handTipPos(teta1, teta2, teta3)]
        y_tip_data = [line[1] for line in self.handTipPos(teta1, teta2, teta3)]
        z_tip_data = [line[2] for line in self.handTipPos(teta1, teta2, teta3)]

        x_joint_data = [line[0] for line in self.handJointsPos(teta1, teta2, teta3)]
        y_joint_data = [line[1] for line in self.handJointsPos(teta1, teta2, teta3)]
        z_joint_data = [line[2] for line in self.handJointsPos(teta1, teta2, teta3)]

        x_base_data = [line[0] for line in self.baseCordinates(teta1, teta2, teta3)]
        y_base_data = [line[1] for line in self.baseCordinates(teta1, teta2, teta3)]
        z_base_data = [line[2] for line in self.baseCordinates(teta1, teta2, teta3)]

        x_data = x_base_data + x_joint_data + x_tip_data
        y_data = y_base_data + y_joint_data + y_tip_data
        z_data = z_base_data + z_joint_data + z_tip_data

        finger1_data = [[self.baseCordinates(teta1, teta2, teta3)[0][0], self.handJointsPos(teta1, teta2, teta3)[0][0],
                         self.handTipPos(teta1, teta2, teta3)[0][0]],
                        [self.baseCordinates(teta1, teta2, teta3)[0][1], self.handJointsPos(teta1, teta2, teta3)[0][1],
                         self.handTipPos(teta1, teta2, teta3)[0][1]],
                        [self.baseCordinates(teta1, teta2, teta3)[0][2], self.handJointsPos(teta1, teta2, teta3)[0][2],
                         self.handTipPos(teta1, teta2, teta3)[0][2]]]

        finger2_data = [[self.baseCordinates(teta1, teta2, teta3)[1][0], self.handJointsPos(teta1, teta2, teta3)[1][0],
                         self.handTipPos(teta1, teta2, teta3)[1][0]],
                        [self.baseCordinates(teta1, teta2, teta3)[1][1], self.handJointsPos(teta1, teta2, teta3)[1][1],
                         self.handTipPos(teta1, teta2, teta3)[1][1]],
                        [self.baseCordinates(teta1, teta2, teta3)[1][2], self.handJointsPos(teta1, teta2, teta3)[1][2],
                         self.handTipPos(teta1, teta2, teta3)[1][2]]]

        finger3_data = [[self.baseCordinates(teta1, teta2, teta3)[2][0], self.handJointsPos(teta1, teta2, teta3)[2][0],
                         self.handTipPos(teta1, teta2, teta3)[2][0]],
                        [self.baseCordinates(teta1, teta2, teta3)[2][1], self.handJointsPos(teta1, teta2, teta3)[2][1],
                         self.handTipPos(teta1, teta2, teta3)[2][1]],
                        [self.baseCordinates(teta1, teta2, teta3)[2][2], self.handJointsPos(teta1, teta2, teta3)[2][2],
                         self.handTipPos(teta1, teta2, teta3)[2][2]]]

        fingers_data_lines = [finger1_data,finger2_data,finger3_data]

        # ax = plt.axes(projection="3d")
        # plt.xlabel("X axis label")
        # plt.ylabel("Y axis label")
        #
        # # ax.scatter(x_data, y_data, z_data)
        # ax.plot(finger1_data[0], finger1_data[1], finger1_data[2], label="finger 1")
        # ax.plot(finger2_data[0], finger2_data[1], finger2_data[2], label="finger 2")
        # ax.plot(finger3_data[0], finger3_data[1], finger3_data[2], label="finger 3")

        # plt.show()
        return fingers_data_lines

    def step(self,state1,state2):
        state1_data = self.plotData(state1[0],state1[1],state1[2])
        state2_data = self.plotData(state2[0],state2[1],state2[2])

        fig = plt.figure(figsize=plt.figaspect(0.5))

        # ax1 = plt.axes(projection="3d")

        ax1 = fig.add_subplot(1, 2, 1, projection='3d')

        plt.xlabel("X axis label")
        plt.ylabel("Y axis label")
        ax1.set_title("Start state")

        ax1.plot(state1_data[0][0], state1_data[0][1], state1_data[0][2], label="finger 1")
        ax1.plot(state1_data[1][0], state1_data[1][1], state1_data[1][2], label="finger 2")
        ax1.plot(state1_data[2][0], state1_data[2][1], state1_data[2][2], label="finger 3")


        ax2 = fig.add_subplot(1, 2, 2, projection='3d')

        plt.xlabel("X axis label")
        plt.ylabel("Y axis label")
        ax2.set_title("End state")

        ax2.plot(state2_data[0][0], state2_data[0][1], state2_data[0][2], label="finger 1")
        ax2.plot(state2_data[1][0], state2_data[1][1], state2_data[1][2], label="finger 2")
        ax2.plot(state2_data[2][0], state2_data[2][1], state2_data[2][2], label="finger 3")
        plt.tight_layout()


        plt.show()
