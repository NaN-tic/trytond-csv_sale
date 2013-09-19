CSV Sale Import
###############

The csv_sale module allows to import sales from csv files.

Configuration
=============

Importing sales from csv files taken as attachments of emails that are
downloaded automatically via a scheduler, requires additional configuration.
To do this, open the Group menu, select the group "CSV Import Administrator",
and in the tab "Access Permissions" add models "Sale" and "Sale Line" with
permission to read, modify, create and delete.
