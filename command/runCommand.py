import argparse
from utils.commandUtils  import str2bool
def  Parser(Hicdescription,beddescription):
	parser=argparse.ArgumentParser(description='This kit show links of Hic,you should provide hicfile[sparse matrix of Hic proc | merged_nodups.txt that result from juicer] and bed file [bed file of Hic proc|assemblyView of Juicer], \
	if possible,you may provide chromosome prefix in plot, and default prefix chr.')
	parser.add_argument('flag', type=str, choices=['juicer', 'Hicproc'], help="this is only flag, which remind you to run corresponding module")
	parser.add_argument('Hic',type=str,help=Hicdescription)
	parser.add_argument('bed',type=str,help=beddescription)
	parser.add_argument('-H','--Matrix',dest='MTX',type=str,default="",\
						help='matrix file including Hic relation of chromosome')
	parser.add_argument('-p','--prefix',dest='P',type=str,default="chr",  \
		help='chr prefix')
	parser.add_argument('-M','--cMap',dest='CM',type=int,  \
		help='color shapping you choseed,five cMap you can select',default=3)
	parser.add_argument('-W','--chromosome',dest='CHR',type=str,default="whole",help="plot the whole genome, if you provide the last chomosome, then the figure will show between first chromosome and the last chomosome for Hic matrix of Hicproc method. while you provide single choromosome, it will display the chromosome.")
	parser.add_argument('-E','--endChr',dest='ECHR',type=str,default="chr12",help="assigned parameter the last chromosome in the bed, the ved file should be ordered,it's only for Hic matrix of Hicproc method.")
	parser.add_argument('-n','--chrNumber',dest='N',type=int,default=12,help="assigned parameter the chromosome number of genome, it's only for Hic matrix of juicerbox method.")
	parser.add_argument('-s','--chrsorted',dest='_sorted',type=str2bool,default=True,help="assigned parameter whether based one genome size [False, True], it's only for Hic matrix of juicerbox method.")
	parser.add_argument('-r','--resolution',type=int,dest='R',help='resolution used when produce Hic matrix.')
	parser.add_argument('-l','--log',dest='LOG',type=str2bool,required=False,help='assigned parameter log hic matrix or not.')  # wait fot solve?
	parser.add_argument('-i','--Dpi',dest='DPI',type=int,required=False,default=300,help='assigned distinguishability of plot figue,default:300 dpi')
	parser.add_argument('-z','--figSize',dest='FIGS',type=str,required=False,default=(6,6),help='assigned figure size,default:(6,6)')
	parser.add_argument('-X','--AxesLen',dest='AxesL',type=float,required=False,default=4,help='length of x, y axis ticks.')
	parser.add_argument('-w','--Axeswd',dest='AxesW',type=float,required=False,default=2,help='width of x, y axis ticks.')
	parser.add_argument('-d','--AxesPd',dest='AxesPD',type=float,required=False,default=6,help='distance between x, y axis ticks label and plot object.')
	parser.add_argument('-S',"--gstyple",dest='GS',type=str,required=False,default='dashed',help="grid linestyle, '-' or 'solid','--' or 'dashed','-.' or 'dashdot',':' or 'dotted',none")
	parser.add_argument('-C','--gColor',dest='COLO',type=str,required=False,default='black',help="grid color, default: black.")
	parser.add_argument('-L','--glinewd',dest='WD',type=float,required=False,default=1,help="grid linewidth!,defult:1")
	parser.add_argument('-A','--gAlpha',dest='AP',type=float,required=False,default=1,help="grid alpha!,defult:1")
	parser.add_argument('-B','--cbSize',dest='CBSZ',type=str,required=False,default="0.5%",help="percentage of plot ax, default: percentage: 0.5.")
	parser.add_argument('-D','--cbPad',dest='CBPD',type=float,required=False,default=0.1,help="distantance between colorbar and plot ax!,defalt:0.1")
	parser.add_argument('-F','--fontsize',dest='FZ',type=int, default=6, \
		help="fontsize for chromosome when plot whole genome!")
	parser.add_argument('-o','--output',dest='Fg',type=str, default='out.pdf', \
		help='output name of figure')
	parser.add_argument('-R', '--outdir', dest='ODIR', type=str, default='./', \
		help='output directory storing result')
	parser.add_argument("-v", "--verbose", help="show version of kit", action="store_true", default=False)
	args=parser.parse_args()
	return (args)
