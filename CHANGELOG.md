# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased][unreleased]
### Changed
- Updated dependencies (fixed [CVE-2017-18342](https://nvd.nist.gov/vuln/detail/CVE-2017-18342))


## [0.2.2] - 2018-07-06
### Changed
- Updated dependencies

### Fixed
- Fixed version of PyYAML (reverted to 3.x)


## [0.2.1] - 2018-06-27
### Changed
- Small deployment & testing related changes
- Updated dependencies


## [0.2.0] - 2016-03-28
### Added
- Added [include](https://github.com/andras-tim/octoconf/blob/v0.2.0/docs/features.rst#includes) feature

### Changed
- Replaced `octoconf.read(<filename>)` function with `octoconf.load(<stream>)` and `octoconf.loads(<string>)` for
    better fit to the standards.
- Improved code quality (added some error handlers and tests was rewritten, Pylint ready code)


## 0.1.0 - 2016-03-23
### Added
- ``octoconf`` lib with unit tests
- example YAML file


[unreleased]: https://github.com/andras-tim/octoconf/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/andras-tim/octoconf/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/andras-tim/octoconf/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/andras-tim/octoconf/compare/v0.1.0...v0.2.0
