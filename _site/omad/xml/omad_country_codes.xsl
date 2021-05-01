<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:omad="openmetadata:omad:1_0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    version="1.0">
    <xsl:output method="text" encoding="UTF-8"/>
    
    <!-- extract country code/names from schema documentation -->
    <xsl:template match="/">
        <xsl:apply-templates select="/xs:schema/xs:simpleType[@name='Iso2CountryCodeType']" mode="xsl"/>
    </xsl:template>
    
    <xsl:template match="xs:simpleType" mode="xsl">
        <xsl:text>&lt;xsl:choose&gt;&#13;</xsl:text>
        <xsl:for-each select="xs:restriction/xs:enumeration">
            <xsl:text>&lt;xsl:when test="@countryCode='</xsl:text>
            <xsl:value-of select="@value"/>
            <xsl:text>'"&gt;</xsl:text>
            <xsl:value-of select="xs:annotation/xs:documentation"/>
            <xsl:text>&lt;/xsl:when&gt;&#13;</xsl:text>
        </xsl:for-each>
        
        <xsl:text>&lt;/xsl:choose&gt;&#13;</xsl:text>
    </xsl:template>
        
    <!-- JavaScript Array -->
    <xsl:template match="xs:simpleType" mode="js">
        
    </xsl:template>
    
</xsl:stylesheet>