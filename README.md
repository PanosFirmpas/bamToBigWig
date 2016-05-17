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

