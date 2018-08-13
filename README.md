# dabasco - Evaluation module for D-BAS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This module provides an interface between the graph data and user data export of [D-BAS](https://github.com/hhucn/dbas) and various argumentation formalisms. It can also calculate the degree of justification of individual statements or positions in D-BAS. Requires D-BAS argument graph export data as served by the D-BAS export interface. All results are provided as a JSON string.

## Setup

To install required python packages, execute:

    make dependencies
    
To run the service, execute:

    make run
    
This module requires a running D-BAS instance on localhost.
Alternatively, you can provide the D-BAS export interface yourself and serve the json export for the graph data and user opinion data at (respectively):

    http://localhost:4284/export/doj/<discussion_id>
    http://localhost:4284/export/doj_user/<user_id>/<discussion_id>
    
A small python web app that serves example D-BAS data is included. To run it, execute:

    python3 dbas_export_mockup.py
    
## Dung AF Interface

To get a Dung-style argumentation framework (AF) representation of a discussion, use:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>    

The AF is provided in ASPARTIX format.

You can configure dabasco to use a single D-BAS user opinion as a source for assumptions by adding corresponding path elements:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>/user/<user_id> 

To get a different encoding, where the user opinion is strictly enforced, use:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>/user/<user_id>/assumptions_strict

Example pipeline for Dung AF evaluation using conarg2 (get preferred extensions of discussion 2, use user opinion 1):

    curl -s 'http://localhost:5101/evaluate/dungify/dis/2/user/1' | jq -r '.af' > temp; ./conarg2 -e preferred temp; rm temp;
    
Web sources:

- ASPARTIX website: https://www.dbai.tuwien.ac.at/proj/argumentation/systempage/
- conarg website: http://www.dmi.unipg.it/conarg/

## TOAST/ASPIC Interface

To get a TOAST input format representation of a user opinion in a discussion, use:

    http://localhost:5101/evaluate/toastify

In the body of the request, provide JSON in the following format to specify parameters:

    {
      "discussion": <dbas_discussion_id>,  # mandatory
      "assumptions": {  # optional, default type "none"
        "type": "none", "weak", "strong",  # optional, default type "none"
        "bias": "none", "positive", "negative",  # optional, default bias "none"
      },
      "opinion": {  # optional, default type "none"
        "type": "none", "weak", "strong", "strict",  # optional, default type "none"
        "user": <dbas_user_id>  # mandatory unless opinion type is "none"
      }
    }    

Example pipeline for evaluation using the TOAST Web service (evaluate discussion 2, user ID 1, with weak user opinion and no assumptions):

    curl -H "Content-Type: application/json" -XGET 'http://localhost:5101/evaluate/toastify' -d '{"discussion": 2, "opinion": {"type": "weak", "user": 1}}' | curl -d @- http://toast.arg-tech.org/api/evaluate
    
Web sources:

- TOAST website: http://toast.arg-tech.org/help/web
- TOAST API: http://toast.arg-tech.org/help/api
- TOAST interactive web interface: http://toast.arg-tech.org/
- TOAST web interface: http://toast.arg-tech.org/api/evaluate

## ADF Interface

To get a YADF/DIAMOND formatted ADF representation of a user opinion in a discussion, use:
 
    http://localhost:5101/evaluate/adfify/dis/<discussion_id>/user/<user_id>
    
You can configure dabasco to use strict ADF rules (instead of defeasible rules, as default) to represent D-BAS user assumptions by adding a corresponding path element:

    http://localhost:5101/evaluate/adfify/dis/<discussion_id>/user/<user_id>/assumptions_strict 
         
Example pipeline for ADF evaluation using YADF, lpopt, gringo and clasp (get preferred models for user 1 in discussion 2):

    curl -s 'http://localhost:5101/evaluate/adfify/dis/2/user/1' | jq -r '.adf' > temp.dl; java -jar yadf_2.11-0.1.0.jar -prf temp.dl | lpopt | gringo | clasp -n 0 --outf=2; rm temp.dl;   
     
Web sources:

- YADF: https://www.dbai.tuwien.ac.at/proj/adf/yadf/
- DIAMOND: http://diamond-adf.sourceforge.net/
- gringo/clasp: https://potassco.org/
- lpopt: https://www.dbai.tuwien.ac.at/research/project/lpopt/

## Degrees of Justification

To request all degrees of justification for a discussion, use:

    http://localhost:5101/evaluate/dojs/dis/<discussion_id>
    
To request the degrees of justification of specific statements (s1, s2, ...) in a discussion, use:

    http://localhost:5101/evaluate/dojs/dis/<discussion_id>/stats/<s1>,<s2>,...

To request the degree of justification of a specific position (given by comma separated IDs of accepted statements "acc1" and rejected statements "rej1") conditioned by another specific position (given by "acc2" and "rej2"), use:

    http://localhost:5101/evaluate/doj/dis/<discussion_id>/pos1/acc/<acc1>/rej/<rej1>/pos2/acc/<acc2>/rej/<rej2>
    
All statement parameters are optional. When omitting a parameter, also omit the corresponding route element, e.g.:

    http://localhost:5101/evaluate/doj/dis/<discussion_id>/pos1/rej/<rej1>/pos2/acc/<acc2>/rej/<rej2>
    http://localhost:5101/evaluate/doj/dis/<discussion_id>/pos1/rej/<rej1>/pos2/acc/<acc2>
    http://localhost:5101/evaluate/doj/dis/<discussion_id>/pos1/rej/<rej1>/pos2
    http://localhost:5101/evaluate/doj/dis/<discussion_id>/pos1/pos2

To request the degree of justification of a user opinion (as provided by the user opinion export), use:

    http://localhost:5101/evaluate/doj/dis/<discussion_id>/user/<user_id>

## Reasons

To request all reason relations for a discussion, use:

    http://localhost:5101/evaluate/reasons/dis/<discussion_id>

To request the strength of reason of a specific statement s2 for/against a specific statement s1, use (either of):

    http://localhost:5101/evaluate/reasons/dis/<discussion_id>/for/<s1>/by/<s2>
    http://localhost:5101/evaluate/reasons/dis/<discussion_id>/by/<s2>/for/<s1>
                                             
To request the strength of reason of all statements for/against a specific statement s1, use:

    http://localhost:5101/evaluate/reasons/dis/<discussion_id>/for/<s1>
        
To request the strength of reason of a specific statement s2 for/against all statements, use:

    http://localhost:5101/evaluate/reasons/dis/<discussion_id>/by/<s2>
    
