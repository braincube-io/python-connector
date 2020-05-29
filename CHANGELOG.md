# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2019-05-28
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
