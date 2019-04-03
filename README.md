# dabasco - Evaluation module for D-BAS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This module provides an interface between the discussion data and user data export interface of [D-BAS](https://github.com/hhucn/dbas) and established data formats of abstract [argumentation framework](https://doi.org/10.1016/0004-3702(94)00041-X), [abstract dialectical frameworks](https://dl.acm.org/citation.cfm?id=2540245), or the [ASPIC](https://doi.org/10.1016/j.artint.2012.10.008) framework. As input, dabasco requires D-BAS argument graph and user data as served by the D-BAS export interface. All results are provided as a JSON string.

## Setup

To install required python packages, execute:

    make dependencies
    
To run the tests, execute:

    make test

To run the service, execute:

    make run
    
This module requires a running D-BAS instance to fetch data. Configure the D-BAS host address and the API version of that D-BAS instance in `config.py` (API version 1 for D-BAS v1.4.2 or older, API version 2 for D-BAS v1.17.0 or newer).
    
A small python web app that serves example D-BAS data (API version 1) is included. To run it, execute:

    python3 dbas_export_mockup.py
    
## Argumentation Framework Interface

The [argumentation framework](https://doi.org/10.1016/0004-3702(94)00041-X) (AF) interface creates AF instances in [ASPARTIX](https://www.dbai.tuwien.ac.at/proj/argumentation/systempage/dung.html#input_format) syntax based on a translation by [Wyner et al. (2015)](http://www.doi.org/10.1080/19462166.2014.1002535).

To get an AF representation of the D-BAS discussion with ID <discussion_id>, use:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>    

You can configure dabasco to use a single D-BAS user opinion, identified by that user's ID <user_id>, as a source for assertions by adding corresponding route elements:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>/user/<user_id> 

To get a different encoding, where the user opinion is strictly enforced, use:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>/user/<user_id>/opinion_strict

Example pipeline for Dung AF evaluation using the [conarg](http://www.dmi.unipg.it/conarg/) solver (get preferred extensions of discussion 2, use user opinion 1):

    conarg -e preferred <(curl -s 'http://localhost:5101/evaluate/dungify/dis/2/user/1' | jq -r '.af')
    
Web sources:

- ASPARTIX website: https://www.dbai.tuwien.ac.at/proj/argumentation/systempage/
- conarg website: http://www.dmi.unipg.it/conarg/

## ASPIC Interface

The [ASPIC](https://doi.org/10.1016/j.artint.2012.10.008) interface creates ASPIC instances formatted for the [TOAST](http://toast.arg-tech.org/help/web) web service.
To get a TOAST representation of a user opinion in a discussion, use either of the following, where the user opinion is encoded with varying strength. 

Normal opinion (no additional route element):

    http://localhost:5101/evaluate/toastify/dis/<discussion_id>/user/<user_id>
The opinion is represented by defeasible rules with the same preference as rules representing D-BAS arguments. If a user commitment is in conflict with the conclusion of a D-BAS argument, these mutually attack each other and both will be acceptable in some extension (but not simultaneously).

Weak opinion (add "opinion_weak" to route): 
    
    http://localhost:5101/evaluate/toastify/dis/<discussion_id>/user/<user_id>/opinion_weak 
The opinion is represented by defeasible rules with a lower preference than rules representing D-BAS arguments. This allows to weakly assume each commitment in the opinion, but these commitments are overruled by the conclusions of D-BAS arguments, if in conflict.
   
Strict opinion (add "opinion_strict" to route):
    
    http://localhost:5101/evaluate/toastify/dis/<discussion_id>/user/<user_id>/opinion_strict
The opinion is represented by strict rules. This enforces the user opinion and defeats all assumptions or conclusions of D-BAS arguments that are in conflict with the opinion.
    
Example pipeline for evaluation using the [TOAST Web service](http://toast.arg-tech.org/help/api) (evaluate discussion 2, user ID 1, with weak user opinion):

    curl -s 'http://localhost:5101/evaluate/toastify/dis/2/user/1/opinion_weak' | curl -d @- http://toast.arg-tech.org/api/evaluate
    
Web sources:

- TOAST website: http://toast.arg-tech.org/help/web
- TOAST API: http://toast.arg-tech.org/help/api
- TOAST interactive web interface: http://toast.arg-tech.org/
- TOAST web interface: http://toast.arg-tech.org/api/evaluate

## Abstract Dialectical Framework Interface

The [ADF](https://dl.acm.org/citation.cfm?id=2540245) interface creates ADF instances based on a translation by [Strass (2015)](https://doi.org/10.1093/logcom/exv004) formatted for the [YADF](https://www.dbai.tuwien.ac.at/proj/adf/yadf/), [DIAMOND](http://diamond-adf.sourceforge.net/), or [k++ADF](https://bitbucket.org/andreasniskanen/k-adf)  solvers. 
To get an ADF representation of a user opinion in a D-BAS discussion, use:
 
    http://localhost:5101/evaluate/adfify/dis/<discussion_id>/user/<user_id>
    
You can configure dabasco to use strict ADF rules (instead of defeasible rules, as default) to represent the D-BAS user opinion by adding a corresponding route element:

    http://localhost:5101/evaluate/adfify/dis/<discussion_id>/user/<user_id>/opinion_strict 
         
Example pipeline for ADF evaluation using [YADF](https://www.dbai.tuwien.ac.at/proj/adf/yadf/), [lpopt](https://www.dbai.tuwien.ac.at/research/project/lpopt/), [gringo and clasp](https://potassco.org/) (get preferred models for user 1 in discussion 2):

    java -jar yadf.jar -prf <(curl -s 'http://localhost:5101/evaluate/adfify/dis/2/user/1' | jq -r '.adf') | lpopt | gringo | clasp -n 0   
     
Web sources:

- YADF: https://www.dbai.tuwien.ac.at/proj/adf/yadf/
- DIAMOND: http://diamond-adf.sourceforge.net/
- k++ADF: https://bitbucket.org/andreasniskanen/k-adf
- gringo/clasp: https://potassco.org/
- lpopt: https://www.dbai.tuwien.ac.at/research/project/lpopt/
