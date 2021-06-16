# MediaTool class

import subprocess
import time
import os

class MediaTool(object):

    __outputName = 'outputFile.mp4'

    def __init__(self) -> None:
        super().__init__()

    def setOutputName(self, name) -> None:
        self.__outputName = name

    def concatenate(self, sourcePath, outputName='outputFile.mp4', outputPath='vidoes'):
        """
        sourcePath 为待拼接的视频的保存地址
        outputName 为拼接后视频的名称
        outputPath 为拼接后视频保存的地址
        """

        tempFileTxt = 'video_path_list_temp.txt'
        filesExtensions = [".flv", ".mkv", ".mp4"]
        if not outputName or len(outputName) == 0:
            outputName = self.__outputName

        with open(tempFileTxt, 'w') as f:
            for root, dirs, files in os.walk(sourcePath):
                # 根據名字排序
                soredFiles = sorted(files)
                for file in soredFiles:
                    if os.path.splitext(file)[1] in filesExtensions:
                        v_path = os.path.join(root, file)
                        f.write("file '{0}'\n".format(v_path))

        if os.path.exists(tempFileTxt):
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            try:
                print("begin merge...")
                path_name = os.path.join(outputPath, outputName)
                ffmpeg_command = r"ffmpeg -f concat -safe 0 -i {0} -c copy {1}".format(
                    tempFileTxt, path_name)
                subprocess.call(ffmpeg_command, shell=True)
                # 删除temp文件
                os.remove(tempFileTxt)
                print("end merge...")
            except Exception as e:
                print("merge e:", e)

