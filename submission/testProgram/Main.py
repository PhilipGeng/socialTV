import numpy as np, cv2
import transparency as tp
import superimpose as si
import cover as c

def play():
	avatar_path = ["Alpaca","Cheetah","Leopard","Suricate","Tiger"]
	avatars = [0,0,0,0,0] #imread 5 avatars at each frame
	avatar_emotion = [0,0,0,0,0] #the string "happy",sad...(predicted answer from asgn2)
	emotion = ["angry","disgusted","happy","nervous","neutral","sad","surprised"]
	emotion_img = loadEmotion(emotion);#prepare for emoticons
	for i in range(len(avatars)):
		avatar_emotion[i] = parseArff(avatar_path[i])#get correct answers

	cap = cv2.VideoCapture("../video/movie.mp4")
	video_w = 800
	video_h = 400
	frame_number = 0
	avatarview = np.zeros((160, 800,4), np.uint8)
	view = np.zeros((660, 900,4), np.uint8)
	view = cv2.resize(cv2.imread("images.jpg", cv2.IMREAD_UNCHANGED),(900,660))
	while(cap.isOpened()): 
		frame_number+=1
		if(frame_number>16200):
			break
		print frame_number
		ret, videoframe = cap.read()
		videoframe = cv2.resize(videoframe,(video_w,video_h))#upper part -- video
		
		if frame_number%5 == 1:
			for i in range(len(avatars)):
				avatars[i] = prepareFrame(avatar_path[i],frame_number) #lower part -- 5 avatars
	
		h1, w1 = videoframe.shape[:2]
		h2, w2 = avatars[0].shape[:2]
		dif = video_w/5-w2
		view[50:h1+50,50:w1+50,:3] = videoframe #attach to view
		if frame_number%50== 1:
			for i in range(len(avatars)):# superimpose emoticons
				ss = getEmotion(avatar_emotion,i,frame_number)#get correct emotion
				avatars[i] = c.cover(avatars[i], getEmotionImg(emotion,emotion_img,ss), 0.5, 0.5, 0, 90)
				cv2.putText(avatars[i],avatar_path[i]+"   "+ss, (0,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
				avatarview[:h2, i*(w2+dif):(i+1)*(w2+dif)-dif] = avatars[i] # attach to view
		si.superimpose(view,avatarview,1,1,450,50)
		cv2.imshow("test", view)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
	cap.release()
	cv2.destroyAllWindows()

def getEmotion(avatar_emotion,i,frame_number):# get current frame emotion by putting the array into a stack
	if(len(avatar_emotion[i])>1 and frame_number>int(avatar_emotion[i][1][0])-1):
		avatar_emotion[i].pop(0) # pop up the out-dated one
	return avatar_emotion[i][0][1] #read the top one

def loadEmotion(emotion):
	emotion_img = []
	for i in range(len(emotion)):
		emotion_path = "../emotion/"+emotion[i]+".jpg"
		emotion_img.append(cv2.imread(emotion_path, cv2.IMREAD_UNCHANGED))
		emotion_img[i] = imgAddAlphaChannel(emotion_img[i])
	return emotion_img

def getEmotionImg(emotion_arr,emotion_img,emotion):
	for i in range(len(emotion_arr)):
		if(emotion_arr[i]==emotion):
			return emotion_img[i]

def parseArff(animal):
	path = "../arff/"+animal+".predict.arff"
   	f = open(path, "r")
	line_num = 0;
	instance = [];
	for line in f:
        	features = line.split(",")
		if ((len(instance) == 0) or (features[len(features)-1]!=instance[len(instance)-1][1])):
			instance.append([features[0],str.strip(features[len(features)-1])])
	return instance

def imgAddAlphaChannel(img):
	toappend = np.zeros((len(img),len(img[0]),1),np.uint8)
	toappend[:len(img),:len(img[0]),:1] = 255
	img = np.dstack((img,toappend))
	return img

def prepareFrame(animal,index):
	avatar_w = 210
	avatar_h = 210
	path = "../users/"+animal+"/avatar1/frames"+str(index).rjust(6,'0')+".jpg"
	if(animal == "Leopard"):
		path = "../users/"+animal+"/avatar1/frame"+str(index).rjust(6,'0')+".jpg"
	avatar = cv2.imread(path)
	if avatar is None:
		return prepareFrame(animal,index-1)	
	avatar = cv2.resize(avatar,(avatar_w,avatar_h))
	avatar = tp.openFile(avatar)
	avatar = cv2.resize(avatar,(120,160))
	ret = np.zeros((160, 160,4), np.uint8)
	ret[:160,:120]=avatar
	return ret
	
play()
