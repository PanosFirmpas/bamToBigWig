# bamToBigWig
Directly create a bigwig file with signal derived from a sorted and indexed bam file.

This script reads the input bam file, filters and shifts the reads,
and then computes the signal with single base resolution and directly outputs a .bw file. 
It should run significantly faster than indirect approaches since it is parallelizeable
while skipping any intermediate conversions between file types.

![Alt text](/Drawing.png?raw=true "Optional Title")

     
## Installation
This should work with any decently modern python version, in any Linux distribution or MacOS.
First of all, try this:
```sh
$ git clone https://github.com/PanosFirmpas/bamToBigWig
$ #You might need sudo for the following commands
$ pip install numpy
$ pip install ./bamToBigWig
```
If that does't work, here are more details on installing:

##### 1) Requirements    
bamToBigWig is a python script, so you will need a working installation of python.     
Thankfully most operating systems these days come with python already installed so this should't be a problem.    
*    [numpy](http://www.scipy.org/scipylib/download.html) is needed and needs to be installed first.    
*    [pysam](https://github.com/pysam-developers/pysam) is used to read the input bam file, to install it follow the instructions in the project's page. 
*    [pyBigWig](https://github.com/dpryan79/pyBigWig) is used to write the output bw file, to install it follow the instructions in the project's page. 
*    [SHaredArray](https://pypi.python.org/pypi/SharedArray) is used for the multiprocessing commuunication.
        
##### 2) bamToBigWig

Is a single script, so you could just take the script file from the /scripts/ folder and run it from anywhere in your system, as long as the required libraries are available. Since this is packaged as a python package though, you can use the setup.py script to automatically install bamToBigWig in your system.

Using the setup.py script:
```sh
$ git clone https://github.com/PanosFirmpas/bamToBigWig
$ # alternatively: $ wget https://github.com/PanosFirmpas/bamToBigWig
$ cd ./bamToBigWig
$ python setup.py install
```
Alternatively:
```sh
$ git clone https://github.com/PanosFirmpas/bamToBigWig
$ pip install ./bamToBigWig
```

Things that might go wrong:
        
        Permission denied
This will happen if you are installing bamToBigWig using the global system's python environment,  
in which case the operating system needs to know that you have the right to do that so you should run the installation command with sudo:

```sh
$ # sudo pip install ./bamToBigWig
```

If you don't have sudo privileges, you can use a [virtual environment](https://virtualenv.pypa.io/en/latest/).  
This is how you should be installing python libraries on computers that you don't have absolute control over,
like on clusters, remote servers etc.  

## Usage
For on-the-spot help:
```sh
$ bamToBigWig --help
```

Here are a couple of examples of how to use bamToBigWig:

```sh
$ bamToBigWig -b input.bam -chr /home/user/chrominfo/mm20.txt -o output.bw -q 10 -f 2 -atac --
```
This command will read reads from input.bam, for all chromosomes in /home/user/chrominfo/mm20.txt,
keep only the ones marked as "proper pair", correct the signal for an atac experiment and
produce output.bw showing the signal of the ATAC cutting events, expanded three bases to each direction,
thanks to the default options of --shift -3 --extsize 7.

```sh
$ bamToBigWig -b input.bam -chr /home/user/chrominfo/mm20.txt -o output.bw -q 10 -f 2 -atac -tlu 120
```
This command will additionally only use reads that mapped within 120bp from their mate. For an ATACseq experiment,
these reads could be considered "nucleosome free" since the distance between them is too small to have
contained an entire nucleosome, meaning they are more likely to have come from a nuceosome free region.


### The options
#### Required:
#####  -b,--bam
This us a required option and should be the path to the input .bam file.
The bam file must be sorted and indexed (samtoools sort, samtools index)
You can give more than one input files, separated by space, or even 
wilcard expressions e.g.,"/path/to/some/species_stage*_replicate*.bam" . 
#####  -chr,--chrominfo
This should be a simple text file with two or more tab-separated columns (columns after the firt two will be ignored).  
The first column contains chromosome names and the second column their respective sizes in nucleotides. This file is  
required by wigToBigWig, but also works as a convenient way to filter chromosomes.  bamToBigWig only works on the  
chromosomes found in this file, so if you want to create a bigwig with only some chromosomes included,  
edit this input file accordingly. Chromosome names need to be the same in the bam file and the chrom info file.
#### Filtering Arguments:
#####  -q,--q
Only include reads with mapping quality >= this option. Default is None, no q filter is applied.
#####  -f,--filter_lc
Only include reads with all bits of this argument set in their flag. Default is None,no read filter is applied.See [--explain_flags](https://github.com/PanosFirmpas/bamToBigWig#--explain_flags)
#####  -F,--filter_uc
Only include reads with none of the bits of this argument set in their flag. See [--explain_flags](https://github.com/PanosFirmpas/bamToBigWig#--explain_flags)
#####  -tlu,--t_len_upper
This option sets filtering so that only reads with absolute(tlen) lower than this are accepted.
The 'tlen' is set by the mapper, so be careful. For paired-end DNA it will typically refer to the
'fragment size', that is, the distance between the two cutting ends of each pair of reads. For ATAC experiments, setting this to approximately 120, will visualize the "nucleosome free" reads.  If you set this option, it is suggested to also set t_len_lower to at least 0 so that reads without a mate (tlen -1) get filtered out, alternatively, set an appropriate -F filter.  Default is "None", no fragment size filter is applied.
#####  -tll,--t_len_lower
Sets filtering so that only reads with absolute(tlen) greater than this are accepted. See also --t_len_upper
#### Shifting/Extending Arguments:
#####  -sh,--shift
Arbitrary shift in bp. This value is used to move cutting ends (5') towards 5'->3'. If you want to
extend the signal downstream of the original cutting end, for example to visualize CHIPseq experiments,
you will want to leave this value to 0 and set --extsize to how much you want to extend. If on the
other hand you want to extend the signal to both sides of the cutting end, for example if you are
visualizing ATACseq or DNAse-seq, you will want to set this value to something negative.  
The default value -35 in combination with the default value of --extsize 70 will extend the signal by 35bp around the cutting end. 
#####  -exts,--extsize
Arbitrary extension size in bp.This value is used to extend each read towards 3' end.
Can be usefully combined with --shift. The default value is 70 which in combination with the 
default --shift -35 extends the signal by 35bp upstream and downstream of the original cutting end.
If this is set to 'fragment',reads will be extended until their mate.
#####  -sh_p,--shift_p
Like --shift (and applied on top of it), but only applied to reads that map on the possitive strand. Default is 0.
#####  -sh_n,--shift_n
Like --shift (and applied on top of it), but only applied to reads that map on the negative strand.Default is 0.
#####  -atac,--atac
Shift reads mapping to the plus strand by +5 and reads that map
on the minus strand by -4. This centers the cutting ends on the center of the
transposase 'event'. **this OVERWRITES --shift_p to 5 and --shift_n to -4.**    

####  Other Arguments
#####  -o,--out
The path to the output .bw file. If not given, for an input file of "/path/to/input.bam" the output file will be set to /path/to/input.bw'.
##### -p,--procs
The number of processors to use. Defaults to 4. Be advised that one of those processors with be consumed by the wigToBigWig process. After that, each available processor works on one chromosome at a time until all chromosomes are done.    
##### -split, --split_strands
Output separate files for + strand and - strand. They will automatically be named based on the output.bw     
(output_pstrand.bw / output_nstrand.bw)
##### -vv, --verbose        
Prints out some helpful/debugging messages.

##### -exfl,--explain_flags
Sequencing reads in sam/bam files contain a binary flag, which is a  combination of 12 bit-wise flags.  They are set by the aligner/mapper and allow fast and efficient filtering of the reads.  
If a read, for example, has its flag set to 2, we can see the bitwise flags by converting 2 to its binary representation which is 000000000010 .  
The second (reading from right to left) bit/flag is set to 1, so it is True, but all other bitwise flags are False. 
This means that this imaginary read belongs to a 'proper pair',  BUT since all other flags are False, this imaginary read is also "not paired" (the first bit is 0), "not the first read of the pair" (7th bit is 0), "not the second read in the pair" (8th bit is 0).  Hopefully then, you will never encounter a read with its flag set to 2, since that would mean that something is going wrong with your mapping which results in illogically flagged reads !!  
A more reasonable flag for a read would be 99. The binary representation of 99 is 000001100011.  Bits 1,2,6 and 7 are True (1) so this read would be "paired","mapped to proper pair","its mate read aligned to the negative strand" and "is the first read of the pair".  
  
If you set the -f option to 2, you are making sure that only reads which  
have their second bitwise flag set to 1 will be used. By setting the -F   
option to 2, you are making sure that such reads are excluded.

Some Examples:
```sh
# Only use 'proper pair' reads (usually implies more filters, depending on the mapper you used)
>> bamToBigWig -b in.bam -chr chrm.txt -f 2 
# EXCLUDE 'proper pair' reads 
>> bamToBigWig -b in.bam -chr chrm.txt -F 2 
# Only use reads that mapped on the '-' strand:
>> bamToBigWig -b in.bam -chr chrm.txt -f 16 
# Only use 'proper pair' reads that mapped on the '-' strand:
>> bamToBigWig -b in.bam -chr chrm.txt -f 18 
# Only use reads that mapped on the '+' strand (we exclude the '-' reads):
>> bamToBigWig -b in.bam -chr chrm.txt -F 16 
# Only use 'proper pair' reads that mapped on the '+' strand:
>> bamToBigWig -b in.bam -chr chrm.txt -f 2 -F 16 
```

An amazing resource to help you set your filters can be found here:  
https://broadinstitute.github.io/picard/explain-flags.html       

##### -exco,--coverage_examples
To visualize an ATACseq experiment, we use -atac to shift the reads
appropriatelly, then --shift the reads upstream by 10 and expand the
signal downstream of the cutting-site by 21. This expands the signal by
10bp each side of the cutting site.
```shj
>> bamToBigWig -b in.bam -chr chrm.txt --shift -10 --extsize 21
```
To visualize a CHIPseq experiment, we expand the signal dowbstream of
the cutting site by the experiment's fragment size, in this example: 300
```sh
>> bamToBigWig -b in.bam -chr chrm.txt --extsize 300 
```
