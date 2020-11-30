#coding: UTF-8
import scipy.sparse as sps
import numpy  as np
import sys,re
import logging
from command.runCommand import Parser
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

LOG_FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT)
#handler = logging.FileHandler('output.log', mode='a', encoding=None, delay=False)
#formatter = logging.Formatter("%(asctime)s:%(filename)s:%(levelname)s:%(message)s")
#handler.setFormatter(formatter)
#handler.setLevel(logging.DEBUG)
#logger.addHandler(handler)

class getmarixticks(object):
	'''
	This class used for obtaining matrix of hic from sparse matrix and ticksLabels.
	you should provide hicfile and bed file,chromosome prefix,default chr.If possible
	you will provide certain chromosome name to show,default whole. 
	'''
	#__slots__ =('hicFile','bedFile','prefix','showChr')


	def __init__(self,hicFile,bedFile,prefix='chr',showChr='whole',endChr="chr12"):
		self.hicFile=hicFile
		self.bedFile=bedFile
		self.prefix =prefix
		self.showChr  =showChr
		self.chromosomes=dict()
		self.endChr     =endChr
		self.chrDict   =dict()
		self.chrList   =list()
	def __str__(self):
		return  "getmatrix and ticks for plot !!!"
	def formChr(self,chromosome):
		if chromosome.upper().startswith("CHR"):
			chromosome= chromosome.upper()
			chromosome=re.sub('CHR',"",chromosome)
		elif chromosome.upper().startswith("LG"):
			chromosome=re.sub('LG',"",chromosome)
		else:
			chromosome=re.sub('\D+',"",chromosome)
		return int(chromosome)

	def getTicks(self):
		### prefix #########
		prefix=self.prefix
		axesTicks={}
		chrStart=0;chrEnd=0
		for  block  in self.chrList:
			binnum=len(block[1])
			chrEnd+=binnum
			#chrStart=chrEnd-binnum+1		
			chrTick=chrEnd
			#chrTick=(chrStart+chrEnd)/2				
			chromosome=prefix+str(block[0])
			axesTicks[chromosome]=chrTick
		return  axesTicks
	def getEnd(self):
		chromosomes=self.chromosomes
		self.chrList=sorted(chromosomes.items(),key=lambda chromosomes:chromosomes[0],reverse=False) #return list containtuple
		axesTicks=self.getTicks()
		#endbin=chrList[-1][1][-1]
		return axesTicks
	def readSparseHic(self):
		binList=[]
		try:
			bed = open(self.bedFile,'rU')
		except IOError:
			print >>sys.stderr, 'cannot open', bedFile
			raise SystemExit
		endChr =self.formChr(self.endChr)    #get end chr
		for line in bed.readlines():
			tags = line.strip().split("\t")
			if tags[0]=='chrM':logger.warning("warnings skip chrM: %s" % tags[0]);continue
			if tags[0].lower().startswith("contig"):
				logger.warning("warnings contig %s bin skipped" % tags[0])
				continue
			#tags[0]=int(formChr(tags[0]))
			tags[0]=self.formChr(tags[0])
			if int(tags[0]) >int(endChr):break
			binList.append(tags[3])  #store all bins in the binlist
			if tags[0] not in self.chromosomes.keys():
				self.chromosomes[tags[0]]=[]
				self.chromosomes[tags[0]].append(int(tags[3]))
			else: self.chromosomes[tags[0]].append(int(tags[3]))
		if self.showChr == 'whole':
			axesTicks=self.getEnd()
			#plot whole genome
			start = 1 #single chromosome strat+startbin;end= chromosomes[chromosome][0]+endBin
			endbin=int(binList[-1])  # provide endbin or not
			clast = endbin
		else:
			# exption
			self.showChr=self.formChr(self.showChr)
			chrlastBin=self.chromosomes[self.showChr][-1]
			start     =self.chromosomes[self.showChr][0]
			endbin    =chrlastBin
		length = endbin-start+1
		mtx = sps.dok_matrix((length, length), dtype=np.int)
		logging.info('You will plot bin %s ->bin %s' % (start,endbin))
		try:
			matrixFile = open(self.hicFile,'rU')
		except IOError:
			print >>sys.stderr, 'cannot open', filename
			raise SystemExit

		for line in matrixFile:
			tags = line.strip().split("\t")
			if int(tags[0]) <= endbin and int(tags[0])>=start :
				if int(tags[1]) <= endbin and int(tags[1])>=start :
					mtx[int(tags[0])-start, int(tags[1])-start] = int(round(float(tags[2])))
					mtx[int(tags[1])-start, int(tags[0])-start] = int(round(float(tags[2])))
			if int(tags[0]) > endbin: break
		matrix = mtx.todense()
		if self.showChr == 'whole':
			return matrix,axesTicks
		else:
			return  matrix,length
