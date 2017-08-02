# dabasco - Evaluation module for D-BAS

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

    http://localhost:5101/evaluate/dungify/<discussion_id>    

The AF is provided in ASPARTIX format.

Example pipeline for Dung AF evaluation using conarg2 (get stable extensions of discussion 2):

    curl -s 'http://localhost:5101/evaluate/dungify/2' | jq -r '.af' > temp; ./conarg2 -e stable temp; rm temp;
    
Web sources:

- ASPARTIX documentation: https://www.dbai.tuwien.ac.at/proj/argumentation/systempage/docu.htm
- conarg website: http://www.dmi.unipg.it/conarg/

## TOAST/ASPIC Interface

To get a TOAST input format representation of a user opinion in a discussion, use:

    http://localhost:5101/evaluate/toastify/<discussion_id>/<user_id>

Example pipeline for evaluation using the TOAST Web service (evaluate discussion 2, user ID 1):

    curl http://localhost:5101/evaluate/toastify/2/1 | curl -d @- http://www.arg.dundee.ac.uk/toast/api/evaluate
    
Web sources:

- TOAST website: http://toast.arg-tech.org/help/web
- TOAST API: http://www.arg.dundee.ac.uk/toast/help/api
- TOAST interactive web interface: http://toast.arg-tech.org/
- TOAST web interface: http://www.arg.dundee.ac.uk/toast/api/evaluate

## ADF Interface

To get a YADF/DIAMOND formatted ADF representation of a user opinion in a discussion, use:
 
    http://localhost:5101/evaluate/adfify/<discussion_id>/<user_id>
         
Example pipeline for ADF evaluation using YADF, lpopt, gringo and clasp (get preferred models for user 1 in discussion 2):

    curl -s 'http://localhost:5101/evaluate/adfify/2/1' | jq -r '.adf' > temp.dl; java -jar yadf_2.11-0.1.0.jar -prf temp.dl | lpopt | gringo | clasp -n 0 --outf=2; rm temp.dl;   
     
Web sources:

- YADF: https://www.dbai.tuwien.ac.at/proj/adf/yadf/
- DIAMOND: https://isysrv.informatik.uni-leipzig.de/diamond
- gringo/clasp: http://potassco.sourceforge.net/
- lpopt: https://www.dbai.tuwien.ac.at/research/project/lpopt/

## Degrees of Justification

To request all degrees of justification for a discussion, use:

    http://localhost:5101/evaluate/dojs/<discussion_id>
    
To request the degrees of justification of specific statements (s1, s2, ...) in a discussion, use:

    http://localhost:5101/evaluate/dojs/<discussion_id>/<s1>,<s2>,...

To request the degree of justification of a specific position (given by comma separated IDs of accepted statements "acc1" and rejected statements "rej1") conditioned by another specific position (given by "acc2" and "rej2"), use:

    http://localhost:5101/evaluate/doj/<discussion_id>/pos1/acc/<acc1>/rej/<rej1>/pos2/acc/<acc2>/rej/<rej2>
    
All statement parameters are optional. When omitting a parameter, also omit the corresponding route element, e.g.:

    http://localhost:5101/evaluate/doj/<discussion_id>/pos1/rej/<rej1>/pos2/acc/<acc2>/rej/<rej2>
    http://localhost:5101/evaluate/doj/<discussion_id>/pos1/rej/<rej1>/pos2/acc/<acc2>
    http://localhost:5101/evaluate/doj/<discussion_id>/pos1/rej/<rej1>/pos2
    http://localhost:5101/evaluate/doj/<discussion_id>/pos1/pos2

To request the degree of justification of a user opinion (as provided by the user opinion export), use:

    http://localhost:5101/evaluate/doj/<discussion_id>/user/<user_id>

## Reasons

To request all reason relations for a discussion, use:

    http://localhost:5101/evaluate/reasons/<discussion_id>

To request the strength of reason of a specific statement s2 for/against a specific statement s1, use (either of):

    http://localhost:5101/evaluate/reasons/<discussion_id>/for/<s1>/by/<s2>
    http://localhost:5101/evaluate/reasons/<discussion_id>/by/<s2>/for/<s1>
                                             
To request the strength of reason of all statements for/against a specific statement s1, use:

    http://localhost:5101/evaluate/reasons/<discussion_id>/for/<s1>
        
To request the strength of reason of a specific statement s2 for/against all statements, use:

    http://localhost:5101/evaluate/reasons/<discussion_id>/by/<s2>
    
