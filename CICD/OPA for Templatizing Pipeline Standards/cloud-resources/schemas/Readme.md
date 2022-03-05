## This is initial work related to cerberus based yaml validation
### Objectives
* Allow validation of yaml content based on associated schema defined in yaml
* Validation should be performed in as simple manner as possible without any complex calling python code.
* Validation constraint should focus on enforcing presence of required elements but not necessarily the content. Strict content validation should be  delegated to policy enforcement at k8s level.

### Main Cerberus features and their applicability in KCC framework
| Cerberus Feature         | Applicability in KCC  |
| ------------- |-------------|
| Support for basic primitive types: string, number | **YES** |
| Support for composite types: list, dict | **YES** |
| Allows for more than one type for the element | **YES** |
| Allows to use different schemas for element (anyof_schema) | possible |
| Support regex validation of the element content |  **YES** |
| Allow for generic regular expression enforcement for key/value of the dict like structure | **YES** |
| Allows to define dependencies between elements to define situations like such a) one element must be present when the other one is ( inclusion )  b) one element must be present but only the other one is absent ( exclusion )| **YES** |
| Allows to define ‘unknown element breaks validation’ on per element level |  **YES** |
| Rich features that require introduction of custom module in python validator layer: a) Support for schema registries b) Custom validators c) Normalizer ( ability to force “normalization” changes in element content, purge unknown elements, apply defaults to missing elements ) d) Custom rules | NO |

### Project input vars validation schemas
The schemas are located in **schemas/gcp_project_schemas**

#### References:
* [Cerberus](https://docs.python-cerberus.org/en/stable/)
* [Presentation by author of module](https://www.youtube.com/watch?v=vlHAjIPvoT4)
* [Blog on custom validator](https://codingnetworker.com/2016/03/validate-json-data-using-cerberus/)