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

You can configure dabasco to use a single D-BAS user opinion as a source for assertions by adding corresponding path elements:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>/user/<user_id> 

To get a different encoding, where the user opinion is strictly enforced, use:

    http://localhost:5101/evaluate/dungify/dis/<discussion_id>/user/<user_id>/opinion_strict

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
        "type": "none", "weak",  # optional, default type "none"
      },
      "opinion": {  # optional, default type "none"
        "type": "none", "weak", "strong", "strict",  # optional, default type "none"
        "user": <dbas_user_id>  # mandatory unless opinion type is "none"
      }
    }
    
ASPIC can only build arguments from assumed literals. You can use either a user opinion, general assumptions, or both to provide these.
    
The field "assumptions" is ignored if not present or if its "type" is "none". If the assumptions type is "weak", then a defeasible rule with a lower preference than rules representing D-BAS arguments is created for each D-BAS statement and its negation. This allows to weakly assume each and every statement, but these are overruled by the conclusions of D-BAS arguments or by strong or strict user commitments, if in conflict.

The field "opinion" is ignored if not present or if its "type" is "none". If the opinion "type" is either of "weak", "strong", or "strict", the field "user" must be set to a D-BAS user's ID in the given discussion - this user's opinion is then encoded in the result via either:
* "weak": defeasible rules with a lower preference than rules representing D-BAS arguments. This allows to weakly assume each commitment in the opinion, but these commitments are overruled by the conclusions of D-BAS arguments, if in conflict. Note that a weak user opinion has no impact when already using (weak) assumptions. 
* "strong": defeasible rules with the same preference as rules representing D-BAS arguments. This allows to strongly assume each commitment in the opinion. If a strong user commitment is in conflict with the conclusion of a D-BAS argument, these mutually attack each other and both will be acceptable in some extension (but not simultaneously).
* "strict": strict rules. This enforces the user opinion and defeats all assumptions or conclusions of D-BAS arguments that are in conflict with the opinion.

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
    
You can configure dabasco to use strict ADF rules (instead of defeasible rules, as default) to represent the D-BAS user opinion by adding a corresponding path element:

    http://localhost:5101/evaluate/adfify/dis/<discussion_id>/user/<user_id>/opinion_strict 
         
Example pipeline for ADF evaluation using YADF, lpopt, gringo and clasp (get preferred models for user 1 in discussion 2):

    curl -s 'http://localhost:5101/evaluate/adfify/dis/2/user/1' | jq -r '.adf' > temp.dl; java -jar yadf_2.11-0.1.0.jar -prf temp.dl | lpopt | gringo | clasp -n 0 --outf=2; rm temp.dl;   
     
Web sources:

- YADF: https://www.dbai.tuwien.ac.at/proj/adf/yadf/
- DIAMOND: http://diamond-adf.sourceforge.net/
- gringo/clasp: https://potassco.org/
- lpopt: https://www.dbai.tuwien.ac.at/research/project/lpopt/
