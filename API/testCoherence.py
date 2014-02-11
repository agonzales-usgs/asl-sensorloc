#!/usr/bin/env python

import coherence 

# Example of running coherence with *args and **kwargs
#coherence.Help()
homedir = os.getcwd()
seeddir = os.path.join(homedir, 'data', '2014_036_IU_ANMO')
seedfile1 = os.path.join(seeddir, '10_LH1.512.seed')
seedfile2 = os.path.join(seeddir, '10_LH2.512.seed')
refseed1 = os.path.join(seeddir, '00_LH1.512.seed')
refseed2 = os.path.join(seeddir, '00_LH2.512.seed')

