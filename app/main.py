from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import numpy as np
import json
import math
import cv2

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('image')

class STAIRS(Resource):
    def post(self):
        args = parser.parse_args()
        image = args['image']
        img = json.loads(image)
        print(len(img))
        img = np.array(img,dtype='uint8')
        print(img.shape)
        img1 = cv2.GaussianBlur(img,(3,3),cv2.BORDER_DEFAULT)
        img2 = cv2.Canny(img1,100,180,3)
        print(img1.shape)
        lines=cv2.HoughLinesP(img2,1,np.pi/180,30,minLineLength=40,maxLineGap=5)
        c=0
        for line in lines:
        	x1,y1,x2,y2=line[0]
        	d = math.atan2(abs(y2-y1),abs(x2-x1))
        	if d<0.5:
        		cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        		c+=1
        img = cv2.putText(img,'steps:'+str(c),(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0) ,2, cv2.LINE_AA) 
        output = {'result':str(c)}
        return output

api.add_resource(STAIRS, '/')
