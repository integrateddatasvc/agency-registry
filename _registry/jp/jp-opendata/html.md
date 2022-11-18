---
name: jp-opendata
external:
  wikidata:
    aliases:
      ja:
      - language: ja
        value: data.go.jp
    claims:
      P17:
      - id: Q97153912$2A3F9096-2F84-48BE-B783-7F6E5F624972
        mainsnak:
          datatype: wikibase-item
          datavalue:
            type: wikibase-entityid
            value:
              entity-type: item
              id: Q17
              numeric-id: 17
          property: P17
          snaktype: value
        rank: normal
        type: statement
      P31:
      - id: Q97153912$8D299559-7E4C-4CF7-A839-6D26F3514B94
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
      - id: Q97153912$18F90AD5-A289-4584-AC96-9A19454AD21A
        mainsnak:
          datatype: wikibase-item
          datavalue:
            type: wikibase-entityid
            value:
              entity-type: item
              id: Q5287
              numeric-id: 5287
          property: P407
          snaktype: value
        rank: normal
        type: statement
      P856:
      - id: Q97153912$445C27E3-DB9B-423F-A60F-5155C5ACA14C
        mainsnak:
          datatype: url
          datavalue:
            type: string
            value: https://www.data.go.jp/
          property: P856
          snaktype: value
        qualifiers:
          P407:
          - datatype: wikibase-item
            datavalue:
              type: wikibase-entityid
              value:
                entity-type: item
                id: Q5287
                numeric-id: 5287
            hash: d858d1b9f6e6e383f38dfbe706d102f056c07312
            property: P407
            snaktype: value
        qualifiers-order:
        - P407
        rank: normal
        type: statement
    descriptions:
      en:
        language: en
        value: Japan open data portal
      ja:
        language: ja
        value: "\u65E5\u672C\u653F\u5E9C\u306E\u30AA\u30FC\u30D7\u30F3\u30C7\u30FC\
          \u30BF\u30FB\u30DD\u30FC\u30BF\u30EB"
    id: Q97153912
    labels:
      ca:
        language: ca
        value: data.go.jp
      en:
        language: en
        value: data.go.jp
      ja:
        language: ja
        value: "\u30C7\u30FC\u30BF\u30AB\u30BF\u30ED\u30B0\u30B5\u30A4\u30C8"
    lastrevid: 1362563672
    modified: '2021-02-16T13:25:18Z'
    ns: 0
    pageid: 95596396
    sitelinks: {}
    title: Q97153912
    type: item
ids:
  wikidata: Q97153912
services:
  catalogs:
  - client: html
    endpoint: https://www.data.go.jp/
    lang: jp
    name: "\u30C7\u30FC\u30BF\u30AB\u30BF\u30ED\u30B0\u30B5\u30A4\u30C8"
    platform: proprietary
  - client: html
    endpoint: https://www.data.go.jp/
    lang: en
    name: Data Catalog Site
    platform: proprietary
---
