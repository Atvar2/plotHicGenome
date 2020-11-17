 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>.
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 
 

plotHicGenome: the tools are used for displaying hic signal of whole genome
===========================================================================
Installation
----------------------------------------------------------------------------

Python package and command line interface for displaying Hic signals of assembly genome
was tested with python 2.7 on linux. You can install it using pip or through source codes.

* Dependent pakages<br/>
matplotlib-2.2.3<br/>
pandas-0.24.0<br/>
numpy-1.16.4<br/>
scipy-1.2.0<br/>

* Install by pip<br/>
   git clone  https://github.com/chenjunhui/plotHicGenome<br/>
   cd plotHicGenome<br/>
   pip install --user<br/>
* Install through raw codes<br/>
  git clone  https://github.com/chenjunhui/plotHicGenome<br/>
  cd  plotHicGenome<br/>
  python  setup.py  install   [--prefix=/user/direction]<br/>

Notably: you'd better install it under virtual environment in case  system conflict.<br/>

Create virtualenv refer to:   https://docs.python.org/3/tutorial/venv.html.<br/>
  virtualenv --no-site-packages venv  //[project Name]<br/>
Finally, you need `source venv/activate` or `. venv/activate`, and execute as the methods above.<br/>

After completing to install, you can type on the command line:<br/>


```Bash
export PATH="/user/direction/bin:$PATH"
plotHicGenome  --help
```

USAGE
==============================================================================================
The package includes two sub-commands {Hicproc, juicer}, and you can choose corresponding module basing
on result of the your hic matrix.

```Bash
/user/direction/bin/plotHicGenome  --help
```
********************************************************************************<br/>
*plotHicGenome  version: 0.1.0<br/>
*please chose the plot type, subcommand: juicer or Hicproc,command<br/>
*plotHicGenome   juicer<br/>
*plotHicGenome   Hicproc<br/>
********************************************************************************<br/>

Display Hic matrix of Hic-proc
-------------------------------------------------------------------------------
```Bash
plotHicGenome   Hicproc     Hic_500000.matrix   Hic_500000_abs.bed   -p  chr  -W  whole  -E  chr20  -n  40  -r  500000  -l   T   -i  300   -z  6,6   -C  black   -L  1 -A  1  -B  "0.5%" -D 0.1    -F  6  -o  HicprocWhole.pdf    -R  ./
plotHicGenome   Hicproc     Hic_500000.matrix   Hic_500000_abs.bed   -p  chr  -W  chr1  -E  chr20  -n  40  -r  500000  -l   T   -i  300   -z  6,6   -C  black   -L  1 -A  1  -B  "0.5%" -D 0.1    -F  6  -o  Hicprocchr1.pdf    -R  ./
```
![Hicproc whole genome](https://github.com/chenjunhui/plotHicGenome/blob/plotHicGenome/example/Hic_proc.png)<br/>

Display Hic matrix of Juicerbox
--------------------------------------------------------------------------------------

If run the sub-command firstly, the command will calculate the Hic matrix to produce the Hic matrix and figure.
However, if dissatisfied with the produced figure above, the parameters are needed ajusting to obatain a better displaying.


`Sorted by chromosome size`
```Bash
plotHicGenome  juicer  ./merged_nodups.txt  ./genome.review.assembly  -W whole -n  24   -s  True  -l  t  -F  4   -r  500000  -X  2  -w  0.5  -d  3  -S  'dashed'  -i 300 -z 6,6  -C  'black'  -L  0.8   -A  0.8  -B  '1%' -D  0.2  -o  Juicerboxsorted.pdf    -R   ./sorted
```
![juicerbox sorted](https://github.com/chenjunhui/plotHicGenome/blob/plotHicGenome/example/sorted.png)<br/>
`Non-sorted by chromosome size`
```Bash
plotHicGenome  juicer  ./merged_nodups.txt  ./genome.review.assembly  -W whole -n  24   -s  False  -l  t  -F  4   -r  500000  -X  2  -w  0.5  -d  3  -S  'dashed'  -i 300 -z 6,6  -C  'black'  -L  0.8   -A  0.8  -B  '1%' -D  0.2  -o  JuicerboxNonsorted.pdf    -R   ./sorted
```
![juicerbox non-sorted](https://github.com/chenjunhui/plotHicGenome/blob/plotHicGenome/example/HicnonSorted.png)

`run sub-command juicer secondly`
```Bash
plotHicGenome  juicer  ./merged_nodups.txt  ./genome.review.assembly -W  whole   -n  24   -l  t  -F  4   -r  500000  -X  2  -w  0.5  -d  3  -S  'dashed'  -i 300 -z 6,6  -C  'black'  -L  0.8   -A  0.8  -B  '1%' -D  0.2  -o  JuicerboxNtsortedMtx.pdf  -H  sorted/Hicmatrix.txt   -R   ./sorted
 ```
 Notably, axesTicks.csv should exist in the ourdir, command read it in default. <br/>

`Plot single choromosome`
```Bash
plotHicGenome juicer   ./merged_nodups.txt  .genome.review.assembly  -W   chr1   -n  24   -s  True  -l  t  -F  4   -r  500000  -X  2  -w  0.5  -d  3  -S  'dashed'  -i 300 -z 6,6  -C  'black'  -L  0.8   -A  0.8  -B  '1%' -D  0.2  -o  JuicerboxNtsortedMtx_testchr24.pdf  -H  ./sorted/Hicmatrix.txt   -R   ./sorted
```

Parameters
==============================================================================================================================================================================

  usage: plotHicGenome [-h] [-H MTX] [-p P] [-M CM] [-W CHR] [-E ECHR] [-n N] [-s _SORTED] [-r R] [-l LOG] [-i DPI] [-z FIGS] [-X AXESL] [-w AXESW] [-d AXESPD] [-S GS] [-C COLO][-L WD] [-A AP] [-B CBSZ] [-D CBPD] [-F FZ] [-o FG] [-R ODIR] [-v] {juicer,Hicproc} Hic bed<br/>

  This kit show links of Hic,you should provide hicfile[sparse matrix of Hic proc | merged_nodups.txt that result from juicer] and bed file [bed file of
  Hic proc|assemblyView of Juicer], if possible,you may provide chromosome prefix in plot, and default prefix chr.<br/>

  positional arguments:<br/>
  {juicer,Hicproc}      this is only flag, which remind you to run
                        corresponding module<br/>
  Hic                   Result of juicer:                                     //Hic matrix<br/>
  bed                   ajusted by juicerbox                                  //bed file<br/>

  optional arguments:<br/>
  -h, --help            show this help message and exit<br/>
  -H MTX, --Matrix MTX  matrix file including Hic relation of chromosome      //Hic matrix [bin]<br/>
  -p P, --prefix P      chr prefix                                            //chromosome prefix<br/>
  -M CM, --cMap CM      color shapping you choseed,five cMap you can select   //mapplotlib color map<br/>
  -W CHR, --chromosome CHR                                                    //chromoesome,default: whole
                        plot the whole genome, if you provide the last
                        chomosome, then the figure will show between first
                        chromosome and the last chomosome for Hic matrix of
                        Hicproc method. while you provide single choromosome,
                        it will display the chromosome.<br/>
  -E ECHR, --endChr ECHR                                                      //last chromosome,if plot using Hic matrix of Hicproc method
                        assigned parameter the last chromosome in the bed, the
                        ved file should be ordered,it's only for Hic matrix of
                        Hicproc method.<br/>
  -n N, --chrNumber N   assigned parameter the chromosome number of genome,   //chromosome number of genome<br/>
                        it's only for Hic matrix of juicerbox method.<br/>
  -s _SORTED, --chrsorted _SORTED                                             //sorted by chromosome size or not, for allotetraploid, it should set to False or F<br/>
                        assigned parameter whether based one genome size
                        [False, True], it's only for Hic matrix of juicerbox
                        method.<br/>
  -r R, --resolution R  resolution used when produce Hic matrix.            //resolution [BIN]<br/>
  -l LOG, --log LOG     assigned parameter log hic matrix or not.           //wether log or not<br/>
  -i DPI, --Dpi DPI     assigned distinguishability of plot figue,default:300 //dpi<br/>
  -z FIGS, --figSize FIGS                                                    //Figure size
                        assigned figure size,default:(6,6)<br/>
  -X AXESL, --AxesLen AXESL                                                  //Axes length
                        length of x, y axis ticks.<br/>
  -w AXESW, --Axeswd AXESW                                                  //Axes width
                        width of x, y axis ticks.<br/>
  -d AXESPD, --AxesPd AXESPD                                               //distance between axes and figure region
                        distance between x, y axis ticks label and plot
                        object.<br/>
  -S GS, --gstyple GS   grid linestyle, '-' or 'solid','--' or 'dashed','-.'   //grid type 
                        or 'dashdot',':' or 'dotted',none<br/>
  -C COLO, --gColor COLO                                                       //grid color
                        grid color, default: black.<br/>
  -L WD, --glinewd WD   grid linewidth!,defult:1                              //grid width<br/>
  -A AP, --gAlpha AP    grid alpha!,defult:1                                  //grid alpha<br/>
  -B CBSZ, --cbSize CBSZ                                                      //color bar size, default 0.5%
                        percentage of plot ax, default: percentage: 0.5.<br/> 
  -D CBPD, --cbPad CBPD                                                       //distantance between colorbar and plot ax
                        distantance between colorbar and plot ax!,defalt:0.1<br/>
  -F FZ, --fontsize FZ  fontsize for chromosome when plot whole genome.        //fontsize for chromosome<br/>
  -o FG, --output FG    output name of figure                                  //output figure<br/>
  -R ODIR, --outdir ODIR                                                      //outputdir
                        output directory storing result<br/>
  -v, --verbose         show version of kit<br/>


