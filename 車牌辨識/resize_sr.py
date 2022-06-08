def emptydir(dirname):          #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)                #刪除檔案~需延遲,否則會出錯
    os.mkdir(dirname)           #建立資料夾

def dirResize(src, dst):
    myfiles = glob.glob(src + '/*.JPG')  #讀取資料夾內全部jpg檔案
    emptydir(dst)
    print(src + ' 資料夾：')
    print('開始轉換圖形尺寸！')
    for i, f in enumerate(myfiles):
        img = Image.open(f)
        img_new = img.resize((300, 225), PIL.Image.ANTIALIAS)  #尺寸300x225
        outname = str("resizejpg") + str('{:0>3d}').format(i+1) + '.jpg'
        img_new.save(dst + '/' + outname)
    print('轉換圖形尺寸完成！\n')

import PIL
from PIL import Image
import glob
import shutil, os
from time import sleep

dirResize('carPlate_sr', 'carPlate')
dirResize('realPlate_sr', 'realPlate')
