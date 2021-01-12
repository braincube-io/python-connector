# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0 - 2020-12-01](https://gitlab.ipleanware.com/braincube/core/python/py_client/compare/2.2.1...2.2.2)

### Added
- Make `get_name` and `get_bcid` methods available for all BaseEntity objects.
- provide a selection system for the type of name to use for the objects.
- Add parameter in MemoryBase get_data() function to change the label_type ("name" or "bcid") 
- Add parameter in MemoryBase get_data() function to return a pandas DataFrame

### Fixed
 - Fix the parsing of date list containing "null" elements (https://gitlab.ipleanware.com/braincube/misc/redmine/-/issues/2597)

### Changed
 - Improve list of date parsing using pandas

## [2.2.1 - 2020-11-09](https://gitlab.ipleanware.com/braincube/core/python/py_client/compare/2.2.0...2.2.1)

### Fixed
 - Fix typo in documentation (https://gitlab.ipleanware.com/braincube/misc/redmine/-/issues/2547)

## [2.2.0 - 2020-10-27](https://gitlab.ipleanware.com/braincube/core/python/py_client/compare/2.1.0...2.2.0)

### Added
 - Add the personal access token option for authentication.
 - Allow requests without json parsing in `request_ws`.
### Fixed
 - Fix the setting of the `verify` parameter for the SSL certificate setting.

## [2.1.0 - 2020-07-08](https://gitlab.ipleanware.com/braincube/core/python/py_client/compare/2.0.2...2.1.0)

### Fixed
 - possibility to use other memory base references than dates.

### Added
 - a get_order_variable_long_id method to memory_bases, get_braindata_memory_base_info to the data library

### Modified
 - the data's function collect_data now takes a memory_base instead of its metadata as a parameter.

## [2.0.2 - 2020-06-11](https://gitlab.ipleanware.com/braincube/core/python/py_client/compare/2.0.1...2.0.2)

### FIXED
 - Fixes the [requests library](https://gitlab.ipleanware.com/braincube/misc/redmine/issues/1791) not present error by adding it to the no-dev dependencies.

## [2.0.1 - 2020-06-03](https://gitlab.ipleanware.com/braincube/core/python/py_client/compare/2.0.0...2.0.1)

### FIXED
 - Convert all object bcid to str in `_get_resource`. Prevents error when bcids are passed as int

## [2.0.0] - 2020-05-28
The version 2.0.0 redefines the connector API by unifying the function naming.

### Added
- client to the braincube WS API
- Add Braincube, MemoryBase, VariableDescription, JobDescription, Event, DataGroups, RuleDescription objects
- Add methods to get a VariableDescription, JobDescription, Event, DataGroups, or RuleDescription object from a memory_base
- Add get_data functions to fetch the data from a memory_base
- Generate request filters from event and job conditions
- Add job methods to get events, conditions, variables, categories, data, and rules

### Removed
 - The token getter utility. It now relies on the braincube-token-getter package.
