import cv2
from PIL import Image
import os

def max_face_params(faces):
	s_max = 0
	ind = 0
	for i in range(len(faces)):
		if faces[i, 2]*faces[i, 3] > s_max:
			s_max = faces[i, 2]*faces[i, 3]
			ind = i

	return faces[ind, 0], faces[ind, 1], faces[ind, 2], faces[ind, 3]

def get_crop_params(image_path):
	# Загрузка изображения
	image = cv2.imread(image_path)
	# преобразуем изображение к оттенкам серого
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	face_cascade = cv2.CascadeClassifier('/Users/romanvisotsky/Downloads/xmlClassifiers/haarcascade_frontalface_default.xml')
	# обнаружение всех лиц на изображении
	faces = face_cascade.detectMultiScale(image_gray)

	if len(faces)>0:
		# для всех обнаруженных лиц рисуем синий квадрат
		w1, h1, width, height = max_face_params(faces)

		h2 = h1 + height
		w2 = w1 + width

		H1 = int(0.85*(-0.25*h2 + 1.25*h1))
		H2 = int(2.25*h2 - 1.25*h1)

		W1 = int(0.5*w1 + 0.5*w2 - 1.25*h2 + 1.25*h1)
		W2 = int(0.5*w1 + 0.5*w2 + 1.25*h2 - 1.25*h1)

		if H1 < 0:
			H1 = 0
		if H2 > image.shape[0]:
			H2 = image.shape[0]
		if W1 < 0:
			W1 = 0
		if W2 > image.shape[1]:
			W2 = image.shape[1]

		# если вертикальная отрезаем низ
		if W2 - W1 < H2 - H1:
			delta = (H2 - H1) - (W2 - W1)
			H2 -= delta
		# если горизнтальная отрезаем края
		elif W2 - W1 > H2 - H1:
			delta = ((W2 - W1) - (H2 - H1))
			if delta%2 == 0:
				W1 += delta//2
				W2 -= delta//2
			else:
				W1 += delta//2 + 1
				W2 -= delta//2


		return (W1, H1, W2, H2)
	else:
		return None

def cut(path, to):
	pics = os.listdir(f'{path}')
	for pic in pics:
		if pic != ".DS_Store":
			with Image.open(f'{path}/{pic}') as im:
				par = get_crop_params(f'{path}/{pic}')
				if par == None:
					continue
				else:
					sq = im.crop(par)
                        
				# сжимем до 64х64 и сохраняем
				try:
					sq = sq.resize((64,64),Image.ANTIALIAS)
					sq.save(f'{to}/{pic}',quality=95)
				except:
					print(f'{path}/{pic} is bugged')
		else:
			pass

PATH = '/Users/romanvisotsky/Documents/GitHub/ticktok_parsing/'

frames_dirs = os.listdir(f'{PATH}frames/')
if '.DS_Store' in frames_dirs:
	frames_dirs.remove('.DS_Store')

for location in frames_dirs:
	os.mkdir(f'{PATH}dataset/{location}')
	cut(f'{PATH}frames/{location}',f'{PATH}dataset/{location}')

