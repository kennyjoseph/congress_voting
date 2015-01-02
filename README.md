Introduction
============

This is code that can be used to generate the cosponsorship and voting networks for the 113 congress.  Steps:

1. Go into the data folder and untar '''bills.tgz''' and '''votes.tgz'''. To do so, type the following at the command line:

'''

> tar -xzvf bills.tgz ; tar -xzvf votes.tgz 

'''

**** The data is from the amazing Congress project, which you can find [here](https://github.com/unitedstates/congress). ****


2. Open up '''get_vote_network.py''' and change the paths for the output files. Right now, they're my public Dropbox directory, which isn't much help to you.

3. CD back to the top level and run the python script by typing the following at the command line:

'''

> python get_vote_network.py

'''

Once you've done this, you'll have CSV files representing the networks. I then used the network analysis tool [ORA](http://casos.cs.cmu.edu/projects/ora/) to analyze the data and generate the plots. Drop me a line if you want more information.


Feel free to use/modify this code however you please.