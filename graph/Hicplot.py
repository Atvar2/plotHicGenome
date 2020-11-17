import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
import matplotlib.font_manager
import matplotlib.pyplot as plt
from  numpy import log2,log10
import  numpy as np
from matplotlib.ticker  import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import make_axes_locatable

cmaps = ['Greys','Reds','YlOrBr','YlOrRd','hot']
def plot(matrix,axesTicks,outfile='out.pdf',figSize=(6,6),Dpi=300,cMap=3,start=1, AxesLen=4,Axeswd=1,AxesPad=6, \
gridSt='dashed',gridColor='black',gridLw=1,gripAp=0.8, \
cpSize="0.5%",cpPad=0.05,fontSize=6,Log="False"):
	orientation = 'lower'
	(w,h)=figSize.split(',')
	fig=plt.figure(figsize=(int(w),int(h)),dpi=Dpi)   #define figure, add_subplot,sub2plot need not
	ax1 = plt.subplot2grid((1, 4), (0,0), rowspan=1,colspan=4)
	params={'font.family':'serif',
        'font.serif':'Times New Roman',
        'font.style':'italic',
        'font.weight':'normal',
        'font.size':fontSize
        }
	try:
		rcParams.update(params)
	except Warning:
		sys.stderr.write("You should install serif font family if possible"+'\n')
	#ax1.set_xlabel('ax4_x')
	#a=[20,50,100,400];b=['a','b','c','d']
	labels=list(axesTicks.keys());pos=list(axesTicks.values())
	ax1.set_xticks(pos)
	ax1.set_xticklabels(labels)
	ax1.set_yticklabels(labels)
	ax1.set_yticks(pos)
	ax1.grid(color=gridColor,linestyle=gridSt,linewidth=gridLw,alpha=gripAp)
	#ax.set_xlabel('xlabel', fontsize=10)  fontsize
	#ax.xaxis.label.set_size(20)  setting label sizes after creation
	plt.setp(ax1.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor",fontsize=fontSize)
	plt.setp(ax1.get_yticklabels(), rotation=45, ha="right",rotation_mode="anchor",fontsize=fontSize)
	ax1.tick_params(direction='out', length=AxesLen, width=Axeswd,pad=AxesPad)
	divider = make_axes_locatable(ax1)
	cax = divider.append_axes("right", size=cpSize, pad=cpPad)   #pad=0.05, size="5%", 5% of ax
	length=len(matrix)
	ax1.set_ylim(int(start or 1) - 0.5,int(start or 1) + length - 0.5)
	ax1.set_xlim(int(start or 1) - 0.5,int(start or 1) + length - 0.5)
	#cmaps = ['Greys','Reds','YlOrBr','YlOrRd','hot']
	if Log:
		with np.errstate(divide='ignore'):img=ax1.imshow(log2(matrix),cmap=plt.get_cmap(cmaps[cMap]),origin=orientation,interpolation="nearest",extent=(int(start or 1) - 0.5, int(start or 1) + length - 0.5,int(start or 1) - 0.5,int(start or 1) + length - 0.5),aspect='auto') #solve log2 Divide by zero error encountered error
		cb=fig.colorbar(img,ax=ax1,cax=cax,orientation="vertical") #extend="both", change colobarticks:cb.set_ticks, cb.set_ticklabels,cb.get_ticks, cb.ax.tick_params(labelsize=16)
		cb.ax.tick_params(labelsize=fontSize) #https://blog.csdn.net/qq_35240640/article/details/89478662
		plt.savefig(outfile) #format='pdf'
	else:
		with np.errstate(divide='ignore'):img=ax1.imshow(matrix,cmap=plt.get_cmap(cmaps[cMap]),origin=orientation,interpolation="nearest",extent=(int(start or 1) - 0.5, int(start or 1) + length - 0.5,int(start or 1) - 0.5,int(start or 1) + length - 0.5),aspect='auto') #solve log2 Divide by zero error encountered error
		fig.colorbar(img,ax=ax1,cax=cax,orientation="vertical") #extend="both"
		plt.savefig(outfile)
def plotChr(matrix,length=0,outfile='out.pdf',cMap=3,chromosome='',resolution=1000000,figSize=(6,6), \
			Dpi=300,AxesLen=4,Axeswd=1,AxesPad=6,cpSize="0.5%",cpPad=0.05,Log=True):
	orientation='lower' #figure display method
	(w,h)=figSize.split(',')
	fig=plt.figure(figsize=(int(w),int(h)),dpi=Dpi)
	ax1 = fig.add_subplot(1,1,1,aspect = "equal")
	start=1
	ax1.set_ylim(int(start or 1) - 0.5,int(start or 1) + length - 0.5)
	ax1.set_xlim(int(start or 1) - 0.5,int(start or 1) + length - 0.5)
	ax1.get_yaxis().set_label_coords(-0.125,0.5)
	ax1.get_xaxis().set_label_coords(0.5,-0.125)
	with np.errstate(divide='ignore'): img=ax1.imshow(log2(matrix),cmap=plt.get_cmap(cmaps[cMap]),origin=orientation,interpolation="nearest",extent=(int(start or 1) - 0.5,int(start or 1) + length - 0.5,int(start or 1) - 0.5,int(start or 1) + length - 0.5),aspect='auto')
	divider=make_axes_locatable(ax1)
	cax = divider.append_axes("bottom", size=cpSize, pad=cpPad)
	fig.colorbar(img,ax=ax1,cax=cax,orientation='horizontal')
	ax1.set_ylabel('log2(interaction matrix) - %s (Genomic Bins)' % (chromosome))
	plt.setp(ax1.get_xticklabels(), visible=False)
	ax1.tick_params(direction='out', length=AxesLen, width=Axeswd, pad=AxesPad)
	ax1.set_xlabel('Chromosome %s Mb (resolution: %sKb)' % (chromosome , resolution/1000))
	plt.savefig(outfile)
