import glob,os

fp = open('Haar-Training_carPlate/training/negative/bg.txt', 'w')
files = glob.glob("Haar-Training_carPlate/training/negative/*.jpg")
print('開始產生 bg.txt')
text=""
for file in files:
    basename=os.path.basename(file)  # 取得檔名
    filename= "negative/" + basename # negative/negGray???.jpg                     
    text += filename + "\n"
    print(text)
    
fp.write(text) 
fp.close()   
print('bg.txt！完成!')