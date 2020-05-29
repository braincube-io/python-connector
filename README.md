# braincube_connector: a python client for Braincube

## Description

The python package `braincube_connector` provides a tool for datascientists to access their data on Braincube directly from python.

## Installation

Install with pip:

```bash
pip install braincube_connector
```

## Usage

### Client

A client can be inialized manually from a custom configuration file.

```python
from braincube_connector import client

client.get_instance(config_file="pathto/config.json")
```

**Note:** If the client is not initialized manually, the package creates a client instance from one of these two files `./config.json`  or `~/.braincube/config.json` (in this priority order) if they exist.


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
mb_list = bc.get_memory_base(20)
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
data = mb.get_data(["2000001", "2000034"], filters=my_filters)
```

The output format is a dictionary in which the keys are the variable bcIds and the value a list of data. This allows an easy conversion to a pandas dataframe:

```python
import pandas as pd

df = pd.DataFrame(data)
```

**Note:** By default the dates are not parsed to `datetime` objects in order to speed up the `get_data` function but it is possible to enable the parsing:
```python
from braincube_connector import parameters
parameters.set_parameter({"parse_date": True})
```

### Data filters
The `get_data` methods have the option to restrict the data that are collected by using a set of filters. The `filters` parameter must be a list conditions (even for a single condition):
```python
object.get_data(filters=[{"BETWEEN",["mb20/d2000002",0,10]},{"BETWEEN",["mb20/d2000003", -1, 1]}])
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
    - When multiple filters are provided in the `get_data`'s `filters` parmeters, they are joined together within the function using `AND` gates.  

- **Or gate:**  
  Similar to `AND` but uses a `OR` gate.
  ```json
  {
    "OR": [{"filter1":...}, {"filter2":...}]
  }
  ```

## Library parameters
The library parameters can be set to custom values:

```python
from braincube_connector import parameters

# Change the request pagination size to 10
parameters.set_parameter({"page_size": 10})

# Parse dates to datetime objects
parameters.set_parameter({"parse_date": True})
```


## Configuration

In order to connect to the web service, the client needs a Oauth2 token saved in a configuration file. For simplicity it is recommended to use a helper [braincube-token-getter](https://pypi.org/project/braincube-token-getter/) to get the token and to setup the configuration file as follows:

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
The `token-getter` script saves the configuration in the `~/.braincube/config.json` file by default.
