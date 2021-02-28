# Agency Registry

**THIS PROJECT IS IN EARLY STAGE**

This project aims at compiling information around government agencies, data archives, research centers, and other organizations producing and publishing statistical and scientific data, with a focus on documenting coverage and data access mechanisms. 

This includes:
- Organization profile: web site, location, contact information
- Geospatial coverage: what is the geographical level the organization (global, regional, national, subnational, city) and its area of operation
- Sector: social, health, education, hard sciences
- Role: producer, archive, research, funding, other
- Nature: government (national/local), acadmic, non-profit, commercial, international org, joint projects,  consortium, foundation
- Data access policies / modalities
- Availability of data catalogs and APIS

The term egancy is broad and can also include in some cases initiatives or projects (such as open government data)

## How this works?
- Each agency has a dedicated directory that contains files storing various pieces of information (metadata) about it.
- A metadata file has a well defined structure and content (schema) and is typically stored in a YAML, JSON, or XML.
- The files follow specific naming conventions to indentify its origin and schema (content)

The following files are maintained in this project:
- ids.yaml: list of know unique identifiers for the agency
- geo.yaml: level and geographical coverage of the agency
- services.yaml: web sites, data catalog, data web services, newsfeed
- social.yaml: social networkk account identifiers and info

JSON schemas for these files can be found in the project /schemas directory. **Note that the canonical version is maintained in YAML format**.

The ids.yaml file is used by scripts to automatically harvest and updated metadata from external sources.

The following files are harvested and stored in the ```<agency>/external``` directory:
- ror.json
- isni.xml

The following files are generated from the available metadata and stored in the docs directory:

- (todo)

### How to add an agency
- Create a directory in the relevant catalog under the registry
- Create an ids.yaml file, with at least its ROR identifier
- Run the updater script in the utils directory: `python updater.py <group>/<agency>`
  - This will further populate the ids and add metadata files from other registries
- (to be continued)

### naming conventions

#### catalogs
- agencies are organized in catalog (the first level of the registry)
- 2-letter catalog name are reserverd for ISO 3166 countty codes
- ```int``` is reserved for supra national organizations (global, regional)

#### agencies
- The agency directory name is an unique value withing the entire registry
- Note that this is not a formal identifier and is subject to change
- Its first component is always the name of the umbrella catalog
- the following are used to further inform about the nature of the agency
  - ```city```: City level agency
  - ```gov```: National government organization
  - ```opendata```: Reserved for country national level open data (data.gov)
  - ```nso```: National statistical office or agency

## Identifers and basic information
Several initiaives readilly collect and maintain basic information about agencies and assign them unique identifiers. We can leverage these to harvest/aggregate what we need, and add the additional metadata elements that we want to capture.

Below list of sources we have identified and can be used to compile basic agency profile information. Note that only a few provide public API end point, and all seem to lack OpenAPI / Postman docs. Some offer a full database download. ROR seem like a good starting point for identifiers. 

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

## Geo Coverage
The geo.yaml file captures information about the geographic area the agency operates in. 

The ```level``` can be one of the following values: ```global | regional | national | subnational | city  | other

The following properties hold codes for their corresponding standards. This can be a single string value, or an arrya of strings if more than one applies.

- iso3166: ISO 3166 code(s). Note that this covers different classifications and parsers will need to determine the nature of the coed base on the format. For country, the alpha-2 is preferred.
- geonames: Geonames codes
- fips


## Services
The services.yaml file documents web based services provided by the agency. 

The ```name``` and ```description``` provide an overview of the service

The ```type``` property informs on the nature of the service. Values can be:
- catalog
- calendar: data releases and publications
- blog
- news
- data: data access and querying services
- www: a web site or home page

The ```protocol``` property indicates how the service can be accessed or consumed. Values can be:
- html (a web site intended for end-users)
- atom
- rest
- soap
- proprietary

The ```endpoint``` property hold the service URL

The ```lang``` property reflects the service language 9when relevant). This must be a valid ISO 639-1 code.

The ```platform``` property informs on the software powering the service. It can be one one of the following value
- for catalog: ```dataverse```, ```ckan```, ```ihsn-nada```
- for data: ```data.world```, ```mtna-rds```, ```socrata```, ```statista```
- generic: ```proprietary```, ```other```


## Social
The social.yaml file documents social network sites the agency is leveraging.
Valid tope level keys are: facebook, linkedin, twitter, pinterest, youtube

Each network is a dictionary with the key representing the identifier. 
The value is a dictionnary with the following properties
- lang: the ISO 631-1 language code


## Sponsors

This project is supported by [Integrated Data Management Services](http://www.integrateddatasvc.ca), [Metadata Technology North America](https://www.mtna.us), [API Evangelist](https://apievangelist.com), and [Postman](https://postman.com).
