# Data Agency Registry

**THIS PROJECT IS IN EARLY DEVELOPMENT STAGE**

## Overview

This project aims at compiling information around government agencies, data archives, research centers, and other organizations producing and publishing statistical and scientific data. Our objective is to complement existing registries, that tend to focus on agency identification and profile, by capturing additional information about the agencies services and data discovery/access mechanisms offers. 

A key aspect of this project is to ensure this information is available in machine actionable formats, which in turn enables automated data and services discovery,

Note that the term agency is broad and can also include in some cases initiatives or projects (such as open government data)

To browse the registry, please visit [https://integrateddatasvc.github.io/agency-registry/](https://integrateddatasvc.github.io/agency-registry/)


## Where are we?
*Last updated 2021-07-12*

### Progress

This project is in its very initial stage and at this time have:

- Defined rough schemas for the registry files 
- Identified the following agency registries: Crossref, FundRef, GRID, ISNI, OrgRef, ROR, Wikidata
- Recognized Wikidata as the most comprehensive registry
- Captured initial metadata for government agencies in the U.S., national statistical offices around the globe, a few regional and international organizations, and select data.gov sites. Our initial focus has been on identifiers, social networks, and newsfeeds
- Completed an initial scan of [CKAN](https://ckan.org/) based catalog services
- Using [Jekyll](https://jekyllrb.com/), generated an HTML web site top provide basic catalog navigation 

### Roadmap

Our current objectives include:

- Involving the community to help maintain and enhance the registry content
  - Continue to compile information on CKAN powered data catalogs
  - Compile information on Dataverse powered data catalogs around the globe
- Leveraging the registry machine actionable catalog to globally discover existing and new data, and potentially develop unified DCAT compliant APIs
- Leveraging the registry RSS/atom newsfeed information to drive aggregated news services and APIs
- Add Wikidata pages for agencies that do not currently have an entry (and therefore no Wikidata identifier)
- Investigating potential integration with Wikidata (automated contribution and extensions)
- Deploy a Apache Solr server to support rich registry search
- Investigating how to align on various recommendations of the FAIR initiative, in particular [FAIR implementation profiles (FIPS)](https://www.go-fair.org/how-to-go-fair/fair-implementation-profile/), [FAIR Digital Objects (FDOs)](https://fairdo.org/), and [FAIR Data Points](https://www.fairdatapoint.org/).

## How to contribute?

The registry content can be directly maintained by editing the content under the _data directory. You can do this by cloning the project and submitting pull requests using standard GitHub mechanisms. More information on this below.

We understand that not everyone is familiar with Git or YAML and knows how to do this. We welcome your feedback, comments, or suggestions, which you can submit through using the Issues(https://github.com/integrateddatasvc/agency-registry/issues)

## Editing the content

The registry is primarily driven by the content of the ```_data``` directory. 

The first level is used to group agencies by geographical location or coverage. This is mostly using self-explanatory ISO country or geocodes. You will usually not have to create directories at this level.

Each agency or initiative then lives in its own dedicated directory, whose name is composed or dash separated acronyms. It must be unique across the entire registry and is based on the following naming conventions:
- The first component is always the name of the umbrella group
- The following are used to further inform about the nature of the agency:
  - ```city```: City level agency
  - ```edu```: Academic institution
  - ```gov```: National government organization
  - ```nso```: National statistical office or agency
  - ```opendata```: Reserved for country national level open data (data.gov)
- The suffix can then be the agency common acronym or abbreviation
Note that this is not intended as a formal identifier and is subject to change.

An agency directory can contains the following property files, using the [YAML](https://yaml.org/) syntax:
  - ids.yaml: holds a list of know unique identifiers for the agency (from other registries)
  - geo.yaml: describes geographical coverage of the agency
  - services.yaml: web sites, data catalog, data web services, newsfeed
  - social.yaml: social networks account identifiers and information

Schemas for these files can be found in the project ```/schemas``` directory (note that the canonical version is maintained in YAML format). Note that these are under development and subject to changes.

## Generated content

Various Python scripts, located in the ```/utils``` directory, are used to automatically produce the following content on schedule or when a push is committed to the project:

- The agency's ```external``` sub-directoryholding metadata found in other registries or sites. This is driven by the content of the ```ids.yaml``.
- The ```/_registry``` directory used by Jekyll to generate the registry's [web site](https://integrateddatasvc.github.io/agency-registry/). This essentially holds markdown files aggregating content from the agency's metadata.

The GitHub Jekyll integration populates the ```/_site``` directory and is driven by content from the following locations:

- ```_includes```
- ```_layouts```
- ```assets```


## Identifiers and basic information
Several initiatives readily collect and maintain basic information about agencies and assign them unique identifiers. We can leverage these to harvest/aggregate what we need, and add the additional metadata elements that we want to capture.

Below list of sources we have identified and can be used to compile basic agency profile information. Note that only a few provide public API end point, and all seem to lack OpenAPI / Postman docs. Some offer a full database download. 

### [Crossref Funder ID](https://www.crossref.org/services/funder-registry/)
The Funder Registry and associated funding metadata allows everyone to have transparency into research funding and its outcomes. It’s an open and unique registry of persistent identifiers for grant-giving organizations around the world.

The Crossref Funder Registry is an open registry of grant-giving organization names and identifiers, which you use to find funder IDs and include them as part of your metadata deposits. It is a freely-downloadable RDF file. It is CC0-licensed and available to integrate with your own systems. Funder names from acknowledgements should be matched with the corresponding unique funder ID from the Funder Registry.

See also: [API Docs](https://www.crossref.org/education/retrieve-metadata/rest-api/)

### [ISNI: International Standard Name Identifier](https://isni.org/)
ISNI is the ISO certified global standard number for identifying the millions of contributors to creative works and those active in their distribution, including researchers, inventors, writers, artists, visual creators, performers, producers, publishers, aggregators, and more.

See also: [Technical documentation](https://isni.org/page/technical-documentation/) | [Search API Guidelines](https://isni.oclc.org:2443/isni/docs/ISNI%20SRU%20search%20API%20guidelines.pdf)

### [GRID: Global Research Identifier Database](https://www.grid.ac/). 

Global Research Identifier Database (GRID) is an openly accessible database of educational and research organizations worldwide, created and maintained by Digital Science & Research Solutions Ltd., part of the technology company Digital Science.

Each organization is assigned a unique GRID ID and there is a corresponding web address and page for each ID in the database. The dataset contains the institution's type, geo-coordinates, official website, and Wikipedia page. Name variations of institutions are included, as well.

*GRID data is available through the [Dimensions API](https://www.dimensions.ai/dimensions-apis/), which only is sadly freely for personal, non-commercial use*

See also: [GRID Formats](https://www.grid.ac/format) | [Download options](https://www.grid.ac/downloads)

### [ROR: Research Organization Registry](https://ror.org)
ROR is a community-led project to develop an open, sustainable, usable, and unique identifier for every research organization in the world.

API end point is at https://api.ror.org. List of arganizations at http://api.ror.org/organizations

See also: [ROR documentation](https://github.com/ror-community) | [ROR API](https://github.com/ror-community/ror-api)

### [Wikidata](https://www.wikidata.org/)
Wikidata is a free and open knowledge base that can be read and edited by both humans and machines.

### [Wikipedia](http://wikipedia.org/)
The free encyclopedia...


### Examples

| Registry  | U.S. Census Bureau | Statisitcs Canada | EUROSTAT | 
|----------:|:------------------:|:-----------------:|:--------:|
| crossref  |[100006958](https://api.crossref.org/funders/100006958)|-|[501100000804](https://api.crossref.org/funders/501100000804)|
| facebook  |[uscensusbureau](https://www.facebook.com/uscensusbureau)|[statistiquecanada](https://www.facebook.com/statistiquecanada)|[EurostatStatistics](https://www.facebook.com/EurostatStatistics)|
| GRID      |[grid.432923.d](https://www.grid.ac/institutes/grid.413850.b)|[grid.413850.b](https://www.grid.ac/institutes/grid.432923.d)|[grid.467724.4](https://www.grid.ac/institutes/grid.467724.4)|
| ISNI      |[0000000113307149](http://isni.org/isni/0000000113307149)|[0000000120975698](http://isni.org/isni/0000000120975698)|[0000000000459042213](http://isni.org/isni/0000000000459042213)|
| LinkedIn  |[us-census-bureau](https://www.linkedin.com/company/us-census-bureau)|[statcan](https://www.linkedin.com/company/statcan)|[eurostat](https://www.linkedin.com/company/eurostat)|
| ROR       |[01qn7cs15]((https://ror.org/05k71ja87)) ([api](http://api.ror.org/organizations/https://ror.org/01qn7cs15))|[05k71ja87](https://ror.org/05k71ja87) ([api](http://api.ror.org/organizations/https://ror.org/05k71ja87))|[033d3q980](https://ror.org/033d3q980) ([api](http://api.ror.org/organizations/https://ror.org/033d3q980))|
| Twitter  |[uscensusbureau](https://twitter.com/uscensusbureau)|[StatCan_eng](https://twitter.com/StatCan_eng) / [StatCan_fra](https://twitter.com/StatCan_fra)|[EU_Eurostat](https://twitter.com/EU_Eurostat)|
| Wikidata  |[Q637413](https://www.wikidata.org/wiki/Q637413)|[Q1155740](https://www.wikidata.org/wiki/Q1155740) / [json](https://www.wikidata.org/wiki/Special:EntityData/Q1155740.json)|[Q217659](https://www.wikidata.org/wiki/Q217659)|
| Wikipedia |[United\_States_Census](https://en.wikipedia.org/wiki/United_States_Census)|[Statistics_Canada](https://en.wikipedia.org/wiki/Statistics_Canada)|[Eurostat](https://en.wikipedia.org/wiki/Eurostat)|


## Sponsors

This project is supported by [Integrated Data Management Services](http://www.integrateddatasvc.ca), [Metadata Technology North America](https://www.mtna.us), [API Evangelist](https://apievangelist.com), and [Postman](https://postman.com).
