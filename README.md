# Awesome-Urban-Mobility-Management
## Top Urban Mobility Management Tools Ecosystem
**Curated List of SaaS Products & Open-Source GitHub Projects**
*Focused on Transit Planning, Real-Time Operations, MaaS, Microtransit, Curb Management & Mobility Analytics*
**Last updated: July 2026**

This repository tracks notable **SaaS platforms** and **open-source projects** for **Urban Mobility Management**. These tools help cities, transit agencies, and operators plan routes, optimize schedules, deliver real-time information, manage on-demand and shared mobility, analyze travel patterns, and build Mobility-as-a-Service (MaaS) experiences using GTFS, real-time vehicle data, location analytics, and open standards.

**Examples** include Via, Optibus, Swiftly, TransitScreen, Populus, Moovit MaaS, Citymapper for Business, Padam Mobility, Remix, and StreetLight Data (the category leaders).

**Open-source emphasis**: This section is heavily expanded with every major active project for self-hosting, GTFS/GTFS-RT processing, multimodal trip planning, real-time predictions, and open mobility data platforms — ideal for transit agencies, cities, researchers, and developers building transparent, interoperable urban mobility solutions.

Contributions welcome! Open a PR to add/update entries. Keep descriptions factual and link to official sites.

## Table of Contents
- [SaaS/Hosted Platforms](#saashosted-platforms)
- [Open-Source GitHub Projects](#open-source-github-projects)
- [How to Contribute](#how-to-contribute)
- [Disclaimer](#disclaimer)

## SaaS/Hosted Platforms

### Core Platforms (Urban Mobility Management)
- **[Via](https://ridewithvia.com/)**  
  End-to-end public transit software and operations platform for microtransit, paratransit, planning (Remix), and MaaS (Citymapper). Powers dynamic on-demand networks for cities and agencies worldwide.

- **[Optibus](https://optibus.com/)**  
  AI-powered end-to-end platform for transit planning, scheduling, rostering, and operations optimization used by agencies and operators globally.

- **[Swiftly](https://www.swiftly.com/)**  
  Real-time transit performance analytics and passenger information platform delivering high-accuracy insights, tracking, and operational intelligence for agencies.

- **[TransitScreen](https://transitscreen.com/)**  
  Custom real-time multimodal displays and digital signage aggregating transit, micromobility, and shared mobility options for public spaces, campuses, and buildings.

- **[Populus](https://www.populus.ai/)**  
  City-facing platform for managing shared mobility fleets, curbs, streets, and policy — aggregating operator data, enforcing regulations, and providing analytics.

- **[Moovit MaaS](https://moovit.com/maas-solutions)**  
  White-label Mobility-as-a-Service solutions including branded apps, multimodal trip planning, payments, urban mobility analytics, and on-demand transit (owned by Mobileye/Intel).

- **[Citymapper for Business](https://citymapper.com/)**  
  Enterprise and city MaaS offering built on the popular multimodal navigation app (now part of Via), providing trip planning, insights, and network recommendations.

- **[Padam Mobility](https://www.padam-mobility.com/)**  
  Demand-responsive transit (DRT) and on-demand mobility platform for dynamic routing, booking, and operations (Siemens ecosystem).

- **[Remix](https://www.remix.com/)** (by Via)  
  Collaborative web-based transit planning and scenario analysis tool for designing routes, evaluating equity and accessibility impacts, and visualizing networks.

- **[StreetLight Data](https://www.streetlightdata.com/)**  
  Big-data mobility analytics platform turning anonymous location data into origin-destination, volume, speed, and travel pattern insights for planners and engineers.

## Open-Source GitHub Projects

- **[OpenTripPlanner](https://github.com/opentripplanner/OpenTripPlanner)**  
  Leading open-source multimodal trip planner combining GTFS, OpenStreetMap, bike-share (GBFS), and ride-hailing. Powers agency and city journey planners worldwide with GraphQL APIs and real-time support.

- **[OneBusAway](https://github.com/OneBusAway)**  
  Complete open-source suite for real-time transit information: server modules, REST APIs, GTFS-RT export, web interfaces, and official iOS/Android apps. Managed by the Open Transit Software Foundation.

- **[TheTransitClock](https://github.com/TheTransitClock/transitime)**  
  Open-source real-time arrival prediction system (formerly Transitime). Ingests vehicle positions, applies adaptive Kalman-filter algorithms, and outputs GTFS-Realtime trip updates.

- **[Transitland](https://github.com/transitland)** / **[Transitland Atlas](https://github.com/transitland/transitland-atlas)**  
  Community-edited global directory of GTFS, GTFS-RT, GBFS, and MDS feeds plus libraries (`transitland-lib`) for fetching, validating, transforming, and serving open transit data.

- **[MobilityData / Mobility Database](https://github.com/MobilityData)**  
  Canonical GTFS & GBFS validators, Mobility Database catalog of thousands of feeds, GTFS.org, and the widely used awesome-transit curated list of tools and datasets.

- **[MATSim](https://github.com/matsim-org/matsim-libs)**  
  Large-scale agent-based transport simulation framework supporting private vehicles, public transit, demand-responsive transport, and MaaS scenarios. Extensible Java platform used for research and planning.

- **[Navitia](https://github.com/CanalTP/navitia)**  
  Open-source multimodal journey-planning engine powering Navitia.io; supports GTFS and rich transit data models with APIs for schedules, isochrones, and routing.

### Additional Strong Open-Source Options
- **GTFS tooling & validation**: MobilityData/gtfs-validator, gtfs-utils, Google transitfeed, osm2gtfs, Prism (OSM → GTFS), static-GTFS-manager.
- **Real-time & predictions**: TheTransitClock (above), OneBusAway modules, various GTFS-RT converters and visualizers.
- **Multimodal & MaaS building blocks**: OpenTripPlanner clients (OTPKit for iOS, Android apps), Locomotion (open rider app), Netmobiel platform, OpenRide.
- **Shared mobility standards**: Open Mobility Foundation Mobility Data Specification (MDS), GBFS tools, SharedStreets.
- **Simulation & analytics**: MATSim-MaaS examples, SUMO traffic simulation, gtfspy / NxTransit network analysis libraries, Mobility Python package.
- **Data catalogs & pipelines**: Transitland Atlas, Mobility Database catalogs, Interline transitland-lib, many community GTFS archives and converters.

**Frameworks for building custom systems**: Combine **OpenTripPlanner** + **OneBusAway** / **TheTransitClock** + **Transitland** / **Mobility Database** + **GTFS validators** with **InfluxDB/Grafana** or **PostgreSQL/PostGIS** (and optionally **MobilityDB**) for self-hosted real-time information, trip planning, and mobility analytics platforms. Add **MATSim** for scenario simulation and **MDS/GBFS** tools for shared-mobility regulation.

## How to Contribute
1. Fork the repo.
2. Add/edit entries in `README.md` (follow existing format).
3. Include: name, link, 1–2 sentence description, and whether it's SaaS or open-source.
4. Submit PR with a short explanation.

Star the repo if you find it useful!

## Disclaimer
- This is a **community-curated** list — not exhaustive and not an endorsement.
- Urban mobility and transit tools must comply with local regulations, data privacy laws (GDPR, CCPA, etc.), and accessibility requirements.
- Self-hosted open-source solutions require proper security, reliability, and operational support for production use by public agencies.

---
**Made for cities, transit agencies, mobility operators, urban planners, and open-source developers.**  
Let's make urban mobility management more open, data-driven, and interoperable.

