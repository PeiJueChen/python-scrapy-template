import os
class File(object):
    def writeFile(self, content, name = "1.html"):
        # print('name:',name[0:7])
        # if name[0:7] != 'static/':
        #     name = "static/" + name
        fs = open(name, 'w', encoding="utf-8")
        fs.write(content)
        fs.close()
    def create_dir(self, dir_path):
        # if not os.path.exists(dir_path): os.mkdir(dir_path)
        # 可以创建多层
        if not self.isExist(dir_path): os.makedirs(dir_path)
    def isExist(self, dir_path):
        return os.path.exists(dir_path)
    # os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
    def getCurrentFilePath():
        return os.path.dirname(os.path.dirname(__file__))

fileTool = File()

# fs = open('static/1.html', 'w', encoding="utf-8")
# fs.write("content")
# fs.close()
