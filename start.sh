docker run -d -ti --memory=5g -p 3000:3000 opendronemap/nodeodm
source /home/murad/Documents/myprojectenv/bin/activate
cd /home/murad/Documents/yolowebapp2/
python manage.py runserver 0.0.0.0:8080
#docker run -p 3000:3000 --gpus all opendronemap/nodeodm:gpu
