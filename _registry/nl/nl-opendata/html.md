---
name: nl-opendata
external:
  wikidata:
    entities:
      Q97013475:
        aliases:
          en:
          - language: en
            value: data.overheid.nl
        claims:
          P17:
          - id: Q97013475$8B6A452C-81E8-4447-9CB5-DEF044B77379
            mainsnak:
              datatype: wikibase-item
              datavalue:
                type: wikibase-entityid
                value:
                  entity-type: item
                  id: Q55
                  numeric-id: 55
              property: P17
              snaktype: value
            rank: normal
            type: statement
          P31:
          - id: Q97013475$3AF196E8-E1C6-463B-B092-2E0B359FCA09
            mainsnak:
              datatype: wikibase-item
              datavalue:
                type: wikibase-entityid
                value:
                  entity-type: item
                  id: Q27031827
                  numeric-id: 27031827
              property: P31
              snaktype: value
            rank: normal
            references:
            - hash: 4c374fb0af83332c22a85d2d01acb312ecde0ff2
              snaks:
                P248:
                - datatype: wikibase-item
                  datavalue:
                    type: wikibase-entityid
                    value:
                      entity-type: item
                      id: Q5227102
                      numeric-id: 5227102
                  property: P248
                  snaktype: value
                P813:
                - datatype: time
                  datavalue:
                    type: time
                    value:
                      after: 0
                      before: 0
                      calendarmodel: http://www.wikidata.org/entity/Q1985727
                      precision: 11
                      time: +2020-10-29T00:00:00Z
                      timezone: 0
                  property: P813
                  snaktype: value
                P854:
                - datatype: url
                  datavalue:
                    type: string
                    value: https://www.data.gov/open-gov/
                  property: P854
                  snaktype: value
              snaks-order:
              - P813
              - P248
              - P854
            type: statement
          P407:
          - id: Q97013475$4858EB77-27E2-4331-9A7D-E229666004C6
            mainsnak:
              datatype: wikibase-item
              datavalue:
                type: wikibase-entityid
                value:
                  entity-type: item
                  id: Q1860
                  numeric-id: 1860
              property: P407
              snaktype: value
            rank: normal
            type: statement
        descriptions: {}
        id: Q97013475
        labels:
          en:
            language: en
            value: Open Data Portal Netherlands
          ta:
            language: ta
            value: "\u0BB0\u0BCA\u0BB1\u0BA9\u0BCD\u0BB0\u0BCB \u0BA4\u0BBF\u0BB1\u0BA8\
              \u0BCD\u0BA4 \u0BA4\u0BB0\u0BB5\u0BC1"
        lastrevid: 1299456730
        modified: '2020-10-29T16:29:07Z'
        ns: 0
        pageid: 95515541
        sitelinks: {}
        title: Q97013475
        type: item
ids:
  wikidata: Q97013475
services:
  catalogs:
  - api_endpoint: https://data.overheid.nl/data/api/3/
    client: html
    endpoint: https://data.overheid.nl/
    lang: nl, en
    name: Open Data of the Government
    platform: ckan
  - client: html
    endpoint: https://data.overheid.nl/
    lang: nl
    name: Dataplatform
    platform: ckan
---
