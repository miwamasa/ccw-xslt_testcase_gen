<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>

  <!-- Identity template: copy everything by default -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Transform Source to Target -->
  <xsl:template match="Source">
    <Target>
      <xsl:apply-templates select="name"/>
      <xsl:apply-templates select="age"/>
      <xsl:apply-templates select="city"/>
    </Target>
  </xsl:template>

  <!-- Transform specific elements -->
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
