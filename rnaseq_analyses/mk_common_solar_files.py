import numpy

exprdata=numpy.loadtxt('/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/cluster_eigengenes_GOBS.txt')


f=open('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/subcodes_common.txt')
subcodes=[i.strip() for i in f.readlines()]
f.close()

fd_demog=numpy.loadtxt('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/fd_common.txt')

wincorr=numpy.loadtxt('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/wincorr_common.txt')

f=open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/GOBS_wincorr_expression_solar.txt','w')
wincorr_names=['WC%d'%i for i in range(1,wincorr.shape[1]+1)]
me_names=['ME%d'%int(i+1) for i in range(exprdata.shape[0])]
nuisance_names=['fd','age','sex']

header=['ID']+nuisance_names+wincorr_names+me_names

f.write('%s\n'%','.join(header))

for i in range(len(subcodes)):
    data=[subcodes[i]] + ['%f'%x for x in fd_demog[i,:]] +  ['%f'%x for x in wincorr[i,:]] +  ['%f'%x for x in exprdata[:,i]]
    f.write('%s\n'%','.join(data))

f.close()