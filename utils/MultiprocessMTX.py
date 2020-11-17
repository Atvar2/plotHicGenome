from multiprocessing import Pool, cpu_count
import Queue
import threading
import numpy as np
import re,sys,os
cpu=int(sys.argv[1])

filename=sys.argv[2]
matrix = np.genfromtxt(filename,skip_header=1,filling_values='0',skip_footer=0).T
(r,c)=np.shape(matrix)
print (matrix)
def long_time_task(i,Mstart,Mend,matrix):
	print ("%s\t%d\tmstart:%d\tMend\t%d" % ('*' * 20,i,Mstart,Mend))
	print ('process {}'.format(os.getpid()))
	#print (matrix)
	subMatrix=matrix[:,Mstart:Mend]
	(r,c)=np.shape(subMatrix)
	print (subMatrix)
	print ("*" *30)
	for i in range(r):
		for j in range(c):
			#print (subMatrix[i,j])
			subMatrix[i,j]=subMatrix[i,j]+1
			#print(subMatrix[i,j])
	return (subMatrix,Mstart,Mend)
class Header(object):
	mPortionLen=0
	col=0
	Mstart=0
	Mend=0

class  allotCPU(Header):
	def __init__(self,matrix,cpu):
		Header.__init__(self)
		self.matrix=matrix
		self.cpu    =cpu

		(r,c)=np.shape(self.matrix)
		self.col=c
		if self.cpu >=cpu_count():
			self.cpu=cpu_count()
			print ("process number was resetted as cpu_count:%d" % cpu_count())
		if self.cpu >c:
			self.cpu=c
		self.mPortionLen=c/self.cpu
		if isinstance(self.mPortionLen,float):
			self.mPortionLen=int(c/self.cpu+0.5)
		else:
			self.mPortionLen=int(c/self.cpu)
		print ("row: %d, col: %d, Portion: %d, CPU: %d" % (r,c,self.mPortionLen,self.cpu))
		self.Matrix=np.empty((r,c), dtype = float)
		self.p=Pool(cpu)
		self.subMTXq=Queue.Queue()
	def PoolFun(self):
		for i in range(self.cpu):
			if self.Mend >self.col:
				self.Mend=self.col-1
				break
			self.Mstart=self.Mend
			self.Mend  =self.Mstart+self.mPortionLen

			try:
				self.subMTXq.put(self.p.apply_async(long_time_task, args=(i,self.Mstart,self.Mend,self.matrix)))
			except:
				break
	def getsubMTX(self):
		i=0
		while 1:
			i+=1
			if i >self.cpu:
				self.p.terminate()
				break
			subMTX,Mstart,Mend=self.subMTXq.get().get()
			#print (subMTX)
			self.Matrix[:,Mstart:Mend]=subMTX
		print(self.Matrix)	
		self.p.close()
		self.p.join()
	#print(Matrix)
if __name__  ==  '__main__':	
	obj=allotCPU(matrix,int(cpu))
	obj.PoolFun()
	obj.getsubMTX()
#print (Matrix)



'''
for b in range(len(matrix)):
	header+='Bin'+str(b)+'\t'
header=re.sub('\t$','',header)
print header
for i in range(r):
	line=''
	for j in range(c):
		if line:
			line+='\t'+str(matrix[i,j])
		else:
			line=str(matrix[i,j])
	
	print line
'''
