from command.runCommand import Parser
from getMtxAxes.readHic import Juicerbox,readHicMatrix,downloadMatrix
from graph.Hicplot import plot,plotChr
import logging,sys,re
import pandas  as pd
def plotJuicerbox():
    args = Parser("Result of juicer:", "ajusted by juicerbox")
    #linkFile,reviewFile,chrNum,prefix,Bin,_sorted
    if args.CHR == 'whole' and not args.MTX:
        sys.stdout.write("Readding and dealing with Hic matrix, please patient...\n")
        getFileObjects = Juicerbox(args.Hic, args.bed, args.N, args.P, args.R,args._sorted)
        matrix, axesTicks = getFileObjects.obtainMtxAxes()
        args.ODIR=re.sub('/$','',args.ODIR)+'/'
        plot(matrix, axesTicks, args.Fg, args.FIGS, args.DPI, args.CM, 1, args.AxesL, args.AxesW, args.AxesPD, args.GS,args.COLO, args.WD, args.AP, args.CBSZ, args.CBPD, args.FZ, args.LOG)
        sys.stdout.write(">>>>>>>>>>>>>>\nplot completely!\n>>>>>>>>>>>>>\n")
        logging.info("dowload matrix, axesTicks to %s, if your re-run juicerbox module, you only assign -H or --Matrix MatrixFile" % args.ODIR)
        axesTicksList=[axesTicks]
        downloadMatrix(matrix, args.ODIR)
        axesTicksDf=pd.DataFrame(axesTicksList).T
        try:
            axesTicksDf.to_csv('%saxesTicks.csv' % args.ODIR)
        except  IOError:
                raise IOError("Can not write axesTicks.csv")
    elif args.CHR == 'whole' and args.MTX:
        logging.info("Readding and dealing with Hic matrix, please patient...")
        matrix=readHicMatrix(args.MTX, skip_header=1, skip_footer=0, filling_values=0)
        axesTicksDf=pd.read_csv('%s/axesTicks.csv' % args.ODIR, header=0,names=('chr','pos'))
        axesTicks=dict(zip(axesTicksDf['chr'], axesTicksDf['pos']))
        plot(matrix, axesTicks, args.Fg, args.FIGS, args.DPI, args.CM, 1, args.AxesL, args.AxesW, args.AxesPD, args.GS,args.COLO, args.WD, args.AP, args.CBSZ, args.CBPD, args.FZ, args.LOG)
        sys.stdout.write(">>>>>>>>>>>>>>\nplot completely!\n>>>>>>>>>>>>>\n")
    elif args.CHR != 'whole' and args.MTX:
        matrix = readHicMatrix(args.MTX, skip_header=1, skip_footer=0, filling_values=0)
        showChr=args.P+re.sub("\D+","",args.CHR)
        getFileObjects = Juicerbox(args.Hic, args.bed, args.N, args.P, args.R,args._sorted)
        getFileObjects.getwholeBin()
        regionStart = getFileObjects.whoChr[showChr][0]
        regionEnd = getFileObjects.whoChr[showChr][1]
        Binstart = int(round(regionStart/float(getFileObjects.Bin)))
        Binend = int(round(regionEnd/float(getFileObjects.Bin)))
        regionMatrix = matrix[Binstart:Binend, Binstart:Binend]
        length= len(regionMatrix)
        plotChr(regionMatrix, length, args.Fg, args.CM, args.CHR, args.R, args.FIGS, args.DPI, args.AxesL, args.AxesW, \
                args.AxesPD,args.CBSZ, args.CBPD, args.LOG)
    else:
        sys.stderr.write("args Parameter setting error: if you want to  show whole genome, please set args.CHR \
                         hic matrix or not; while if you want to show single genome, you should set args.CHR and hic matrix at the same time.")
        sys.exit(1)
