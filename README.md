# myconnectome

Data analysis code for the [myconnectome project](http://www.myconnectome.org/)

### timeseries_analyses

This directory contains code used to run time series analyses comparing different variables.

* est\_bivariate\_arima_model.R - code to run bivariate association analysis
* mk_graph.py - code to generate GEXF file representing the phenome-wide network

### rsfmri_analyses 

This directory contains code used to analyze the resting state fMRI data.

* rsfmri\_get\_network\_stats.py - code to compute graph-theoretic network stats
* 

### rnaseq_analyses 

This directory contains code used to analyze the RNA-seq data.

* process\_rnaseq.py - sets up shell scripts to run the RNA-seq analysis pathway
* rnaseq\_setup\_htcount\_data.R - uses DeSEQ to compute variance-stabilized read values
* 
