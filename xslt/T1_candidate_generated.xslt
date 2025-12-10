<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>

  <!-- Auto-generated XSLT by simple mapping generator -->
  <xsl:template match="Order">
    <Invoice>
      <City><xsl:value-of select="city"/></City>
      <Country><xsl:value-of select="country"/></Country>
      <Email><xsl:value-of select="customerEmail"/></Email>
      <Name><xsl:value-of select="customerName"/></Name>
      <Phone><xsl:value-of select="customerPhone"/></Phone>
      <RequestedDelivery><xsl:value-of select="deliveryDate"/></RequestedDelivery>
      <Item><xsl:value-of select="item"/></Item>
      <Item><xsl:value-of select="itemCode"/></Item>
      <Item><xsl:value-of select="itemName"/></Item>
      <Price><xsl:value-of select="price"/></Price>
      <Quantity><xsl:value-of select="quantity"/></Quantity>
      <State><xsl:value-of select="state"/></State>
      <Street><xsl:value-of select="street"/></Street>
      <code><xsl:value-of select="zipCode"/></code>
    </Invoice>
  </xsl:template>

</xsl:stylesheet>
