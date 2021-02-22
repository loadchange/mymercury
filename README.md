# 水星 Mercury MIPC251C-4 网络摄像头循环录像

## rtsp
1. 高清 rtsp://admin:pass@192.168.31.222:554/stream1
2. 流畅 rtsp://admin:pass@192.168.31.222:554/stream2

## 使用

```
docker run -dit -p8822:22 \
-v /mnt/sdc1/cctv/video:/cctv/video \
-e CCTV_RTSP=rtsp://admin:pass@192.168.31.222:554/stream1 \
mymercury
```