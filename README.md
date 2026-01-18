# Irrigation Gate Control

<!-- ![Doover Logo](https://doover.com/wp-content/uploads/Doover-Logo-Landscape-Navy-padded-small.png) -->
<img src="https://doover.com/wp-content/uploads/Doover-Logo-Landscape-Navy-padded-small.png" alt="App Icon" style="max-width: 300px;">

**Control irrigation gates via hydraulic remotes with configurable open/close timeouts.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/getdoover/irrigation-gate-control)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/getdoover/irrigation-gate-control/blob/main/LICENSE)

[Configuration](#configuration) | [Developer](https://github.com/getdoover/irrigation-gate-control/blob/main/DEVELOPMENT.md) | [Need Help?](#need-help)

<br/>

## Overview

Control irrigation gates via hydraulic remotes with configurable open/close timeouts.

<br/>

## Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| **Hydraulic Controller** | Application that controls hydraulics | `None` |
| **Controlled Remote** | Name of the remote controlling the gate | `None` |
| **Open Direction** | Direction that opens the gate | `Forward` |
| **Open Timeout** | Seconds to run to open | `5` |
| **Close Timeout** | Seconds to run to close | `5` |

<br/>
## Integrations

### Tags

This app exposes the following tags for integration with other apps:

| Tag | Description |
|-----|-------------|
| `request_{remote_key}` | Request sent to hydraulics controller |

<br/>
This is a standalone app with no dependencies on other Doover apps.

<br/>

## Need Help?

- Email: support@doover.com
- [Community Forum](https://doover.com/community)
- [Full Documentation](https://docs.doover.com)
- [Developer Documentation](https://github.com/getdoover/irrigation-gate-control/blob/main/DEVELOPMENT.md)

<br/>

## Version History

### v1.0.0 (Current)
- Initial release

<br/>

## License

This app is licensed under the [Apache License 2.0](https://github.com/getdoover/irrigation-gate-control/blob/main/LICENSE).
