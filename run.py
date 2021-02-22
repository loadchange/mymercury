import cv2 as cv
import time
import numpy
import os
import threading	#多线程
import datetime

def create_file(filename):
    path = filename[0:filename.rfind("/")]
    if not os.path.isdir(path):  # 无文件夹时创建
        os.makedirs(path)
    if not os.path.isfile(filename):  # 无文件时创建
        fd = open(filename, mode="w", encoding="utf-8")
        fd.close()
    else:
       pass


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        #dir_list = sorted(dir_list, key=lambda x: int(x[:-4]))  # 按名称排序
        # print(dir_list)
        return dir_list

def SaveVideo():
        fpsize = os.path.getsize('/capturevideo/2020-06-28-17-04.avi') / 1024
        if fpsize >= 150.0: #大于150KB的视频需要压缩
            if '/capturevideo/2020-06-28-17-04.avi':
                compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format('/capturevideo/2020-06-28-17-04.avi','/capturevideo/2020-06-28-17-041.avi')
                isRun = os.system(compress)
            else:
                print(" ")
                #compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(self.fileInputPath, self.fileInputPath)
                #isRun = os.system(compress)
            if isRun != 0:
                return (isRun,"没有安装ffmpeg")
            return True
        else:
            return True

def Compress_Video():
    # 异步保存打开下面的代码，注释同步保存的代码
    thr = threading.Thread(target=SaveVideo)
    thr.start()
    #下面为同步代码
    # fpsize = os.path.getsize(self.fileInputPath) / 1024
    # if fpsize >= 150.0:  # 大于150KB的视频需要压缩
    #     compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(
    #         self.fileInputPath, self.fileOutPath)
    #     isRun = os.system(compress)
    #     if isRun != 0:
    #         return (isRun, "没有安装ffmpeg")
    #     return True
    # else:
    #     return True
camera = cv.VideoCapture(os.getenv('RTSP1'))
# camera=cv.VideoCapture(0) #获取摄像头
fps=camera.get(cv.CAP_PROP_FPS) #获取帧率
numFramesRemaining=1*fps; #z
width=int(camera.get(cv.CAP_PROP_FRAME_WIDTH)) #一定要转int 否则是浮点数
height=int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))
print(width)
print(height)
size=(width,height) #大小
# 格式化成2016-03-20 11:45:39形式
success,frame=camera.read()#只写10帧
# print (time.strftime("%Y-%m-%d-%H-%M", time.localtime())) 
# newfilename=time.strftime("%Y-%m-%d-%H-%M", time.localtime())+'.avi'
# newrootpath = '/capturevideo/'
# newfilefullname=newrootpath+ newfilename
#Compress_Video()
while True:
    print (time.strftime("%Y-%m-%d-%H-%M", time.localtime())) 
    newfilename=time.strftime("%Y-%m-%d-%H-%M", time.localtime())+'.mp4'
    newrootpath = '/cctv/video/'
    newfilefullname=newrootpath+ newfilename
    if os.path.exists(newfilefullname):
        # VWirte=cv.VideoWriter(newfilefullname,cv.VideoWriter_fourcc('I','4','2','0'),fps,size) #初始化文件写入 文件名 编码解码器 帧率 文件大小
        VWirte=cv.VideoWriter(newfilefullname,cv.VideoWriter_fourcc(*"mp4v"),fps,size) #初始化文件写入 文件名 编码解码器 帧率 文件大小
        while True:
            VWirte.write(frame)    
            success,frame=camera.read()
            numFramesRemaining-=1
            if (time.strftime("%Y-%m-%d-%H-%M", time.localtime()) not in  newfilename):
                break
        VWirte.release()
    else:
        if success == False:
            while not success:
                camera = cv.VideoCapture(os.getenv('RTSP2'))
                success,frame=camera.read()
        # print("   ")
        # print (time.strftime("%Y-%m-%d-%H-%M", time.localtime())) 
        # newfilename=time.strftime("%Y-%m-%d-%H-%M", time.localtime())+'.avi'
        # newrootpath = '/capturevideo/'
        # newfilefullname=newrootpath+ newfilename
        create_file(newfilefullname)
        filelist = get_file_list(newrootpath)
        for filename in filelist:
            lastupdatetime = os.path.getmtime(os.path.join(newrootpath, filename))
            d1 = datetime.datetime.now()
            d3 = d1 + datetime.timedelta(hours=-36)
            threeDaysAgoTimeStamp = int(time.mktime(d3.timetuple()))

            # timeArray = time.localtime(lastupdatetime)
            if lastupdatetime < threeDaysAgoTimeStamp:
                if os.path.exists(os.path.join(newrootpath, filename)):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(os.path.join(newrootpath, filename))  
                    #os.unlink(path)
                else:
                    print('no such file:%s'%os.path.join(newrootpath, filename))  # 则返回文件不存在
            else:
                break

time.sleep(1) #y延迟一秒关闭摄像头 否则会出现 terminating async callback 异步处理错误
camera.release() #释放摄像头
print('ok')