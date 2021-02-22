import cv2
import time
import traceback


def delay_time(rtsp_url):
    """
    获取拉取到第一帧数据的时间
    :return:
    """
    start_time = time.time()
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        success, frame = cap.read()
        cost_time = time.time()-start_time
        print(f"拉取到第一帧数据用时：{cost_time}秒")
        return cost_time
    else:
        print("拉取流地址失败")


def pull_rtsp(rtsp_url, run_time=60):
    save_file = "/cctv/video/" + time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    """
    拉取视频流
    :param run_time: 拉取的时长，单位秒。默认为60秒
    :param save_file: 保存的文件名不带尾缀，格式为avi,默认空时，不保存拉取 视频流
    :return:
    """
    videoWrite = False
    cap = cv2.VideoCapture(rtsp_url)
    # 获取视频分辨率
    if save_file:
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # 获取视频帧率
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(f"视频流的分辨率{size}, FPS:{fps}")
        # 设置视频格式
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # 调用VideoWrite（）函数
        videoWrite = cv2.VideoWriter(f"{save_file}.avi", fourcc, fps, size)

    # 运行指定的时长
    start_time = time.time()
    while (time.time() - start_time) < run_time:
        if cap.isOpened():
            try:
                success, frame = cap.read()
                if not videoWrite is False:
                    videoWrite.write(frame)
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
            # 获取视频流异常后重新拉取
            except Exception as e:
                print(traceback.format_exc())
                cap = cv2.VideoCapture(rtsp_url)
                time.sleep(1)
        else:
            print("拉取流地址失败")
    print("拉取结束，退出程序")
    pull_rtsp(rtsp_url, run_time)


if __name__ == "__main__":
    rtsp_url = os.environ['CCTV_RTSP']
    delay_time(rtsp_url)
    pull_rtsp(rtsp_url, run_time=60)