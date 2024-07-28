from download_tiktok_no_watermark.download import download
from tqdm import tqdm

PATH = '/Users/romanvisotsky/Documents/GitHub/ticktok_parsing/videos/'

with open('/Users/romanvisotsky/Documents/GitHub/ticktok_parsing/urls.txt', 'r') as f:
	data = list(f)

# будет работать только если в названии канала не может быть знака ?
def get_name(url):
	name = url.replace('?' , '/')
	try:
		return name.split('/')[5]
	except:
		return name.split('/')[-1]

for url in tqdm(data):
	name = get_name(url)
	download(video_url = url, output_name = name, output_dir = PATH)
