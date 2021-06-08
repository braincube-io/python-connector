# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- #[25](https://github.com/braincube-io/python-connector/issues/25): support `{braincube-name}` as a placeholder in `braincube_base_url` configuration.

## [2.4.1 - 2021-04-22](https://github.com/braincube-io/python-connector/compare/2.4.0...2.4.1)

### Fixed

- Fix URL construction when there is a path in one of the configured base URLs

## [2.4.0 - 2021-04-21](https://github.com/braincube-io/python-connector/compare/2.3.0...2.4.0)

### Added

- update configuration, we can use `sso_base_url` and `braincube_base_url` to define different domains for those services

### Changed

- Move project to GitHub

## [2.3.0 - 2021-02-23](https://github.com/braincube-io/python-connector/compare/2.2.2...2.3.0)

### Added
- Make `get_name` and `get_bcid` methods available for all BaseEntity objects
- Provide a selection system for the name type to use for the objects
- Add parameter in MemoryBase get_data() function to change the label_type ("name" or "bcid")
- Add parameter in MemoryBase get_data() function to return a pandas DataFrame
- Entities have a get_uuid method

## [2.2.2 - 2020-12-01](https://github.com/braincube-io/python-connector/compare/2.2.1...2.2.2)

### Fixed
 - Fix the parsing of date list containing "null" elements

### Changed
 - Improve list of date parsing using pandas

## [2.2.1 - 2020-11-09](https://github.com/braincube-io/python-connector/compare/2.2.0...2.2.1)

### Fixed
 - Fix typo in documentation

## [2.2.0 - 2020-10-27](https://github.com/braincube-io/python-connector/compare/2.1.0...2.2.0)

### Added
 - Add the personal access token option for authentication.
 - Allow requests without json parsing in `request_ws`.
### Fixed
 - Fix the setting of the `verify` parameter for the SSL certificate setting.

## [2.1.0 - 2020-07-08](https://github.com/braincube-io/python-connector/compare/2.0.2...2.1.0)

### Fixed
 - possibility to use other memory base references than dates.

### Added
 - a get_order_variable_long_id method to memory_bases, get_braindata_memory_base_info to the data library

### Modified
 - the data's function collect_data now takes a memory_base instead of its metadata as a parameter.

## [2.0.2 - 2020-06-11](https://github.com/braincube-io/python-connector/compare/2.0.1...2.0.2)

### FIXED
 - Fixes the "requests library not present" error by adding it to the no-dev dependencies.

## [2.0.1 - 2020-06-03](https://github.com/braincube-io/python-connector/compare/2.0.0...2.0.1)

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
