# File: requesttracker_connector.py
#
# Copyright (c) 2016-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Phantom imports
import json
import re

import phantom.app as phantom
import requests
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.rules import vault_info
from phantom.vault import Vault

from requesttracker_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class RTConnector(BaseConnector):
    # actions supported by this script
    ACTION_ID_CREATE_TICKET = "create_ticket"
    ACTION_ID_LIST_TICKETS = "list_tickets"
    ACTION_ID_GET_TICKET = "get_ticket"
    ACTION_ID_UPDATE_TICKET = "update_ticket"
    ACTION_ID_LIST_ATTACHMENTS = "list_attachments"
    ACTION_ID_GET_ATTACHMENT = "get_attachment"
    ACTION_ID_ADD_ATTACHMENT = "add_attachment"

    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._host = None
        self._session = None
        self._base_url = None
        self._username = None
        self._password = None

    def initialize(self):
        config = self.get_config()

        # Grab config variables
        request_url = config[RT_JSON_DEVICE_URL].strip("/")
        self._base_url = f"{request_url}/REST/1.0/"
        self._host = self._base_url[request_url.find("//") + 2 :]
        self._username = config.get(phantom.APP_JSON_USERNAME)
        self._password = config.get(phantom.APP_JSON_PASSWORD)

        # Create a sessions to manage cookies
        self._session = requests.Session()

        # Set validator for ticket and attachment ID inputs
        self.set_validator("rt ticket id", self._is_rt_id)
        self.set_validator("rt attachment id", self._is_rt_id)

        return phantom.APP_SUCCESS

    def _get_error_message_from_exception(self, e):
        """
        Get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        error_code = None
        error_msg = ERROR_MSG_UNAVAILABLE

        self.error_print("Error occurred.", e)

        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except Exception as e:
            self.error_print(f"Error occurred while fetching exception information. Details: {e!s}")

        if not error_code:
            error_text = f"Error Message: {error_msg}"
        else:
            error_text = f"Error Code: {error_code}. Error Message: {error_msg}"

        error_text = re.sub(r"pass=[^\s]*", "pass=[masked]", error_text)
        return error_text

    def _process_empty_reponse(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, RT_ERROR_EMPTY_RESPONSE.format(code=response.status_code)), None)

    def _process_text_response(self, response, action_result):
        # A text reponse is expected for every action
        response_text = response.text
        self.debug_print(response_text)

        # The body of the response can be empty
        if response.status_code == 200 and not response_text.strip():
            return RetVal(action_result.set_status(phantom.APP_SUCCESS), response_text)

        # The status code given by response.status_code will be 200 even when certain failures happen
        # This line will extract the actual status code from the body of the response
        status_code = int(re.findall(r"\d{3}", response_text[: response_text.index("\n")])[0])
        self.debug_print(status_code)

        # Please specify the status codes here
        if 200 <= status_code < 399:
            return RetVal(action_result.set_status(phantom.APP_SUCCESS), response_text)

        message = f"Status Code: {status_code}. Data from server:\n{response_text}\n"
        message = message.replace("{", "{{").replace("}", "}}")

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except Exception:
            error_text = "Cannot parse error details"

        message = f"Status Code: {status_code}. Data from server:\n{error_text}\n"

        message = message.replace("{", "{{").replace("}", "}}")

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Unable to parse JSON response. Error: {error_message}"), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            if "error" in resp_json:
                return RetVal(action_result.set_status(phantom.APP_ERROR, "API returned an error. Error: {}".format(resp_json["error"])), None)
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {} Data from server: {}".format(r.status_code, r.text.replace("{", "{{").replace("}", "}}"))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if "json" in r.headers.get("Content-Type", ""):
            return self._process_json_response(r, action_result)

        # Process an HTML resonse, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        if "text" in r.headers.get("Content-Type", ""):
            return self._process_text_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {} Data from server: {}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, files=None, method="get"):
        resp_json = None

        try:
            request_func = getattr(self._session, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), resp_json)

        if params is None:
            params = {}

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(url, data=data, files=files, headers=headers, params=params)
        except Exception as e:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, f"Error Connecting to server. Details: {self._get_error_message_from_exception(e)}"),
                resp_json,
            )

        if self.get_action_identifier() == self.ACTION_ID_GET_ATTACHMENT and endpoint.endswith("content"):
            return phantom.APP_SUCCESS, r

        return self._process_response(r, action_result)

    def _create_rt_session(self, action_result):
        params = None
        if self._username and self._password:
            params = {"user": self._username, "pass": self._password}

        ret_val, response = self._make_rest_call("", action_result, params=params, headers=None)

        return ret_val

    def _is_rt_id(self, rt_id):
        # Check that ticket and attachment IDs are integers
        try:
            if int(rt_id) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    def handle_multiline_text(self, text):
        # Function to handle multiline text properly
        if "\n" in text:
            text = text.replace("\n", "\n ")

        if "\\n" in text:
            text = text.replace("\\n", "\n ")

        return text

    def handle_multiline_subject(self, subject):
        # Function to handle multiline subject properly
        if "\n" in subject:
            subject_text_list = [text.strip() for text in subject.split("\n")]
            subject = " ".join(subject_text_list)

        if "\\n" in subject:
            subject_text_list = [text.strip() for text in subject.split("\\n")]
            subject = " ".join(subject_text_list)

        return subject

    def _test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(param))

        # Progress
        self.save_progress(RT_USING_BASE_URL, base_url=self._base_url)

        # Connectivity
        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, self._host)

        # Create RT Session
        if phantom.is_fail(self._create_rt_session(action_result)):
            self.save_progress("Test Connectivity Failed")
            return phantom.APP_ERROR

        self.save_progress("Test Connectivity Passed")
        return phantom.APP_SUCCESS

    def _update_ticket(self, param):
        action_result = self.add_action_result(ActionResult(param))

        # Progress
        self.save_progress(RT_USING_BASE_URL, base_url=self._base_url)

        # Connectivity
        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, self._host)

        # Create RT Session
        if phantom.is_fail(self._create_rt_session(action_result)):
            return phantom.APP_ERROR

        ticket_id = param[RT_JSON_ID]
        fields = param.get(RT_JSON_FIELDS)
        subject = param.get(RT_JSON_SUBJECT)
        comment = param.get(RT_JSON_COMMENT)

        if not any([fields, subject, comment]):
            return action_result.set_status(phantom.APP_ERROR, "At least one parameter of fields, subject, or comment is required")

        if fields:
            try:
                fields = json.loads(str(fields))
                if isinstance(fields, list):
                    fields = {key: value for x in fields for key, value in x.items()}
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, "Fields paramter is not valid JSON", error_message)
        else:
            fields = {}

        if subject:
            fields["Subject"] = self.handle_multiline_subject(subject)

        if fields:
            # Create the content string
            content = {"content": "\n".join([f"{k}: {v}" for k, v in fields.items()])}

            # Send the edit post request
            ret_val, resp_text = self._make_rest_call(f"ticket/{ticket_id}/edit", action_result, data=content, method="post")

            if phantom.is_fail(ret_val):
                return ret_val

            self.debug_print(resp_text)

            for line in resp_text.split("\n"):
                if line.startswith("#") and "Unknown field" in line:
                    self.debug_print("WARNING: {} is an unknown field and was not included in ticket update".format(line.split(":")[0][2:]))

        if comment:
            self.save_progress("Adding comment")

            comment = self.handle_multiline_text(comment)

            # Create the content dictionary
            content = {"content": f"id: {ticket_id}\nAction: comment\nText: {comment}"}

            # Send the comment post request
            ret_val, resp_text = self._make_rest_call(f"ticket/{ticket_id}/comment", action_result, data=content, method="post")

            if phantom.is_fail(ret_val):
                return ret_val

        self.save_progress("Ticket updated")

        if phantom.is_fail(self._get_ticket_details(ticket_id, action_result)):
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, RT_SUCC_UPDATE_TICKET)

    def _create_ticket(self, param):
        # Create action result
        action_result = self.add_action_result(ActionResult(param))

        # Create RT object
        if phantom.is_fail(self._create_rt_session(action_result)):
            return action_result.get_status()

        queue = param.get(RT_JSON_QUEUE, DEFAULT_QUEUE)
        subject = param[RT_JSON_SUBJECT]
        text = param[RT_JSON_TEXT]
        priority = param.get(RT_JSON_PRIORITY, DEFAULT_PRIORITY)
        owner = param.get(RT_JSON_OWNER)

        subject = self.handle_multiline_subject(subject)
        text = self.handle_multiline_text(text)

        # create the content dictionary
        content = {
            "content": f"Queue: {queue}\nSubject: {subject}\nText: {text} \n \n ---- \n {RT_TICKET_FOOTNOTE}{self.get_container_id()}\nPriority: {priority}\nOwner: {owner}"
        }

        ret_val, resp_text = self._make_rest_call("ticket/new", action_result, data=content, method="post")

        if phantom.is_fail(ret_val):
            return ret_val

        if "# Could not create ticket." in resp_text:
            if "Queue not set" in resp_text:
                return action_result.set_status(phantom.APP_ERROR, "Error creating ticket. Invalid queue given.")
            return action_result.set_status(phantom.APP_ERROR, f"Error creating ticket. Response from server:\n{resp_text}")

        ticket_id = None

        for line in resp_text.split("\n"):
            if line.startswith("#"):
                if "Unknown field" in line:
                    self.debug_print("WARNING: {} is an unknown field and was not included in ticket creation".format(line.split(":")[0][2:]))
                else:
                    ticket_id = re.findall(r"\d+", line)[0]

        if not ticket_id:
            return action_result.set_status(phantom.APP_ERROR, "Ticket creation failed")

        self.save_progress(RT_CREATED_TICKET)

        data = {}

        action_result.add_data(data)
        data[RT_JSON_ID] = ticket_id
        data[RT_JSON_SUBJECT] = param[RT_JSON_SUBJECT]

        action_result.set_summary({RT_JSON_NEW_TICKET_ID: ticket_id})

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_ticket_details(self, ticket_id, action_result):
        # Query the device for details about the ticket
        ret_val, resp_text = self._make_rest_call(f"ticket/{ticket_id}/show", action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        if re.findall("# Ticket .+ does not exist.", resp_text):
            return action_result.set_status(phantom.APP_ERROR, f"Ticket {ticket_id} does not exist.")

        ticket_info = {}

        for line in resp_text.split("\n"):
            if ":" in line:
                spl_line = line.split(":")
                key = spl_line[0]
                value = ":".join(spl_line[1:])
                ticket_info[key] = value.strip()

        data = {}
        data[RT_JSON_ID] = ticket_id
        data[RT_JSON_QUEUE] = ticket_info.get("Queue")
        data[RT_JSON_OWNER] = ticket_info.get("Owner")
        data[RT_JSON_CREATOR] = ticket_info.get("Creator")
        data[RT_JSON_SUBJECT] = ticket_info.get("Subject")
        data[RT_JSON_STATUS] = ticket_info.get("Status")
        data[RT_JSON_PRIORITY] = ticket_info.get("Priority")
        data[RT_JSON_INITIALPRIORITY] = ticket_info.get("InitialPriority")
        data[RT_JSON_FINALPRIORITY] = ticket_info.get("FinalPriority")
        data[RT_JSON_REQUESTORS] = ticket_info.get("Requestors")
        data[RT_JSON_CC] = ticket_info.get("Cc")
        data[RT_JSON_ADMINCC] = ticket_info.get("AdminCc")
        data[RT_JSON_CREATED] = ticket_info.get("Created")
        data[RT_JSON_STARTS] = ticket_info.get("Starts")
        data[RT_JSON_STARTED] = ticket_info.get("Started")
        data[RT_JSON_DUE] = ticket_info.get("Due")
        data[RT_JSON_RESOLVED] = ticket_info.get("Resolved")
        data[RT_JSON_TOLD] = ticket_info.get("Told")
        data[RT_JSON_TIMEESTIMATED] = ticket_info.get("TimeEstimated")
        data[RT_JSON_TIMEWORKED] = ticket_info.get("TimeWorked")
        data[RT_JSON_TIMELEFT] = ticket_info.get("TimeLeft")

        action_result.add_data(data)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_ticket(self, param):
        self.save_progress("starting get tickets")
        # Create action results
        action_result = self.add_action_result(ActionResult(param))

        self.debug_print("Creating rt session")
        # Create RT session
        if phantom.is_fail(self._create_rt_session(action_result)):
            return action_result.get_status()

        # get the ticket ID
        ticket_id = param[RT_JSON_ID]
        self.debug_print("Getting ticket details")
        if phantom.is_fail(self._get_ticket_details(ticket_id, action_result)):
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, RT_SUCC_GET_TICKET)

    def _list_tickets(self, param):
        # Create the action result
        action_result = self.add_action_result(ActionResult(param))

        # Create RT session
        if phantom.is_fail(self._create_rt_session(action_result)):
            return action_result.get_status()

        queue = param.get(RT_JSON_QUEUE, DEFAULT_QUEUE)
        query = param.get(RT_JSON_QUERY, "").strip()

        if query and not query.startswith("AND"):
            query = f" AND {query}"

        # Set up the query
        query = f"Queue='{queue}'{query}"

        # Query the device for the list of tickets
        ret_val, resp_text = self._make_rest_call("search/ticket", action_result, params={"query": query})

        if phantom.is_fail(ret_val):
            return ret_val

        if "No matching results." in resp_text:
            return action_result.set_status(phantom.APP_SUCCESS, "Query returned no results")

        # Get ticket ID for each line in response
        tickets = [x.split(":")[0] for x in resp_text.strip().split("\n")[2:]]

        if tickets and "Invalid query" in tickets[0]:
            return action_result.set_status(phantom.APP_ERROR, f"Given query is invalid. Details:\n\n{resp_text}")

        # Tickets will be a list of tuples, where the first element will be the ticket ID and the second element will be the subject
        for ticket in tickets:
            ar = ActionResult()

            if phantom.is_fail(self._get_ticket_details(ticket, ar)):
                self.debug_print(f"Could not get ticket details for ID {ticket}: {ar.get_message()}")
                continue

            action_result.add_data(ar.get_data()[0])

        action_result.set_summary({RT_TOTAL_ISSUES: len(tickets)})

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_attachments(self, param):
        # Create action result
        action_result = self.add_action_result(ActionResult(param))

        # Create RT object
        if phantom.is_fail(self._create_rt_session(action_result)):
            return action_result.get_status()

        # Grab the ticket ID
        ticket_id = param[RT_JSON_ID]

        # Query the device for the list of attachments of the ticket
        ret_val, resp_text = self._make_rest_call(f"ticket/{ticket_id}/attachments", action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        if re.findall("# Ticket .+ does not exist.", resp_text):
            return action_result.set_status(phantom.APP_ERROR, f"Ticket {ticket_id} does not exist.")

        # Find the start of the attachments list
        resp_text = resp_text.strip()
        attachment_index = resp_text.index("Attachments:")

        if attachment_index == -1:
            self.save_progress(f"No attachments found for ticket id '{ticket_id}'")
            return action_result.set_status(phantom.APP_SUCCESS)

        # Each attachment it on a separate line in the third "block" of text
        attachments = [x.strip() for x in resp_text[attachment_index:].split("\n")]

        # Set the summary
        action_result.set_summary({"attachments": len(attachments)})

        # No reason to move on if we find no attachments
        if len(attachments) == 0:
            self.save_progress(f"No attachments found for ticket id '{ticket_id}'")
            return action_result.set_status(phantom.APP_SUCCESS)

        # The first line of the attachments block starts with "Attachments: "
        attachments[0] = attachments[0][13:]

        # Get the attachment metadata
        # Each line has the form "<attachment_id>: <file_name> (<content_type> / <size>)"
        # The file name could have spaces and parentheses which makes this difficult
        # But the filename will always be bordered by the first colon and the last open paren
        for attachment in attachments:
            data = {}

            data["ticket_id"] = ticket_id
            data["attachment_id"] = re.findall(r"\d+:", attachment)[0][:-1]

            start_path = attachment.find(":") + 2
            end_path = len(attachment) - attachment[::-1].find("(") - 2
            data["path"] = attachment[start_path:end_path]

            split_meta = attachment[end_path + 2 :].split("/")
            data["content_type"] = f"{split_meta[0]}/{split_meta[1].strip()}"
            data["size"] = split_meta[2][: -1 if attachment.endswith(")") else -2].strip()

            action_result.add_data(data)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_attachment(self, param):
        # Create action result
        action_result = self.add_action_result(ActionResult(param))

        # Create RT object
        if phantom.is_fail(self._create_rt_session(action_result)):
            return action_result.get_status()

        # Get parameters
        ticket_id = param[RT_JSON_ID]
        attachment_id = param[RT_JSON_ATTACHMENT]

        # Set up the result data
        data = action_result.add_data(dict())
        data["id"] = ticket_id
        data["attachment_id"] = attachment_id

        # Request the attachment meta data
        ret_val, resp_text = self._make_rest_call(f"ticket/{ticket_id}/attachments/{attachment_id}", action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        if "# Invalid attachment id" in resp_text:
            return action_result.set_status(phantom.APP_ERROR, f"Attachment with ID {attachment_id} not found on ticket {ticket_id}")

        if re.findall("# Ticket .+ does not exist.", resp_text):
            return action_result.set_status(phantom.APP_ERROR, f"Ticket {ticket_id} does not exist.")

        # Look for the filename in the meta data
        filename_index = resp_text.find("filename")

        if filename_index == -1:
            file_name = "noname"
            self.debug_print("Filename not found in header, setting to noname")
        else:
            start_filename = resp_text.find("=", filename_index) + 2
            end_filename = resp_text.find("\n", filename_index) - 1
            file_name = resp_text[start_filename:end_filename]

        if not file_name:
            file_name = "noname"
            self.save_progress("Filename not found in header, setting to noname")

        # Look for the file length in the meta data
        length_index = resp_text.find("Content-Length")

        if length_index == -1:
            return action_result.set_status(phantom.APP_ERROR, "Cannot find Content-Length of attachment")

        start_length = resp_text.find(":", length_index) + 2
        end_length = resp_text.find("\n", length_index)

        length = int(resp_text[start_length:end_length])

        if length == 0:
            return action_result.set_status(phantom.APP_SUCCESS, "File is empty, nothing to do here")

        # Request the attachment content
        ret_val, response = self._make_rest_call(f"ticket/{ticket_id}/attachments/{attachment_id}/content", action_result)

        # Convert to bytes and strip away headers and trailers.
        content = response.content

        if phantom.is_fail(ret_val):
            return ret_val

        # find first newline
        skip = content.find(b"\n")
        if skip == -1:
            return action_result.set_status(phantom.APP_ERROR, "Cannot find first line of file content")
        # skip first and second newline
        skip += 2

        # Let the actiond handle i/o exceptions and return the errors.
        ret_val = Vault.create_attachment(content[skip : length + skip], self.get_container_id(), file_name=file_name)

        if ret_val["succeeded"] is not True:
            return action_result.set_status(phantom.APP_ERROR, "Error saving file to vault: {}".format(ret_val.get("error", "Unknwon error")))

        vault_id = ret_val["vault_id"]
        _, _, file_info = vault_info(vault_id=vault_id, container_id=self.get_container_id())

        if len(file_info) == 0:
            return action_result.set_status(phantom.APP_ERROR, "File not found in vault after adding")

        file_info = file_info[0]

        data["vault_id"] = vault_id
        data["name"] = file_info["name"]
        data["size"] = file_info["size"]
        data["sha1"] = file_info["metadata"]["sha1"]
        data["sha256"] = file_info["metadata"]["sha256"]
        data["path"] = file_info["path"]

        if file_info["metadata"].get("md5"):
            data["md5"] = file_info["metadata"]["md5"]

        return action_result.set_status(phantom.APP_SUCCESS, RT_SUCC_GET_ATTACHMENT)

    def _add_attachment(self, param):
        # Create action result
        action_result = self.add_action_result(ActionResult(param))

        # Create RT object
        if phantom.is_fail(self._create_rt_session(action_result)):
            return action_result.get_status()

        # Get params
        ticket_id = param[RT_JSON_ID]
        vault_id = param[RT_JSON_VAULT]
        comment = param.get("comment")

        # Set default comment
        if not comment:
            comment = "File uploaded from Phantom"
        else:
            comment = self.handle_multiline_text(comment)

        # Check for vault file
        _, _, file_info = vault_info(vault_id=vault_id, container_id=self.get_container_id())

        if not file_info:
            return action_result.set_status(phantom.APP_ERROR, "Vault ID is invalid. Vault file not found")

        file_info = file_info[0]

        # Set mime_type
        file_content_type = file_info.get("mime_type", "application/octet-stream")

        if not file_info["name"]:
            file_info["name"] = vault_id

        # Create payload for request
        content = {"content": "Action: comment\nText: {}\nAttachment: {}".format(comment, file_info["name"])}
        upfile = {"attachment_1": (file_info["name"], open(file_info["path"], "rb"), file_content_type)}

        ret_val, resp_text = self._make_rest_call(f"ticket/{ticket_id}/comment", action_result, data=content, files=upfile, method="post")

        if phantom.is_fail(ret_val):
            return ret_val

        return action_result.set_status(phantom.APP_SUCCESS, RT_SUCC_ADD_ATTACHMENT)

    def handle_action(self, param):
        """Function that handles all the actions

        Args:

        Return:
            A status code
        """

        # Get the action that we are supposed to carry out, set it in the connection result object
        action = self.get_action_identifier()

        ret_val = phantom.APP_SUCCESS

        if action == self.ACTION_ID_CREATE_TICKET:
            ret_val = self._create_ticket(param)
        elif action == self.ACTION_ID_LIST_TICKETS:
            ret_val = self._list_tickets(param)
        elif action == self.ACTION_ID_GET_TICKET:
            ret_val = self._get_ticket(param)
        elif action == self.ACTION_ID_UPDATE_TICKET:
            ret_val = self._update_ticket(param)
        elif action == self.ACTION_ID_LIST_ATTACHMENTS:
            ret_val = self._list_attachments(param)
        elif action == self.ACTION_ID_GET_ATTACHMENT:
            ret_val = self._get_attachment(param)
        elif action == self.ACTION_ID_ADD_ATTACHMENT:
            ret_val = self._add_attachment(param)
        elif action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
            ret_val = self._test_connectivity(param)

        return ret_val


if __name__ == "__main__":
    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)
    argparser.add_argument("-v", "--verify", action="store_true", help="verify", required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            print("Accessing the Login page")
            login_url = RTConnector._get_phantom_base_url() + "/login"
            r = requests.get(login_url, verify=verify, timeout=DEFAULT_TIMEOUT)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, timeout=DEFAULT_TIMEOUT, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platfrom. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = RTConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
