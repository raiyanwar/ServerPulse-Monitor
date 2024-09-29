# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Alert mechanism for sending notifications on failed connection attempts (future implementation).

## [1.0.0] 
### Added
- **Server Monitoring**: Monitors server availability by checking connections on specified ports.
- **Connection Types**: Support for both plain TCP and SSL connections.
- **Ping Feature**: Fallback mechanism to check if the server is reachable via ping.
- **History Logging**: Keeps track of connection attempts and their results with timestamps.
- **Error Handling**: Graceful handling of various socket exceptions and logging of relevant messages.
- **Persistent Server List**: Ability to load and save a list of servers from a `servers.pickle` file.

### Changed
- N/A

### Fixed
- N/A

### Removed
- N/A
