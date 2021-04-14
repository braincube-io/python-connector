# braincube_connector: a python client for Braincube

## Description

The python package `braincube_connector` provides a tool for datascientists to access their data on Braincube directly from python.

## Installation

Install with pip:

```bash
pip install braincube_connector
```

## Configuration and Authentication

Since version `2.2.0`, the authentication uses a personal access token (PAT).

In order to create a PAT, you need to go in your braincube personal `menu > Account > Access tokens > +/Add`

The scopes of the token should include `BRAINCUBE` and `SSO_READ`.

Then two options exist to pass the PAT to the braincube_connector:
 1. Using a configuration dictionary when creating a client:
```python
from braincube_connector import client

client.get_instance(config_dict={"api_key":"<my_personal_access_token>", "domain":"mybraincube.com"})
```
 2. Using a configuration file:
 ```python
 from braincube_connector import client

 client.get_instance("config_file"="myfile.json")
 ```
 *myfile.json*
 ```json
 {"api_key":"<my_personal_access_token>", "domain":"mybraincube.com"}
 ```

### Authentication with an Oauth2 token.

The *braincube_connector* used to support only this type of authentication. This is not the method we encourage
the most since the PAT is available, because the Oauth2 is obtained with the [braincube-token-getter](https://pypi.org/project/braincube-token-getter/) that is not under active development.
However if you still want to use this method, you need to setup the configuration file (or dictionary) as follows:
`config.json`

```json
{
    "client_id": "app id",
    "client_secret": "app key",
    "domain": "mybraincube.com",
    "verify": true,
    "oauth2_token": "token value"
}
```

By default the connector searches for a PAT and uses the oauth2_token when the PAT is not present in the dictionary.

### Configuration parameters

Here is a list of the settings available in the configuration file:

- `domain`(optional if `sso_base_url` and `braincube_base_url` exist): The domain of the braincube to access.
- `sso_base_url`(optional if `domain` exists): The base URL of the SSO used to check the validity of your access token.
- `braincube_base_url`(optional if `domain` exists): The base URL of the Braincube API used to fetch data from.
- `api_key`(optional if `oauth2_token` exists): a personal access token generated in the braincube account configuration.
- `oauth2_token`(optional if `api_key` exists): an OAuth2 token obtained with the [braincube-token-getter](https://pypi.org/project/braincube-token-getter/). Used only when `api_key` does not exist.
- `verify`(optional, default is `True`): If `False`, the requests do not verify the SSL certificate.
> Setting `verify` to false must be used with care, it's a security threat (see [requests documentation](https://requests.readthedocs.io/en/latest/api/#requests.Session.verify)

The `client_id`,  `client_secret` from the last section are used only by the *braincube_token_getter* when requesting a new OAuth token.

### Note:
If the client is not initialized manually or if no configuration is passed to `get_instance`, the package creates a client instance from one of these two files `./config.json`  or `~/.braincube/config.json` (in this priority order) when they exist.



## Usage

### Client

A client can be inialized manually from a custom configuration file.

```python
from braincube_connector import client

client.get_instance(config_file="pathto/config.json")
```

**Note:** If the client is not initialized manually, the package creates a client instance from one of these two files `./config.json`  or `~/.braincube/config.json` (in this priority order) if they exist.

### Features of the connector entities.

The connector gives access to different entities(described in more details in the following sections) that share multiple methods:

- `<entity>.get_name()`: Returns the name of the entity.
- `<entity>.get_bcid()`: Returns the bcId identifier of the entity.
- `<entity>.get_uuid()`: Returns the braincube unique uuid identifier of the entity.
### Braincube

To obtain a list of all the available `Braincube` entities with a client:
```python
from braincube_connector import braincube

braincube.get_braincube_list()
```

Or to select a specific `Braincube` entity from its name:
```python
bc = braincube.get_braincube("demo")
```

### MemoryBase

The list of all the memory bases available within a `Braincube` is obtained with

```python
mb_list = bc.get_memory_base_list()
```

**Note:** The number of memory bases in a braincube can be numerous,  hence `get_memory_base_list` allows paginated requests `bc.get_memory_base_list(page=0)`

To select a unique memory base, go with its bcId:

```python
mb = bc.get_memory_base(20)
```


### VariableDescriptions

The variable description are linked to a memory base.

```python
var_desc = mb.get_variable(bcid="2000034")
```

For multiple variable descriptions:

```python
mb.get_variable_list(page=0)
```

**Note:** Similarly to memory bases, providing no argument to `get_variable_list` retrieves all the descriptions available in the memory base.

The type of variable is obtained with the function `get_type`

```python
var_desc.get_type()
```

### DataGroup
DataGroup are obtained from a memory base:
```python
datagroup = mb.get_datagroup(bcid="10")
```
The list of the available datagroups can also be obtained with `mb.get_datagroup_list()`.

A datagroup is a container that includes multiple variables. They are accessed with
```python
datagroup.get_variable_ids() # Gets the variable bcIds
datagroup.get_variable_list() # Gets the list of VariableDescription objects.
```

### Event
An event is a predifined set of conditions in braincube. It is accessed as follows:
```python
event = mb.get_event(bcid="10")
event_list = mb.get_event_list()
```

The interest of events is that you can access the conditions they contain in order create new [filters](#data-filters) for a `get_data` function:

```python
event.get_conditions()
```

### JobDescription

The job desciption contains the settings used to build an analysis and gives a proxy to access these parameters easily. A JobDescription is obtained from a memory base as follows:

```python
job_desc = mb.get_job(bcid="573")
job_list = mb.get_job_list(page=0)
```

The properties are acced with the following methods:  

- **get_conditions:**  
  Gets a list of the conditions used to select the job variables.
  ```python
  job_desc.get_conditions()
  job_desc.get_conditions(combine=True) # Merge the conditions into one
  job_desc.get_conditions(include_events=True) # Includes the conditions from
                                               # the job's events
  ```

- **get_variable_ids:**  
  Gets a list of the variables involved in the job, including the target variables and the influence variables.
  ```python
  job_desc.get_variable_ids()
  ```

- **get_events:**  
  Gets a list of the event objects used by the job.
  ```python
  job_desc.get_events()
  ```
- **get_categories:**  
  Gets a list of conditions used to categorise a job's data as *good* or *bad*. You may have a *middle* category, it's an old categorisation which will not be used anymore.
  ```python
  job_desc.get_categories()
  ```

- **get_data:**  
  When a job is created on braincube, a separate copy of the data is made. As for now this copy is not available from the webservices. However the `get_data` method collects the job's data from the memory base using the same filters as when the job was created. Be aware that these data might be different from the job's data if the memory base has been updated since the job creation.  

  Similarly to other object `get_data`, a `filters` parameter is available to add additional [filters](#data-filters) to the job's conditions.

  ```python
  job_desc.get_data()
  ```

### Job rules
The job rule descriptions are obtained with the methods `get_rule` or `get_rule_list` either from a job or a memory base. The only difference being that in the case of a memory base `get_rule_list` gets all the rules existing in the memory base whereas for a job, it gets the rules specific to the job under consideration.

```python
rule = job.get_rule(bcid="200")
rule_list = job.get_rule_list()
```

To access a `RuleDescription` object's metadata, you can calle the `get_metadata` function
```python
rule.get_metadata()
```


### Get variable data

A memory base can also request the data for a custom set of variable ids. Adding [filters](#data-filters) restricts the returned data to a desired subset of the data. The method is called as follows:
```python
data = mb.get_data(["2000001", "2000034"], filters=my_filters, label_type="name", dataframe=True)
```

The output format is a dictionary or a pandas DataFrame when the `dataframe` parameter is set to `True`. The keys/column labels are the variable bcIds or names depending on whether `label_type` is set to `"bcid"` or `"name"` respectively.

**Note:** By default the dates are not parsed to `datetime` objects in order to speed up the `get_data` function but it is possible to enable the parsing:
```python
from braincube_connector import parameters
parameters.set_parameter({"parse_date": True})
```

### Data filters
The `get_data` methods have the option to restrict the data that are collected by using a set of filters. The `filters` parameter must be a list conditions (even for a single condition):
```python
object.get_data(filters=[{"BETWEEN": ["mb20/d2000002",0,10]},{"BETWEEN": ["mb20/d2000003", -1, 1]}])
```

Here is a selection of the most common types of filters:
- **Equals to**  
  Selects data when a variable is equal to
  ```json
  {
    "EQUALS": [ "mb20/d2000002", 2.0]
  }
  ```
- **Between**  
  Selects the data when a variable belongs to a range.
  ```json
  {
    "BETWEEN": [ "mb20/d2000003", -1, 1]
  }
  ```
- **Lower than**  
  Selects the data when a variable is lower than a certain value.
  ```json
  {
    "LESS": [ "mb20/d2000003", 10]
  }
  ```
  **Note:** The `LESS_EQUALS` filter also exists.


- **Greater than**  
  Selects the data when a variable is greater than a certain value.
  ```json
  {
    "GREAT": [ "mb20/d2000003", 10]
  }
  ```
  **Note:** The `GREAT_EQUALS` filter also exists.

- **Not:**  
  The `NOT` condition creates the opposite of an existing condition.
  ```json
  {
    "Not": [{"filter":...}]
  }
  ```

- **And gate**  
  It is possible to combine filters using a *and* gate.
  ```json
  {
    "AND": [{"filter1":...}, {"filter2":...}]
  }
  ```
  **Notes:**  
    - A `AND` filter can only host two conditions. In order to join more than two filters multiple `AND` conditions should be nested one into another.
    - When multiple filters are provided in the `get_data`'s `filters` parameters, they are joined together within the function using `AND` gates.  

- **Or gate:**  
  Similar to `AND` but uses a `OR` gate.
  ```json
  {
    "OR": [{"filter1":...}, {"filter2":...}]
  }
  ```
## Advanced Usage

The *braincube_connector* provides a simple interface for the most common features of the *braincube web-services* or *braindata* but it is not extensive.

If you need to access an endpoint of [*braincube webservices*](https://braincube.io/ws-doc/?urls.primaryName=Braincube%20WS) or [*braindata*](https://braincube.io/ws-doc/?urls.primaryName=Braindata%20WS), the `request_ws` function of the library can help you. The function uses the configuration passed to the client creation to manage the authentication.

```python
from braincube_connector import client

client.get_instance(config_dict={...})
json_result = client.request_ws("braincube/demo/braindata/mb20/simple")
```

Most braincube requests return a json, but for a few of them it might be better to deactivate the parsing by setting the `response_as_json` parameter to `False`. In the latter case, `request_ws` returns the response object.

```python
json_result = client.request_ws("braincube/demo/braindata/mb20/simple", response_as_json=False)
```

## Library parameters
The library parameters can be set to custom values:

```python
from braincube_connector import parameters

# Change the request pagination size to 10
parameters.set_parameter({"page_size": 10})

# Parse dates to datetime objects
parameters.set_parameter({"parse_date": True})

# The Braincube database stores multiple names (`tag`, `standard`, or `local`) for a variable
# By default `standard` id used, but you can change it as follows:
parameters.set_parameter(({"VariableDescription_name_key": "tag"}))
```
