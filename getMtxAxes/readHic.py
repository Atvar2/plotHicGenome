import gzip
from collections import OrderedDict, defaultdict
import scipy.sparse as sps
import numpy  as np
import sys,re

class head(object):
	chrSize = dict()
	ctgChrPos = defaultdict(list)
	chrTotal = 0
	whoChr = defaultdict(list)
	wholeBin=0
	chromosomes=list()
	sortedNtoO=dict()
class Juicerbox(head):
	'''
	obtain matirx and axes attribute
	param: likFile, reviewFile, chrNum, chrprefix,Bin,_sorted
	'''
	def __init__(self,linkFile,reviewFile,chrNum,prefix,Bin,_sorted):
		head.__init__(self)
		self.linkFile=linkFile;self.reviewFile=reviewFile
		self.chrNum=chrNum
		self.prefix=prefix
		self.Bin   =Bin
		self.sorted=_sorted

	@classmethod
	def __str__(self):
		'''
		:return:
		'''
		return "The object obtain marix and axes, you need provide inkFile,reviewFile,chrNum,prefix,Bin,_sorted"
	def readReview(self):
		flag=dict();contigIdex=defaultdict(list)
		if self.reviewFile.endswith("gz"):
			rfHandle=gzip.open(self.reviewFile,"rb")
		else:
			rfHandle=open(self.reviewFile,'rU')
		strand="+";chrC=0
		while True:
			line=rfHandle.readline()
			if not line:
				break
			lineList=line.rstrip().split()
			if line.startswith(">"):
				if "fragment" in line:
					Contig=lineList[0].split(":::")[0]
				else:
					Contig=lineList[0]
				Contig=re.sub('>','',Contig)
				lineList[1]=int(lineList[1])
				lineList[2]=int(lineList[2])
				if Contig in flag.keys():
					ctgStart=contigIdex[lineList[1]-1][2]+1
					ctgEnd  =ctgStart+lineList[2]-1
					ctgLen=ctgEnd-ctgStart+1
					contigIdex[lineList[1]]=[Contig,ctgStart,ctgEnd,ctgLen]
				else:
					start=1;end=lineList[2]
					ctgLen=end-start+1
					flag[Contig]=ctgLen
					contigIdex[lineList[1]]=[Contig,start,end,ctgLen]
			else:
				chrC+=1
				if chrC <=self.chrNum:
					chrName=self.prefix+str(chrC)    #chromosome name
					self.chromosomes.append(chrName)
					chrStart=0;chrEnd=1;chrLen=0
					for index,ctgidx in  enumerate(lineList):
						ctgidx=int(ctgidx)
						if ctgidx <0:
							strand="-"
							ctgidx=abs(ctgidx)
						(ctg,ctgSt,ctgEd,ctgLen)=contigIdex[ctgidx]
						chrStart=chrEnd
						chrEnd=chrStart+ctgLen-1
						chrLen+=ctgLen
						self.chrTotal+=ctgLen
						self.ctgChrPos[ctg].append([chrName,ctgSt,ctgEd,strand,chrStart,chrEnd])
					self.chrSize[chrName]  =chrLen
		del  contigIdex
		return 
	#ctgChrPos,chrSize,chrTotal=readReview(sys.argv[1],12,"chr")
	def getwholeBin(self):
		self.readReview()
		self.wholeBin=int(self.chrTotal/float(self.Bin)+0.5)+1   # 933, maybe one  bin
		start=0;end=0
		if  self.sorted:
			chrTuple=sorted(self.chrSize.items(),key=lambda kv:(kv[1]),reverse=True)
			i=0			
			for c,z in chrTuple:
				i += 1
				chrName=self.prefix+str(i)
				self.sortedNtoO[c]=chrName
				start=end+1
				end=start+z-1
				self.whoChr[chrName]=[start,end]
		else:
			for c in self.chromosomes:
				self.sortedNtoO[c]=c
				start=end+1
				end=start+self.chrSize[c]-1
				self.whoChr[c]=[start,end]
		return
	def getAxes(self):
		self.getwholeBin()
		axesTicks=dict()
		i=0
		if self.sorted:
			i=self.chrNum+1
			chrTuple=sorted(self.whoChr.items(),key=lambda kv:(kv[1][0]),reverse=True)
			for c,v in chrTuple:
				i-=1;
				chrName=self.prefix+str(i)
				v=int(v[1]/float(self.Bin)+0.5)
				axesTicks[chrName]=v 
				axesTicks[chrName]=v		
		else:
			for chrName in self.chromosomes:
				pos=self.whoChr[chrName][1]
				v=int(pos/float(self.Bin)+0.5)
				axesTicks[chrName]=v
		return  axesTicks     #change
	def getPos(self,ctg,ctgPos):
		alinPos=0;chrStart=0;chrEnd=0;strand='+';chrName=str();flag=0;
		if ctg not in   self.ctgChrPos.keys():
			return None,None
		for frag  in  self.ctgChrPos[ctg]:
			chrN,ctgSt,ctgEd,sd,chrSt,chrEd=frag[0],frag[1],frag[2], \
			frag[3],frag[4],frag[5]
			ctgPos=int(ctgPos)
			if  ctgPos >=ctgSt  and ctgPos  <= ctgEd:
				chrStart=chrSt;chrEnd=chrEd;strand=sd;chrName=chrN
				flag=1
				break
		if flag == 0 :
			return None,None
		if strand == "+":
			alinPos=chrStart+(ctgPos-ctgSt)
		elif strand=="-":
			alinPos=chrEnd-(ctgPos-ctgSt)
		else:
			raise ValueError("strand should be +/-")
		return chrName,alinPos
	def  readLink(self):
			length=self.wholeBin
			mtx = sps.dok_matrix((length, length), dtype=np.int)
			if self.linkFile.endswith("gz"):
				lfHandle=gzip.open(self.linkFile,"rb")
			else:
				lfHandle=open(self.linkFile,"rU")
			while True:
				line=lfHandle.readline()
				if not line:
					break
				lineList=line.rstrip().split()
				ctg_A, pos_A = lineList[1:3]
				ctg_B, pos_B = lineList[5:7]
				AchrName,AchrPosition=self.getPos(ctg_A,pos_A)
				BchrName,BchrPosition=self.getPos(ctg_B,pos_B)
				if AchrPosition == None  or   BchrPosition==None:
					continue
				AwChrstart=  self.whoChr[self.sortedNtoO[AchrName]][0]
				BwChrstart=  self.whoChr[self.sortedNtoO[BchrName]][0]
				Ai=int((AwChrstart+AchrPosition-1)/float(self.Bin)+0.5)  # chromoseme coord in whole genome
				Bj=int((BwChrstart+BchrPosition-1)/float(self.Bin)+0.5)
				mtx[Ai, Bj]+=1
				mtx[Bj, Ai]+=1
			matrix=mtx.todense()
			return  matrix
	def obtainMtxAxes(self):
		'''
		function getAxes should be excecuted
		before readLink
		:param self:
		:return: matrix,axesTicks
		'''
		axesTicks=self.getAxes()
		matrix   =self.readLink()
		return  matrix,axesTicks
def readHicMatrix(MatrixFile,skip_header=1,skip_footer=0,filling_values=0):
	'''
		numpy.genfromtxt(fname, dtype= < type
		'float' >, comments = '#', delimiter = None, skiprows = 0, skip_header = 0, skip_footer = 0, converters = None, missing = '', missing_values = None, filling_values = None, usecols = None, names = None, excludelist = None, deletechars = None, replace_space = '_', autostrip = False, case_sensitive = True, defaultfmt = 'f%i', unpack = None, usemask = False, loose = True, invalid_raise = True)
		https://het.as.utexas.edu/HET/Software/Numpy/reference/generated/numpy.genfromtxt.html
	'''
	try:
		Matrix=np.genfromtxt(MatrixFile,skip_header=skip_header,skip_footer=skip_footer,filling_values=filling_values)
	except OSError as err:
		sys.stderr.write("OS error: {0} Can not open file {1}\n".format(err,MatrixFile))
		sys.exit(1)
	if len(Matrix[:,1]) != len(Matrix[1,:]):
		sys.stderr.write("{0} was not a square matrix".format(MatrixFile))
		sys.exit(1)
	return Matrix

def downloadMatrix(Matrix,wkDir='./'):
	header=''
	HicMtx=open('%sHicmatrix.txt'% wkDir,'w')
	for b in range(len(Matrix)):
		if header:
			header+='\t'+'Bin'+str(b)
		else:
			header='Bin'+str(b)
	HicMtx.write(header+'\n')
	(r,c)=np.shape(Matrix)
	for i in range(r):
		line=''
		for j in range(c):
			if line:
				line+='\t'+str(Matrix[i,j])
			else:
				line=str(Matrix[i,j])
		HicMtx.write(line+'\n')
        


