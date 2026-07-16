**Unreleased**

* Fixed credential handling to keep passwords out of request URLs and diagnostic logs. (PAPP-37978)
* Rejected attachment filenames containing line breaks to prevent RT field injection. (PAPP-37978)
* Reclassified get attachment as a vault-writing action subject to normal execution controls. (PAPP-37978)
* Prevented get attachment from vaulting HTTP error responses as file content. (PAPP-37978)
