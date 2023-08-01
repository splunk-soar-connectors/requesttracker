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
