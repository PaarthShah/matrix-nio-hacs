# Matrix Nio - HACS

> [!CAUTION]
> This project is NO LONGER MAINTAINED... because it's been included directly into Home Assistant core! See [this PR](https://github.com/home-assistant/core/pull/72797) and [this commit](https://github.com/home-assistant/core/commit/4d3b978398818f4fe7a2094cb54f83c20a57ef18)


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

### HACS (Preferred)

1. [Add](http://homeassistant.local:8123/hacs/integrations) the custom integration repository: https://github.com/PaarthShah/matrix-nio-hacs
2. Select `Matrix Nio` in the Integration tab and click `download`
3. Restart Home Assistant
4. Done!

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `matrix`.
4. Download _all_ the files from the `custom_components/matrix/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Done!

## Usage
For `v1.0.X`, all documentation available for the [default matrix integrations](https://www.home-assistant.io/integrations/matrix/) is fully-applicable and should work as-stated with 0 changes.

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
