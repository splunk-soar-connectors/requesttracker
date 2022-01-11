[comment]: # "Auto-generated SOAR connector documentation"
# Request Tracker

Publisher: Splunk  
Connector Version: 2\.0\.3  
Product Vendor: Best Practical Solutions  
Product Name: Request Tracker  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.10\.0\.40961  

This app allows ticket management on Request Tracker

## Port Information
The app uses HTTP/ HTTPS protocol for communicating with the RequestTracker server. Below are the default ports used by Splunk SOAR.

SERVICE NAME | TRANSPORT PROTOCOL | PORT
------------ | ------------------ | ----
**http** | tcp | 80
**https** | tcp | 443

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
[update ticket](#action-update-ticket) - Updates an existing ticket  
[list tickets](#action-list-tickets) - Get a list of tickets  
[get ticket](#action-get-ticket) - Get information about a single ticket  
[list attachments](#action-list-attachments) - List all attachments for a ticket  
[get attachment](#action-get-attachment) - Download attachment to vault  
[add attachment](#action-add-attachment) - Uploads vaulted file as attachment to ticket  

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
Updates an existing ticket

Type: **generic**  
Read only: **False**

Use this action to set the <b>subject</b> or add a <b>comment</b> to an existing ticket\. If the <b>subject</b> paramter is set and the <b>fields</b> parameter contains a subject field, the <b>subject</b> parameter will take priority\.

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
action\_result\.data\.\*\.md5 | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.path | string | 
action\_result\.data\.\*\.sha1 | string | 
action\_result\.data\.\*\.sha256 | string | 
action\_result\.data\.\*\.size | string | 
action\_result\.data\.\*\.vault\_id | string | 
action\_result\.summary\.attachments | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add attachment'
Uploads vaulted file as attachment to ticket

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
action\_result\.parameter\.id | string |  `rt ticket id` 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.comment | string | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 