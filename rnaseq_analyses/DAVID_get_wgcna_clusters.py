"""
get clusters and annotations for each module
"""


import sys
sys.path.append('../')

import logging
import traceback as tb
import suds.metrics as metrics
from tests import *
from suds import *
from suds.client import Client
from datetime import datetime
import cPickle
import mygene

def load_assignments(infile):
    genedict={}
    f=open(infile)
    for l in f.readlines():
        l_s=l.strip().split(' ')
        genedict[l_s[0]]=int(l_s[1])
    return genedict
    
def get_module_genelists(genedict):
    modules=list(set(genedict.values()))
    genelists={}
    for k in genedict.iterkeys():
        if not genelists.has_key(genedict[k]):
            genelists[genedict[k]]=[k]
        else:
            genelists[genedict[k]].append(k)
    return genelists
  


#add a list
if 1:
  try:
    chartReports_path=cPickle.load(open('/Users/poldrack/data/selftracking/rna-seq/WGCNA/DAVID_chartReport_path_thr8_prefilt_rinreg.pkl','rb'))
    chartReports_GO=cPickle.load(open('/Users/poldrack/data/selftracking/rna-seq/WGCNA/DAVID_chartReport_GO_thr8_prefilt_rinreg.pkl','rb'))
  except: 
    a=load_assignments('/Users/poldrack/data/selftracking/rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt')
    cluster_genes=get_module_genelists(a)
    cluster_genes.pop(0)  # remove unassigned module
        
    setup_logging()
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    
    url = 'http://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
        
    print 'url=%s' % url
    
    #
    # create a service client using the wsdl.
    #
    client = Client(url)
    
    #
    # print the service (introspection)
    #
    print client
    
    #authenticate user email 
    print client.service.authenticate('poldrack@utexas.edu')
    
    chartReports_path={}
    chartReports_GO={}
    chartReports_disease={}
    entrez={}
    
    mg=mygene.MyGeneInfo()
    for modnum in range(len(cluster_genes)+1):
        if modnum==0:
            continue
        genelist=cluster_genes[modnum]
        inputIds=','.join(genelist)
    
        # get entrez gene ids    
        entrez[modnum]=[]
        for g in genelist:
            result=mg.query(g,species='human')
            for h in result['hits']:
                if h.has_key('entrezgene'):
                    entrez[modnum].append('%d'%h['entrezgene'])
                    break
        
        inputIds=','.join(entrez[modnum])
    
        idType = 'ENTREZ_GENE_ID'
        listName = 'mod%02d'%modnum
        listType = 0
    
        client.service.addList(inputIds, idType, listName, listType)
    
        #getChartReport
        thd=0.1
        count = 2
    
        cats_PATH='REACTOME_PATHWAY,BIOCARTA,PANTHER_PATHWAY'
        client.service.setCategories(cats_PATH)
        chartReports_path[modnum]= client.service.getChartReport(thd, count)
            
        cats_GO='GOTERM_BP_FAT,GOTERM_MF_FAT'
        client.service.setCategories(cats_GO)
        chartReports_GO[modnum]= client.service.getChartReport(thd, count)
            
    
    cPickle.dump(chartReports_path,open('/Users/poldrack/data/selftracking/rna-seq/WGCNA/DAVID_chartReport_path_thr8_prefilt_rinreg.pkl','wb'))
    cPickle.dump(chartReports_GO,open('/Users/poldrack/data/selftracking/rna-seq/WGCNA/DAVID_chartReport_GO_thr8_prefilt_rinreg.pkl','wb'))
     
fdr_thresh=0.1

for modnum in range(len(cluster_genes)+1):
    if modnum==0:
        continue
    f_gc=open('/Users/poldrack/data/selftracking/rna-seq/WGCNA/DAVID_thr8_prefilt_rin3PCreg_path_set%03d.txt'%modnum,'w')
    clustgenes=[]
    goodrecs=[]
    moddata=chartReports_path[modnum]
    for gc in range(len(moddata)):
        clust=moddata[gc]
        if clust['benjamini']<fdr_thresh:
                goodrecs.append('%f %s'%(clust['benjamini'],clust['termName']))
                clustgenes.append(clust['geneIds'])
    if len(goodrecs)>0:
        for r in goodrecs:
            f_gc.write('%s\n'%r)
        f_gc.write('%s\n'%','.join(cluster_genes[modnum]))
    f_gc.close()

    f_gc=open('/Users/poldrack/data/selftracking/rna-seq/WGCNA/DAVID_thr8_prefilt_rin3PCreg_GO_set%03d.txt'%modnum,'w')
    clustgenes=[]
    goodrecs=[]
    moddata=chartReports_GO[modnum]
    for gc in range(len(moddata)):
        clust=moddata[gc]
        if clust['benjamini']<fdr_thresh:
                goodrecs.append('%f %s'%(clust['benjamini'],clust['termName']))
                clustgenes.append(clust['geneIds'])
    if len(goodrecs)>0:
        for r in goodrecs:
            f_gc.write('%s\n'%r)
        f_gc.write('%s\n'%','.join(cluster_genes[modnum]))
    f_gc.close()
