<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>

  <!--
    Simple transformation candidate: Should match simple_T0_correct.xslt
    Source: <Source><name>...</name><age>...</age><city>...</city></Source>
    Target: <Target><fullName>...</fullName><years>...</years><location>...</location></Target>
  -->

  <!-- Identity template -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="Source">
    <Target>
      <xsl:apply-templates select="name"/>
      <xsl:apply-templates select="age"/>
      <xsl:apply-templates select="city"/>
    </Target>
  </xsl:template>

  <xsl:template match="name">
    <fullName><xsl:value-of select="."/></fullName>
  </xsl:template>

  <xsl:template match="age">
    <years><xsl:value-of select="."/></years>
  </xsl:template>

  <xsl:template match="city">
    <location><xsl:value-of select="."/></location>
  </xsl:template>
</xsl:stylesheet>
