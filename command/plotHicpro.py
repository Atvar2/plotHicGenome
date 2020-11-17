from command.runCommand import Parser
from getMtxAxes.Hicproc import getmarixticks
from graph.Hicplot import plot,plotChr
import logging,sys
def plotHicpro():
	args=Parser("Hic sparse matrix obteined from hic-proc","Bed file of chromosomes  which contained bins were digested basing  \
	Restriction Enzyme cutting site")
	getFileObjects=getmarixticks(args.Hic,args.bed,args.P,args.CHR,args.ECHR)
	if args.CHR == 'whole':
		logging.info("Readding and dealing with Hic matrix, please patient...")
		matrix,axesTicks=getFileObjects.readSparseHic()
		logging.info("Read matrix completely, begining to plot heamap of Hic...")
		plot(matrix,axesTicks,args.Fg,args.FIGS,args.DPI,args.CM,1,args.AxesL,args.AxesW,args.AxesPD,args.GS,args.COLO,args.WD,args.AP,args.CBSZ,args.CBPD,args.FZ,args.LOG)  #1 start
		sys.stdout.write(">>>>>>>>>>>>>>\nplot completely!\n>>>>>>>>>>>>>\n")
	else:
		matrix,length=getFileObjects.readSparseHic()
		plotChr(matrix,length,args.Fg,args.CM,args.CHR,args.R,args.FIGS,args.DPI,args.AxesL,args.AxesW,args.AxesPD,
		args.CBSZ, args.CBPD,args.LOG)