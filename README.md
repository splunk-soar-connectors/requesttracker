[comment]: # "Auto-generated SOAR connector documentation"
# Request Tracker

Publisher: Splunk  
Connector Version: 2\.2\.0  
Product Vendor: Best Practical Solutions  
Product Name: Request Tracker  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.2\.0  

This app allows ticket management on Request Tracker

[comment]: # " File: README.md"
[comment]: # " Copyright (c) 2016-2022 Splunk Inc."
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
**device\_url** |  required  | string | Device URL, e\.g\. http\://rt\.enterprise\.com
**username** |  optional  | string | Username
**password** |  optional  | password | Password

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity\. This action runs a quick query on the device to check the connection and credentials  
[create ticket](#action-create-ticket) - Create a ticket  
[update ticket](#action-update-ticket) - Update an existing ticket  
[list tickets](#action-list-tickets) - Get a list of tickets  
[get ticket](#action-get-ticket) - Get information about a single ticket  
[list attachments](#action-list-attachments) - List all attachments for a ticket  
[get attachment](#action-get-attachment) - Download attachment to vault  
[add attachment](#action-add-attachment) - Upload vaulted file as attachment to ticket  

## action: 'test connectivity'
Validate the asset configuration for connectivity\. This action runs a quick query on the device to check the connection and credentials

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
**owner** |  optional  | Owner \(Assigned to\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.owner | string | 
action\_result\.parameter\.priority | string | 
action\_result\.parameter\.queue | string |  `rt queue` 
action\_result\.parameter\.subject | string | 
action\_result\.parameter\.text | string | 
action\_result\.data\.\*\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.subject | string | 
action\_result\.summary\.new\_ticket\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update ticket'
Update an existing ticket

Type: **generic**  
Read only: **False**

Use this action to set the <b>subject</b> or add a <b>comment</b> to an existing ticket\. If the <b>subject</b> paramter is set and the <b>fields</b> parameter contains a subject field, the <b>subject</b> parameter will take priority\. The <b>fields parameter</b> is provided to allow flexibility in updating a ticket\. The parameter allows you to update all fields exposed via the request tracker API\. In order to look at available fields, please visit the API documentation at https\://rt\-wiki\.bestpractical\.com/wiki/REST\#Ticket\_Create\. Data needs to be in valid JSON format\. Example\: \{"Status"\: "open"\}\. If unknown fields are included, the action will pass, but the unknown fields will be logged\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID to update | string |  `rt ticket id` 
**fields** |  optional  | Fields to update \(JSON format\) | string | 
**comment** |  optional  | Comment to add to ticket history | string | 
**subject** |  optional  | Subject of ticket to be updated | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.fields | string | 
action\_result\.parameter\.id | string |  `rt ticket id` 
action\_result\.parameter\.subject | string | 
action\_result\.data\.\*\.admin\_cc | string | 
action\_result\.data\.\*\.cc | string | 
action\_result\.data\.\*\.created | string | 
action\_result\.data\.\*\.creator | string | 
action\_result\.data\.\*\.due | string | 
action\_result\.data\.\*\.final\_Priority | string | 
action\_result\.data\.\*\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.initial\_priority | string | 
action\_result\.data\.\*\.owner | string | 
action\_result\.data\.\*\.priority | string | 
action\_result\.data\.\*\.queue | string | 
action\_result\.data\.\*\.requestors | string | 
action\_result\.data\.\*\.resolved | string | 
action\_result\.data\.\*\.started | string | 
action\_result\.data\.\*\.starts | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.time\_estimated | string | 
action\_result\.data\.\*\.time\_left | string | 
action\_result\.data\.\*\.time\_worked | string | 
action\_result\.data\.\*\.told | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list tickets'
Get a list of tickets

Type: **generic**  
Read only: **True**

The value for the <b>query</b> parameter can be generated by Request Tracker's query builder\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**queue** |  optional  | Queue to get the list from | string |  `rt queue` 
**query** |  optional  | Additional parameters to query for | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.query | string | 
action\_result\.parameter\.queue | string |  `rt queue` 
action\_result\.data\.\*\.admin\_cc | string | 
action\_result\.data\.\*\.cc | string | 
action\_result\.data\.\*\.created | string | 
action\_result\.data\.\*\.creator | string | 
action\_result\.data\.\*\.due | string | 
action\_result\.data\.\*\.final\_Priority | string | 
action\_result\.data\.\*\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.initial\_priority | string | 
action\_result\.data\.\*\.owner | string | 
action\_result\.data\.\*\.priority | string | 
action\_result\.data\.\*\.queue | string | 
action\_result\.data\.\*\.requestors | string | 
action\_result\.data\.\*\.resolved | string | 
action\_result\.data\.\*\.started | string | 
action\_result\.data\.\*\.starts | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.time\_estimated | string | 
action\_result\.data\.\*\.time\_left | string | 
action\_result\.data\.\*\.time\_worked | string | 
action\_result\.data\.\*\.told | string | 
action\_result\.summary\.total\_issues | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get ticket'
Get information about a single ticket

Type: **generic**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.admin\_cc | string | 
action\_result\.data\.\*\.cc | string | 
action\_result\.data\.\*\.created | string | 
action\_result\.data\.\*\.creator | string | 
action\_result\.data\.\*\.due | string | 
action\_result\.data\.\*\.final\_Priority | string | 
action\_result\.data\.\*\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.initial\_priority | string | 
action\_result\.data\.\*\.owner | string | 
action\_result\.data\.\*\.priority | string | 
action\_result\.data\.\*\.queue | string | 
action\_result\.data\.\*\.requestors | string | 
action\_result\.data\.\*\.resolved | string | 
action\_result\.data\.\*\.started | string | 
action\_result\.data\.\*\.starts | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.time\_estimated | string | 
action\_result\.data\.\*\.time\_left | string | 
action\_result\.data\.\*\.time\_worked | string | 
action\_result\.data\.\*\.told | string | 
action\_result\.summary\.total\_issues | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list attachments'
List all attachments for a ticket

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.attachment\_id | string |  `rt attachment id` 
action\_result\.data\.\*\.content\_type | string | 
action\_result\.data\.\*\.path | string | 
action\_result\.data\.\*\.size | string | 
action\_result\.data\.\*\.ticket\_id | string |  `rt ticket id` 
action\_result\.summary\.attachments | numeric | 
action\_result\.summary\.failed\_tickets | numeric | 
action\_result\.summary\.succesful\_tickets | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get attachment'
Download attachment to vault

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 
**attachment\_id** |  required  | Attachment ID | string |  `rt attachment id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.attachment\_id | string |  `rt attachment id` 
action\_result\.parameter\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.attachment\_id | string |  `rt attachment id` 
action\_result\.data\.\*\.id | string |  `rt ticket id` 
action\_result\.data\.\*\.md5 | string |  `md5` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.path | string | 
action\_result\.data\.\*\.sha1 | string |  `sha1` 
action\_result\.data\.\*\.sha256 | string |  `sha256` 
action\_result\.data\.\*\.size | string | 
action\_result\.data\.\*\.vault\_id | string |  `vault id` 
action\_result\.summary\.attachments | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add attachment'
Upload vaulted file as attachment to ticket

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Ticket ID | string |  `rt ticket id` 
**vault\_id** |  required  | Vault ID | string |  `vault id` 
**comment** |  optional  | Comment to include with upload | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.id | string |  `rt ticket id` 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 