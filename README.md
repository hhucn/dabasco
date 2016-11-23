# D-BAS DoJ

Calculates degree of justification of individual statements or positions in
D-BAS. Requires D-BAS argument graph export data as served by the D-BAS export
interface.

## Documentation
TODO

## Setup

To run the service, execute:

    python app.py
    
This requires a running D-BAS instance on localhost.
Alternatively, provide the D-BAS export interface yourself and serve the json
export for each individual issue at:

    http://localhost:4284/export/doj/<issue_index>
    
To request all degrees of justifaction and all reason relations for an issue, use:

    http://localhost:5101/evaluate/all?issue=<issue_index>
    
To request all degrees of justifaction for an issue, use:

    http://localhost:5101/evaluate/dojs?issue=<issue_index>
    
To request the degrees of justifaction of specific statements in an issue, use:

    http://localhost:5101/evaluate/dojs?issue=<issue_index>&statements=<s1>,<s2>,...
    
Results are provided as JSON string. 

## Testing
TODO
