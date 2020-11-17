import time
from progressbar import *

total = 1000


def dosomework():
    time.sleep(0.01)


widgets = ['Progress: ', Percentage(), ' ', Bar('*'), ' ', Timer(),
           ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=10 * total).start()
for i in range(total):
    # do something
    pbar.update(10 * i + 1)
    dosomework()
pbar.finish()
'''
Progress: ' ：设置进度条前显示的文字
Percentage() ：显示百分比
Bar('#') ： 设置进度条形状
ETA() ： 显示预计剩余时间
Timer() ：显示已用时间
'''
