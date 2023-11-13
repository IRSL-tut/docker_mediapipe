lCol=[0.2, 0.7, 0.2] ## color link
jCol=[0.7, 0.2, 0.2] ## color joint
jR=0.008 # joint radius
jH=0.018 # joint length
tipR=0.01 # tip radius

length_upper_arm = 0.25
length_lower_arm = 0.25
length_upper_leg = 0.4
length_lower_leg = 0.4

arm_offset=0.3
leg_offset=0.1

rb=RobotBuilder()

rb.makeBox(0.005)
lroot=rb.createLinkFromShape(name='Root', root=True, density=400.0)
jid=0

### upper_body
## left_arm
pos=npa([0., arm_offset, 0.])
lcur=lroot
prefix='left'
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_shoulder_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_shoulder_roll'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
upper_arm_dir = npa([0.,0., -length_upper_arm])
rb.makeLineAlignedShape(pos,  pos + upper_arm_dir, size=0.004, shape='Capsule', color=lCol)
lcur=rb.createLinkFromShape(name='{}_shoulder_yaw'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

pos = pos + upper_arm_dir
lower_arm_dir = npa([0.,0., -length_lower_arm])
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeLineAlignedShape(pos,  pos + lower_arm_dir, size=0.004, shape='Capsule', color=lCol)
rb.makeSphere(tipR, color=jCol).locate(pos + lower_arm_dir)
lcur=rb.createLinkFromShape(name='{}_elbow_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

## right_arm
pos=npa([0., - arm_offset, 0.])
lcur=lroot
prefix='right'
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_shoulder_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_shoulder_roll'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
upper_arm_dir = npa([0.,0., -length_upper_arm])
rb.makeLineAlignedShape(pos,  pos + upper_arm_dir, size=0.004, shape='Capsule', color=lCol)
lcur=rb.createLinkFromShape(name='{}_shoulder_yaw'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

pos = pos + upper_arm_dir
lower_arm_dir = npa([0.,0., -length_lower_arm])
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeLineAlignedShape(pos,  pos + lower_arm_dir, size=0.004, shape='Capsule', color=lCol)
rb.makeSphere(tipR, color=jCol).locate(pos + lower_arm_dir)
lcur=rb.createLinkFromShape(name='{}_elbow_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

### lower_body
## left_leg
pos=npa([0., leg_offset, -0.6])
lcur=lroot
prefix='left'
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_hip_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_hip_roll'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
upper_leg_dir = npa([0.,0., - length_upper_leg])
rb.makeLineAlignedShape(pos,  pos + upper_leg_dir, size=0.004, shape='Capsule', color=lCol)
lcur=rb.createLinkFromShape(name='{}_hip_yaw'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

pos = pos + upper_leg_dir
lower_leg_dir = npa([0.,0., - length_lower_leg])
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeLineAlignedShape(pos,  pos + lower_leg_dir, size=0.004, shape='Capsule', color=lCol)
rb.makeSphere(tipR, color=jCol).locate(pos + lower_leg_dir)
lcur=rb.createLinkFromShape(name='{}_knee_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1


## right_leg
pos=npa([0., - leg_offset, -0.6])
lcur=lroot
prefix='right'
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_hip_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
lcur=rb.createLinkFromShape(name='{}_hip_roll'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(PI/2, coordinates.X).locate(pos, coordinates.wrt.world)
upper_leg_dir = npa([0.,0., - length_upper_leg])
rb.makeLineAlignedShape(pos,  pos + upper_leg_dir, size=0.004, shape='Capsule', color=lCol)
lcur=rb.createLinkFromShape(name='{}_hip_yaw'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1

pos = pos + upper_leg_dir
lower_leg_dir = npa([0.,0., - length_lower_leg])
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeCylinder(jR, jH, color=jCol).rotate(0, coordinates.X).locate(pos, coordinates.wrt.world)
rb.makeLineAlignedShape(pos,  pos + lower_leg_dir, size=0.004, shape='Capsule', color=lCol)
rb.makeSphere(tipR, color=jCol).locate(pos + lower_leg_dir)
lcur=rb.createLinkFromShape(name='{}_knee_pitch'.format(prefix), parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1
