[comment]: # "Auto-generated SOAR connector documentation"
# Request Tracker

Publisher: Splunk  
Connector Version: 2.3.0  
Product Vendor: Best Practical Solutions  
Product Name: Request Tracker  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.0.0  

This app allows ticket management on Request Tracker

[comment]: # " File: README.md"
[comment]: # " Copyright (c) 2016-2023 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
  
**NOTE -**

-   To add a new line in action parameter value "\\n" needs to be added in the parameter value (e.g.
    "line 1 \\n line 2") for "text" and "subject" parameters of "create ticket" action, "comment"
    and "subject" parameters of "update ticket" action and "comment" parameter of "add attachment"
    action.
-   RequestTracker expects each new line to be preceded by a space if the text contains multiple
    lines, and that behavior is handled in the code for "create ticket", "update ticket" and "add
    attachment" actions.

## Port Information

The app uses the HTTP/ HTTPS protocol for communicating with the RequestTracker server. Below are
the default ports used by Splunk SOAR.

|         Service Name | Transport Protocol | Port |
|----------------------|--------------------|------|
|         http         | tcp                | 80   |
|         https        | tcp                | 443  |


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Request Tracker asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**device_url** |  required  | string | Device URL, e.g. http://rt.enterprise.com
**username** |  optional  | string | Username
**password** |  optional  | password | Password

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity. This action runs a quick query on the device to check the connection and credentials  
[create ticket](#action-create-ticket) - Create a ticket  
[update ticket](#action-update-ticket) - Update an existing ticket  
[list tickets](#action-list-tickets) - Get a list of tickets  
[get ticket](#action-get-ticket) - Get information about a single ticket  
[list attachments](#action-list-attachments) - List all attachments for a ticket  
[get attachment](#action-get-attachment) - Download attachment to vault  
[add attachment](#action-add-attachment) - Upload vaulted file as attachment to ticket  

## action: 'test connectivity'
Validate the asset configuration for connectivity. This action runs a quick query on the device to check the connection and credentials

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'create ticket'
Create a ticket

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**queue** |  optional  | Queue to add the ticket to | string |  `rt queue` 
**subject** |  required  | Subject of the ticket | string | 
**text** |  required  | Text of the ticket | string | 
**priority** |  optional  | Priority of the ticket | string | 
**owner** |  optional  | Owner (Assigned to) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.owner | string |  |  
action_result.parameter.priority | string |  |   0 
action_result.parameter.queue | string |  `rt queue`  |  
action_result.parameter.subject | string |  |   Test Subject 
action_result.parameter.text | string |  |   Test Text 
action_result.data.\*.id | string |  `rt ticket id`  |   4229 
action_result.data.\*.subject | string |  |   Test Subject 
action_result.summary.new_ticket_id | string |  |   4229 
action_result.message | string |  |   New ticket id: 4229 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'update ticket'
Update an existing ticket

Type: **generic**  
Read only: **False**

Use this action to set the <b>subject</b> or add a <b>comment</b> to an existing ticket. If the <b>subject</b> paramter is set and the <b>fields</b> parameter contains a subject field, the <b>subject</b> parameter will take priority. The <b>fields parameter</b> is provided to allow flexibility in updating a ticket. The parameter allows you to update all fields exposed via the request tracker API. In order to look at available fields, please visit the API documentation at https://rt-wiki.bestpractical.com/wiki/REST#Ticket_Create. Data needs to be in valid JSON format. Example: {"Status": "open"}. If unknown fields are included, the action will pass, but the unknown fields will be logged.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID to update | string |  `rt ticket id` 
**fields** |  optional  | Fields to update (JSON format) | string | 
**comment** |  optional  | Comment to add to ticket history | string | 
**subject** |  optional  | Subject of ticket to be updated | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   Test comment 
action_result.parameter.fields | string |  |  
action_result.parameter.id | string |  `rt ticket id`  |   4190 
action_result.parameter.subject | string |  |   Test Subject 
action_result.data.\*.admin_cc | string |  |  
action_result.data.\*.cc | string |  |  
action_result.data.\*.created | string |  |   Thu Jan 13 00:48:36 2022 
action_result.data.\*.creator | string |  |   root 
action_result.data.\*.due | string |  |   Not set 
action_result.data.\*.final_Priority | string |  |   0 
action_result.data.\*.id | string |  `rt ticket id`  |   4190 
action_result.data.\*.initial_priority | string |  |   0 
action_result.data.\*.owner | string |  |   Nobody 
action_result.data.\*.priority | string |  |   0 
action_result.data.\*.queue | string |  |   General 
action_result.data.\*.requestors | string |  |  
action_result.data.\*.resolved | string |  |   Not set 
action_result.data.\*.started | string |  |   Not set 
action_result.data.\*.starts | string |  |   Not set 
action_result.data.\*.status | string |  |   new 
action_result.data.\*.subject | string |  |   Test Subject 
action_result.data.\*.time_estimated | string |  |   0 
action_result.data.\*.time_left | string |  |   0 
action_result.data.\*.time_worked | string |  |   0 
action_result.data.\*.told | string |  |   Not set 
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list tickets'
Get a list of tickets

Type: **generic**  
Read only: **True**

The value for the <b>query</b> parameter can be generated by Request Tracker's query builder.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**queue** |  optional  | Queue to get the list from | string |  `rt queue` 
**query** |  optional  | Additional parameters to query for | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.query | string |  |   subject LIKE "Test" 
action_result.parameter.queue | string |  `rt queue`  |   1 
action_result.data.\*.admin_cc | string |  |  
action_result.data.\*.cc | string |  |  
action_result.data.\*.created | string |  |   Mon Feb 08 23:47:48 2021 
action_result.data.\*.creator | string |  |   root 
action_result.data.\*.due | string |  |   Not set 
action_result.data.\*.final_Priority | string |  |   0 
action_result.data.\*.id | string |  `rt ticket id`  |   660 
action_result.data.\*.initial_priority | string |  |   0 
action_result.data.\*.owner | string |  |   root 
action_result.data.\*.priority | string |  |   2 
action_result.data.\*.queue | string |  |   General 
action_result.data.\*.requestors | string |  |  
action_result.data.\*.resolved | string |  |   Not set 
action_result.data.\*.started | string |  |   Not set 
action_result.data.\*.starts | string |  |   Not set 
action_result.data.\*.status | string |  |   new 
action_result.data.\*.subject | string |  |   Test Subject 
action_result.data.\*.time_estimated | string |  |   0 
action_result.data.\*.time_left | string |  |   0 
action_result.data.\*.time_worked | string |  |   0 
action_result.data.\*.told | string |  |   Not set 
action_result.summary.total_issues | numeric |  |   2 
action_result.message | string |  |   Total issues: 2 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get ticket'
Get information about a single ticket

Type: **generic**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `rt ticket id`  |   665 
action_result.data.\*.admin_cc | string |  |  
action_result.data.\*.cc | string |  |  
action_result.data.\*.created | string |  |   Wed Mar 10 19:54:20 2021 
action_result.data.\*.creator | string |  |   root 
action_result.data.\*.due | string |  |   Not set 
action_result.data.\*.final_Priority | string |  |   0 
action_result.data.\*.id | string |  `rt ticket id`  |   665 
action_result.data.\*.initial_priority | string |  |   0 
action_result.data.\*.owner | string |  |   Nobody 
action_result.data.\*.priority | string |  |   0 
action_result.data.\*.queue | string |  |   General 
action_result.data.\*.requestors | string |  |  
action_result.data.\*.resolved | string |  |   Not set 
action_result.data.\*.started | string |  |   Not set 
action_result.data.\*.starts | string |  |   Not set 
action_result.data.\*.status | string |  |   new 
action_result.data.\*.subject | string |  |   Test Subject 
action_result.data.\*.time_estimated | string |  |   0 
action_result.data.\*.time_left | string |  |   0 
action_result.data.\*.time_worked | string |  |   0 
action_result.data.\*.told | string |  |   Not set 
action_result.summary.total_issues | numeric |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list attachments'
List all attachments for a ticket

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `rt ticket id`  |   665 
action_result.data.\*.attachment_id | string |  `rt attachment id`  |   876 
action_result.data.\*.content_type | string |  |   text/plain 
action_result.data.\*.path | string |  |   (Unnamed) 
action_result.data.\*.size | string |  |   88b 
action_result.data.\*.ticket_id | string |  `rt ticket id`  |   665 
action_result.summary.attachments | numeric |  |   1 
action_result.summary.failed_tickets | numeric |  |  
action_result.summary.succesful_tickets | numeric |  |  
action_result.message | string |  |   Attachments: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get attachment'
Download attachment to vault

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 
**attachment_id** |  required  | Attachment ID | string |  `rt attachment id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.attachment_id | string |  `rt attachment id`  |   876 
action_result.parameter.id | string |  `rt ticket id`  |   665 
action_result.data.\*.attachment_id | string |  `rt attachment id`  |   876 
action_result.data.\*.id | string |  `rt ticket id`  |   665 
action_result.data.\*.md5 | string |  `md5`  |   00ac4b437639520bb2f7f891ffb1b66e 
action_result.data.\*.name | string |  |   Test Name 
action_result.data.\*.path | string |  |   /opt/xyz/abc/41/e0/41e049c4c6aaa5a53f4c3f8e4f64d1d89f8300a3 
action_result.data.\*.sha1 | string |  `sha1`  |   41e049c4c6aaa5a53f4c3f8e4f64d1d89f8300a3 
action_result.data.\*.sha256 | string |  `sha256`  |   c34ff9d842a0c7bbfd64bedcd6c73ace44624b36c882b296b9778887ed862917 
action_result.data.\*.size | string |  |   88 
action_result.data.\*.vault_id | string |  `vault id`  |   41e049c4c6aaa5a53f4c3f8e4f64d1d89f8300a3 
action_result.summary.attachments | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add attachment'
Upload vaulted file as attachment to ticket

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 
**vault_id** |  required  | Vault ID | string |  `vault id` 
**comment** |  optional  | Comment to include with upload | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   Test comment 
action_result.parameter.id | string |  `rt ticket id`  |   3960 
action_result.parameter.vault_id | string |  `vault id`  |   4c309a10150910b52212e53c3f8098fc54d170c1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 