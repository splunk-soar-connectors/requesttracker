# File: requesttracker_consts.py
#
# Copyright (c) 2016-2023 Splunk Inc.
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

# Constants relating to JSON values
RT_JSON_DEVICE_URL = "device_url"
RT_JSON_PRIORITY = "priority"
RT_JSON_ID = "id"
RT_JSON_ATTACHMENT = "attachment_id"
RT_JSON_VAULT = "vault_id"
RT_JSON_QUEUE = "queue"
RT_JSON_OWNER = "owner"
RT_JSON_CREATOR = "creator"
RT_JSON_SUBJECT = "subject"
RT_JSON_STATUS = "status"
RT_JSON_INITIALPRIORITY = "initial_priority"
RT_JSON_FINALPRIORITY = "final_Priority"
RT_JSON_REQUESTORS = "requestors"
RT_JSON_CC = "cc"
RT_JSON_ADMINCC = "admin_cc"
RT_JSON_CREATED = "created"
RT_JSON_STARTS = "starts"
RT_JSON_STARTED = "started"
RT_JSON_DUE = "due"
RT_JSON_RESOLVED = "resolved"
RT_JSON_TOLD = "told"
RT_JSON_TIMEESTIMATED = "time_estimated"
RT_JSON_TIMEWORKED = "time_worked"
RT_JSON_TIMELEFT = "time_left"
RT_JSON_COMMENT = "comment"
RT_JSON_FIELDS = "fields"

RT_JSON_QUERY = "query"
RT_TOTAL_ISSUES = "total_issues"
RT_JSON_TEXT = "text"
RT_JSON_NEW_TICKET_ID = "new_ticket_id"

RT_ERR_CONNECTIVITY_TEST = "Connectivity test failed"
RT_SUCC_CONNECTIVITY_TEST = "Connectivity test passed"
RT_ERR_CREATE_TICKET_FAILED = "Ticket creation failed"
RT_ERR_LIST_TICKETS_FAILED = "Failed to get ticket listing"
RT_ERR_LOGIN_FAILED = "Login to RT server failed. Text from device '{status}'"
RT_CREATED_TICKET = "Created ticket"
RT_USING_BASE_URL = "Using url: {base_url}"
RT_ERR_NO_DATA_FROM_DEVICE = "Did not get valid data from device"
RT_ERR_UPDATE_SUBJECT_FAILED = "Update of subject failed"
RT_ERR_UPDATE_COMMENT_FAILED = "Update of comment failed"
RT_ERR_EMPTY_RESPONSE = "Status Code {code}. Empty response and no information in the header."

DEFAULT_PRIORITY = "0"
DEFAULT_QUEUE = "1"
DEFAULT_TIMEOUT = 30
RT_TICKET_FOOTNOTE = "Added by Phantom for container id: "
PHANTOM_VAULT_DIR = "/opt/phantom/vault/tmp/"

# Constants relating to 'get_error_message_from_exception'
ERR_CODE_MSG = "Error code unavailable"
ERR_MSG_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters."
PARSE_ERR_MSG = "Unable to parse the error message. Please check the asset configuration and|or action parameters."

RT_SUCC_ADD_ATTACHMENT = "Attachment added successfully"
RT_SUCC_GET_TICKET = "The ticket has been retrieved successfully"
RT_SUCC_UPDATE_TICKET = "The ticket has been updated successfully"
RT_SUCC_GET_ATTACHMENT = "The attachment has been retrieved successfully"
