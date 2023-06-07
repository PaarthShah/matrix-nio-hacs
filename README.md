# Matrix Nio - HACS

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
![Downloads][downloads]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Community Forum][forum-shield]][forum]
[![Matrix][matrix-chat]][matrix-chat-link]

_Integration to integrate with Matrix Homeservers using [matrix-nio](https://github.com/poljar/matrix-nio). Replaces the core HomeAssistant `matrix` integration._

[PR to merge to core](https://github.com/home-assistant/core/pull/72797)

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `matrix`.
1. Download _all_ the files from the `custom_components/matrix/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Matrix Nio"

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[matrix-nio-hacs]: https://github.com/PaarthShah/matrix-nio-hacs
[commits-shield]: https://img.shields.io/github/commit-activity/y/PaarthShah/matrix-nio-hacs.svg?style=for-the-badge
[commits]: https://github.com/PaarthShah/matrix-nio-hacs/commits/main
[hacs]: https://github.com/hacs/integration
[downloads]: https://img.shields.io/github/downloads/PaarthShah/matrix-nio-hacs/total?style=for-the-badge
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/PaarthShah/matrix-nio-hacs.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Paarth%20Shah%20%40PaarthShah-blue.svg?style=for-the-badge
[matrix-chat]: https://img.shields.io/matrix/matrix-nio-hacs:shahpaarth.com?label=Matrix%20Chatroom&server_fqdn=matrix.shahpaarth.com&style=for-the-badge
[matrix-chat-link]: https://matrix.to/#/#matrix-nio-hacs:shahpaarth.com
[releases-shield]: https://img.shields.io/github/release/PaarthShah/matrix-nio-hacs.svg?style=for-the-badge
[releases]: https://github.com/PaarthShah/matrix-nio-hacs/releases