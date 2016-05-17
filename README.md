# bamToBigWig
Directly create a bigwig file with signal derived from a sorted and indexed bam file.

This script uses pysam to read the input bam file, filters and shifts the reads,
and then computes the signal with single base resolution and directly outputs
a wiggle file to a wigToBigWig process that runs in the background.

It should work with all python versions.
## Installation
First of all, try this:
```sh
$ git clone https://github.com/PanosFirmpas/bamToBigWig
$ #You might need sudo for the following command
$ pip install -e ./bamToBigWig
```
If that does't work, here are more details on installing:
##### 1) Requirements
* bamToBigWig uses [wigToBigWig](https://genome.ucsc.edu/util.html) to create the .bw file, so the wigToBigWig executable needs to be in your path. A simple if not very elegant way to do this, is to download the executable from the link above and put it somewhere like */usr/local/bin* .
*  **Python libraries**
    
    bamToBigWig is a python script, so you will need a working installation of python, thankfully most operating systems these days come with python already installed so this should't be a problem.
    *    [pysam](https://github.com/pysam-developers/pysam) is used to read the input bam file, to install it follow the instructions in the project's page.
    *    [numpy](http://www.scipy.org/scipylib/download.html) is also needed and needs to be installed.
            ```sh
            $ pip install numpy
            ```
            should work.
    
##### 2) bamToBigWig

Is a single script, so you could just take the script file from the /scripts/ folder and run it from anywhere in your system, as long as the required libraries are available. Since this is packages as a python package though, you can use the setup.py script to automatically install bamToBigWig in your system.

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
$ pip install -e ./bamToBigWig
```

Things that might go wrong:
        
        Permission denied
Try running the installation command with sudo:

```sh
$ # sudo pip install -e ./bamToBigWig
```

If you don't have sudo privileges, you can use a [virtual environment](https://virtualenv.pypa.io/en/latest/).

## Usage
```sh
$ bamToBigWig --help
```

Should be handy for on-the-spot help.
### The options
#####  -b,--bam
This us a required option and should be the path to the input .bam file.
The bam file must be sorted and indexed
#####  -chr,--chrominfo
This should be a simple text file with two or more tab-separated columns (columns after the firt two will be ignored). The first column contains chromosome names and the second column their respective sizes in nucleotides. This file is required by wigToBigWig, but also works as a convenient way to filter chromosomes, simply provide a chrominfo file with only the chromosomes you want visualized.
#####  -o,--out
The path to the output .bw file. If not given, it will be set to /path/to/input(.bam).bw'
### Filters
#####  -q,--q
Only include reads with mapping quality >= this option. Default is None, no q filter is applied.
#####  -f,--filter_lc
Only include reads with all bits of this argument set in their flag. Default is None,no read filter is applied.


See --explain_flags')   
    '-F','--filter_uc', 
                       help='Only include reads with none of the bits of this argument set in their flag. See --explain_flags')

    '-tll','--t_len_lower', 
                       help='Sets filtering so that only reads with absolute(tlen) greater than this are accepted.\
                       See also --t_len_upper')

    '-tlu','--t_len_upper', 
                       help='Sets filtering so that only reads with absolute(tlen) lower than this are accepted.\
                       This field is set by the mapper, but for paired-end DNA it will typically refer to the\
                       fragment size. For ATAC experiments, setting this to approximately 120, will visualize\
                       the "nucleosome free" reads. Default is "None", no fragment size filter is applied.')

    '-p','--procs', 
                       help='The number of processors to use. Defaults to 4. Be advised that one of those\
                       processors with be consumed by the wigToBigWig process. After that, each available\
                       processor works on one chromosome at a time until all chromosomes are done.')

    '-sh', '--shift', 
                        help="arbitrary shift in bp. This value is used to move cutting ends (5') towards 5'->3'.\
                        If you want to extend the signal downstream of the original cutting end,\
                        for example to visualize CHIPseq experiments, you will want to leave this value to 0\
                        and set --extsize to how much you want to extend. If on the other hand you want to\
                        extend the signal to both sides of the cutting end, for example if you are visualizing\
                        ATACseq or DNAse-seq, you will want to set this value.\
                        The default value -3 in combination with the default value of --extsize 7\
                        will extend the signal by 3bp around the cutting end.\
                        NOTE: this is different than the ATAC-correction shift, and is applied on top of it.")

    '-exts', '--extsize', 
                        help="arbitrary extension size in bp. \
                        This value is used to extend each read towards 3' end.\
                        CAn be usefully combined with --shift. The default value is 7\
                        which in combination with the default --shift -3 extends the signal\
                        by 3bp upstream and downstream of the original cutting end.")

    '-sh_p', '--shift_p', 
                        help="Like --shift (and applied on top of it), but only applied to reads that map on the possitive strand.")

    '-sh_n', '--shift_n', 
                        help="Like --shift (and applied on top of it), but only applied to reads that map on the negative strand.")

    '-atac', '--atac', action='store_true', default=True,
                        help="shift reads mapping to the plus strand by +5 and reads that map\
                        on the minus strand by -4. This centers the cutting ends on the center of the\
                        transposase 'event'. Overwrites --shift_p to 5 and --shift_n to -4")




