# D-BAS DoJ

Calculates degree of justification of individual statements or positions in
D-BAS. Requires D-BAS argument graph export data as served by the D-BAS export
interface.
All results are provided as a JSON string.

## Documentation
TODO

## Setup

To run the service, execute:

    make run
    
Or alternatively:

    python dabasco/app.py
    
This module requires a running D-BAS instance on localhost.
Alternatively, provide the D-BAS export interface yourself and serve the json
export for the graph data and user opinion data at (respectively):

    http://localhost:4284/export/doj/<discussion_id>
    http://localhost:4284/export/doj_user/<user_id>/<discussion_id>
    
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

To request all reason relations for a discussion, use:

    http://localhost:5101/evaluate/reasons/<discussion_id>
     
## TOAST Interface

To get a TOAST input format representation of a user opinion in a discussion, use:

    http://localhost:5101/evaluate/toastify/<discussion_id>/<user_id>
     
Example to feed this into the TOAST Web service:

    curl http://localhost:5101/evaluate/toastify/2/39 | curl -d @- http://www.arg.dundee.ac.uk/toast/api/evaluate
    
## Dung AF Interface

To get a Dung-style argumentation framework (AF) representation of a discussion, use:

    http://localhost:5101/evaluate/dungify/<discussion_id>    

The AF is provided in ASPARTIX format.

An extended AF representation that also includes AF arguments for D-BAS statements can be obtained by:
 
    http://localhost:5101/evaluate/dungify_extended/<discussion_id> 

## Testing
TODO
