**NOTE -**

- To add a new line in action parameter value "\\n" needs to be added in the parameter value (e.g.
  "line 1 \\n line 2") for "text" and "subject" parameters of "create ticket" action, "comment"
  and "subject" parameters of "update ticket" action and "comment" parameter of "add attachment"
  action.
- RequestTracker expects each new line to be preceded by a space if the text contains multiple
  lines, and that behavior is handled in the code for "create ticket", "update ticket" and "add
  attachment" actions.

## Port Information

The app uses the HTTP/ HTTPS protocol for communicating with the RequestTracker server. Below are
the default ports used by Splunk SOAR.

|         Service Name | Transport Protocol | Port |
|----------------------|--------------------|------|
|         http | tcp | 80 |
|         https | tcp | 443 |
