<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="openmetadata:omad:1_0"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="/">
        <Omad>
            <xsl:for-each select="/*/li">
                <xsl:variable name="id">
                    <xsl:analyze-string select="a/@href" regex="id=(.*)">
                        <xsl:matching-substring>
                            <xsl:value-of select="regex-group(1)"/>
                        </xsl:matching-substring>
                    </xsl:analyze-string>
                </xsl:variable>
                <Organization entityType="public" id="us-{lower-case($id)}">
                    <Name><xsl:value-of select="a"/></Name>
                    <Abbreviation><xsl:value-of select="upper-case($id)"/></Abbreviation>
                    <Location id="hq" countryCode="US"></Location>
                    <WebSite>
                        <DisplayLabel><xsl:value-of select="$id"/> FedSTATS Information Page</DisplayLabel>
                        <Url>http://www.fedstats.gov<xsl:value-of select="a/@href"/></Url>
                    </WebSite>
                    <Operations scope="national"/>
                    <Tags>
                        <Tab>fedstats</Tab>
                    </Tags>
                </Organization>
            </xsl:for-each>
        </Omad>
    </xsl:template>
    
</xsl:stylesheet>