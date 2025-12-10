<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>

  <!-- Improved XSLT v2 - Based on test feedback -->
  <!-- Changes: Added nested structure, attributes, for-each, conditional logic -->

  <xsl:template match="Order">
    <Invoice>
      <!-- Add id attribute from orderNumber -->
      <xsl:attribute name="id">
        <xsl:value-of select="orderNumber"/>
      </xsl:attribute>

      <!-- Group customer information into nested structure -->
      <CustomerInfo>
        <Name><xsl:value-of select="customerName"/></Name>
        <Email><xsl:value-of select="customerEmail"/></Email>
        <xsl:if test="customerPhone">
          <Phone><xsl:value-of select="customerPhone"/></Phone>
        </xsl:if>
      </CustomerInfo>

      <!-- Transform items with for-each loop -->
      <Items>
        <xsl:for-each select="item">
          <Item>
            <!-- Add code attribute -->
            <xsl:attribute name="code">
              <xsl:value-of select="../itemCode"/>
            </xsl:attribute>
            <Description><xsl:value-of select="../itemName"/></Description>
            <Quantity><xsl:value-of select="../quantity"/></Quantity>
            <Price currency="USD"><xsl:value-of select="../price"/></Price>
          </Item>
        </xsl:for-each>
      </Items>

      <!-- Group shipping information into nested structure -->
      <ShippingDetails>
        <Address>
          <Street><xsl:value-of select="street"/></Street>
          <City><xsl:value-of select="city"/></City>
          <xsl:if test="state">
            <State><xsl:value-of select="state"/></State>
          </xsl:if>
          <PostalCode><xsl:value-of select="zipCode"/></PostalCode>
          <Country><xsl:value-of select="country"/></Country>
        </Address>
        <xsl:if test="deliveryDate">
          <RequestedDelivery><xsl:value-of select="deliveryDate"/></RequestedDelivery>
        </xsl:if>
      </ShippingDetails>

    </Invoice>
  </xsl:template>

</xsl:stylesheet>
