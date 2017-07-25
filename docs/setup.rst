.. _setup:

=====
Setup
=====

To install required python packages, execute:

   $ make dependencies

To run the service, execute:

   $ make run

This module requires a running D-BAS instance on localhost.
Alternatively, you can provide the D-BAS export interface yourself and serve the json export for the graph data and user opinion data at (respectively):

   http://localhost:4284/export/doj/<discussion_id>

   http://localhost:4284/export/doj_user/<user_id>/<discussion_id>

A small python web app that serves example D-BAS data is included. To run it, execute:

   $ python3 dbas_export_mockup.py

