#!/usr/bin/env python
# coding: utf-8
#jupyter console --kernel=choreonoid
# # ハンドモデルを作る
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())


# ## パラメータ設定
lCol=[0.2, 0.7, 0.2] ## color link
jCol=[0.7, 0.2, 0.2] ## color joint
jR=0.008 # joint radius
jH=0.018 # joint length
tipR=0.01 # tip radius
lR=0.007 # link radius
palm_y =0.0683 # palm width
palm_y2=0.0363 # palm width
palm_z=0.0856 # palm height
palm_t=lR*2  # palm thickness
thumb_l0=0.0364 # thumb length0
thumb_l1=0.0288 # thumb length1
thumb_l2=0.0233 # thumb length2
fg_l0=0.072 # finger length0
fg_l1=0.046 # finger length1
fg_l2=0.041 # finger length2
scale=1.0 # scale of model

jR*=scale
jH*=scale
tipR*=scale
lR*=scale
palm_y*=scale
palm_z*=scale
palm_t*=scale
thumb_l0*=scale
thumb_l1*=scale
thumb_l2*=scale
fg_l0*=scale
fg_l1*=scale
fg_l2*=scale

jid=0 ## joint-id
rb=RobotBuilder()

# ## 手のひら形状を作る
# makeSphare # 球をつくる
rb.makeLineAlignedShape(npa([0.,0.,0.]),     npa([0.,0.,palm_z]), size=palm_t/2, shape='Capsule', color=lCol)
ang=15*PI/180
rb.makeLineAlignedShape(npa([0.,0.,palm_z]), npa([0., -math.cos(ang)*palm_y, -math.sin(ang)*palm_y + palm_z]), size=palm_t/2, shape='Capsule', color=lCol)
##rb.makeLineAlignedShape(npa([0.,-palm_y,palm_z]), npa([0.,-palm_y,0.]), size=palm_t/2, shape='Capsule', color=lCol)
rb.makeLineAlignedShape(npa([0.,-palm_y2,0.]), npa([0.,0.,0.]), size=palm_t/2, shape='Capsule', color=lCol)
rb.makeSphere(tipR, color=jCol).locate(npa([0., 0., 0.]))

rb.draw.viewAll()
# ルートリンクを作る
lcur=rb.createLinkFromShape(name='Root', root=True, density=400.0)
lroot=lcur

# ## 親指リンクを作る

# thumb0-joint
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(PI/4, coordinates.X).locate(npa([0, -palm_y2, 0]), coordinates.wrt.world)
# thumb0-shape
rb.makeCylinder(jR, jH, color=jCol).rotate(PI/4, coordinates.X).locate(npa([0, -palm_y2, 0]), coordinates.wrt.world) ## rotate-joint-shape
lcur=rb.createLinkFromShape(name='thumb0', parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1


# 第２関節
linkDir=npa([0, -math.sqrt(0.5), math.sqrt(0.5)])
# thumb1-joint
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(npa([0, -palm_y2, 0]), coordinates.wrt.world)
# thumb1-shape
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(npa([0, -palm_y2, 0]), coordinates.wrt.world) ## rotate-joint-shape
rb.makeCapsule(lR, thumb_l0-2*lR, color=lCol).rotate(-PI/4, coordinates.X).locate(npa([0, -palm_y2, 0]) + thumb_l0/2 * linkDir, coordinates.wrt.world) ## shape-body
lcur=rb.createLinkFromShape(name='thumb1', parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1


# 第３関節
pos=npa([0, -palm_y2, 0]) + thumb_l0 * linkDir
# thumb2-joint
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
# thumb2-shape
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world) ## rotate-joint-shape
rb.makeCapsule(lR, thumb_l1-2*lR, color=lCol).rotate(-PI/4, coordinates.X).locate(pos + thumb_l1/2 * linkDir, coordinates.wrt.world) ## shape-body
lcur=rb.createLinkFromShape(name='thumb2', parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1


# 第４関節
pos=npa([0, -palm_y2, 0]) + (thumb_l0 + thumb_l1) * linkDir
# thumb2-joint
rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world)
# thumb2-shape
rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(pos, coordinates.wrt.world) ## rotate-joint-shape
rb.makeCapsule(lR, thumb_l2-2*lR, color=lCol).rotate(-PI/4, coordinates.X).locate(pos + thumb_l2/2 * linkDir, coordinates.wrt.world) ## shape-body
rb.makeSphere(tipR, color=jCol).locate(pos + thumb_l2 * linkDir) ## tip-shape
lcur=rb.createLinkFromShape(name='thumb3', parentLink=lcur, density=400.0, JointId=jid, JointRange=[-PI, PI])
jid += 1


# ## 指を作る
# 指を作るcreateFinger関数を設定して、同じ指を位置を変えて作る
def createFinger(rb, baselink, basepos, jid_base=0, base_name='f', l0=0.05, l1=0.05, l2=0.05, fscale=1.0):
    l0 *= fscale
    l1 *= fscale
    l2 *= fscale
    _jid=jid_base
    rb.createJointShape(jointType=Link.JointType.RevoluteJoint).rotate(-PI/2, coordinates.Z).locate(basepos, coordinates.wrt.world)
    rb.makeCylinder(jR, jH, color=jCol).rotate(-PI/2, coordinates.Z).locate(basepos, coordinates.wrt.world)
    lcur=rb.createLinkFromShape(name=base_name+'_0', parentLink=baselink, density=400.0, JointId=_jid, JointRange=[-PI, PI])
    _jid += 1
    #
    linkDir=npa([0., 0., 1.0])
    rb.createJointShape(jointType=Link.JointType.RevoluteJoint).locate(basepos, coordinates.wrt.world)
    rb.makeCylinder(jR, jH, color=jCol).locate(basepos, coordinates.wrt.world)
    rb.makeCapsule(lR, l0-2*lR, color=lCol).rotate(-PI/2, coordinates.X).locate(basepos + l0/2 * linkDir, coordinates.wrt.world)
    lcur=rb.createLinkFromShape(name=base_name+'_1', parentLink=lcur, density=400.0, JointId=_jid, JointRange=[-PI, PI])
    _jid += 1
    #
    basepos += l0 * linkDir
    rb.createJointShape(jointType=Link.JointType.RevoluteJoint).locate(basepos, coordinates.wrt.world)
    rb.makeCylinder(jR, jH, color=jCol).locate(basepos, coordinates.wrt.world)
    rb.makeCapsule(lR, l1-2*lR, color=lCol).rotate(-PI/2, coordinates.X).locate(basepos + l1/2 * linkDir, coordinates.wrt.world)
    lcur=rb.createLinkFromShape(name=base_name+'_2', parentLink=lcur, density=400.0, JointId=_jid, JointRange=[-PI, PI])
    _jid += 1
    #
    basepos += l1 * linkDir
    rb.createJointShape(jointType=Link.JointType.RevoluteJoint).locate(basepos, coordinates.wrt.world)
    rb.makeCylinder(jR, jH, color=jCol).locate(basepos, coordinates.wrt.world)
    rb.makeCapsule(lR, l2-2*lR, color=lCol).rotate(-PI/2, coordinates.X).locate(basepos + l2/2 * linkDir, coordinates.wrt.world)
    rb.makeSphere(tipR, color=jCol).locate(basepos + l2 * linkDir)## TIP
    lcur=rb.createLinkFromShape(name=base_name+'_3', parentLink=lcur, density=400.0, JointId=_jid, JointRange=[-PI, PI])
    _jid += 1
    return _jid


# 位置を変えて指関節を作る
finger_offset=0.005
org=npa([0, 0, palm_z])
dst=npa([0., -math.cos(ang)*palm_y, -math.sin(ang)*palm_y + palm_z])
off=npa([0, -math.sin(ang),  math.cos(ang)])
ratio=0.0
jid=createFinger(rb, lroot, ratio*org + (1-ratio)*dst, jid_base=jid, base_name='index_finger',
                 l0=0.0353, l1=0.0212, l2=0.0180) ## index-finger
ratio=1.0/3
jid=createFinger(rb, lroot, ratio*org + (1-ratio)*dst + off*0.005 , jid_base=jid, base_name='middle_finger',
                 l0=0.0414, l1=0.0243, l2=0.0191) ## middle-finger
ratio=2.0/3
jid=createFinger(rb, lroot, ratio*org + (1-ratio)*dst + off*0.005, jid_base=jid, base_name='ring_finger',
                 l0=0.0391, l1=0.0233, l2=0.0199)
ratio=1.0
jid=createFinger(rb, lroot, ratio*org + (1-ratio)*dst, jid_base=jid, base_name='pinky',
                 l0=0.0294, l1=0.0191, l2=0.0176)

# ## モデルの保存

# In[19]:
rb.writeBodyFile('HandModel.body', modelName='HandModel')


