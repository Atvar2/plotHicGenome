from  command.plotHicpro import  plotHicpro
from  command.plotJuicerbox import plotJuicerbox
import sys

def  main():
	Help='''
********************************************************************************
* plotHicGenome  version: 0.1.0
* please chose the plot type, subcommand: juicer or Hicproc,command\n\
*	%s   juicer\n\
*	%s   Hicproc\n
********************************************************************************
'''  % (sys.argv[0],sys.argv[0])

	if len(sys.argv)==1:
		sys.stdout.write(Help)
		sys.exit(1)
	if  len(sys.argv)==2 and sys.argv[1]=="--help":
		sys.stdout.write(Help)
		sys.exit(1)

	if sys.argv[1]=='juicer':
		plotJuicerbox()
	elif sys.argv[1] == 'Hicproc':
		plotHicpro()
if __name__ == "__main__":
	main()
