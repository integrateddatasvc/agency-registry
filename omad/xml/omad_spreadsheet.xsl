<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:omad="openmetadata:omad:1_0"
    version="1.0">
    <xsl:output method="text" encoding="UTF-8"/>
    
    <xsl:template match="/">
        <xsl:text>Id,LocationId,Name,Entity,Scope,Url,Address,Country,Iso2,Longitude,Latitude,Accuracy&#13;</xsl:text>
        <xsl:apply-templates  select="/*/omad:Organization"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="omad:Organization">
        <xsl:variable name="orgId"><xsl:value-of select="@id"/></xsl:variable>
        <xsl:variable name="name"><xsl:value-of select="omad:Name[1]"/></xsl:variable>
        <xsl:variable name="entity"><xsl:value-of select="@entityType"/></xsl:variable>
        <xsl:variable name="scope"><xsl:value-of select="omad:Operations/@scope"/></xsl:variable>
        <xsl:variable name="url"><xsl:value-of select="omad:WebSite[1]/omad:Url"/></xsl:variable>
        <xsl:for-each select="omad:Location">
            <xsl:variable name="locId"><xsl:value-of select="@id"/></xsl:variable>
            <xsl:variable name="address">
                <xsl:apply-templates select="omad:Address"/>
            </xsl:variable>
            <xsl:variable name="iso2" select="@countryCode"/>
            <xsl:variable name="country">
                <xsl:apply-templates select="."></xsl:apply-templates>
            </xsl:variable>
            <xsl:variable name="longitude" select="omad:MapLocation/omad:Longitude"/>
            <xsl:variable name="latitude" select="omad:MapLocation/omad:Latitude"/>
            <xsl:variable name="accuracy" select="omad:MapLocation/@accuracy"/>
            <!-- output -->
            <xsl:value-of select="$orgId"/>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$locId"/>
            <xsl:text>,</xsl:text>
            <xsl:text>"</xsl:text><xsl:value-of select='replace($name,"""","""""")'/><xsl:text>"</xsl:text>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$entity"/>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$scope"/>
            <xsl:text>,</xsl:text>
            <xsl:text>"</xsl:text><xsl:value-of select="$url"/><xsl:text>"</xsl:text>
            <xsl:text>,</xsl:text>
            <xsl:text>"</xsl:text><xsl:value-of select="$address"/><xsl:text>"</xsl:text>
            <xsl:text>,</xsl:text>
            <xsl:text>"</xsl:text><xsl:value-of select="$country"/><xsl:text>"</xsl:text>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$iso2"/>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$longitude"/>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$latitude"/>
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$accuracy"/>
            <xsl:text>&#13;</xsl:text>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="omad:Address">
        <xsl:for-each select="omad:Line">
            <xsl:if test="position()>1">
                <xsl:text>, </xsl:text>
            </xsl:if>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:if test="omad:City">
            <xsl:if test="omad:City/preceding-sibling::omad:*">
                <xsl:text>, </xsl:text>
            </xsl:if>
            <xsl:value-of select="omad:City"/>
        </xsl:if>
        <xsl:if test="omad:State">
            <xsl:if test="omad:State/preceding-sibling::omad:*">
                <xsl:text>, </xsl:text>
            </xsl:if>
            <xsl:value-of select="omad:State"/>
        </xsl:if>
        <xsl:if test="omad:Postal">
            <xsl:if test="omad:Postal/preceding-sibling::omad:*">
                <xsl:text> </xsl:text>
            </xsl:if>
            <xsl:value-of select="omad:Postal"/>
        </xsl:if>
    </xsl:template>
        
    <xsl:template match="omad:Location">
        <xsl:choose>
            <xsl:when test="@countryCode='AX'">Aaland Islands</xsl:when>
            <xsl:when test="@countryCode='AF'">Afghanistan</xsl:when>
            <xsl:when test="@countryCode='AL'">Albania</xsl:when>
            <xsl:when test="@countryCode='DZ'">Algeria</xsl:when>
            <xsl:when test="@countryCode='AS'">American Samoa</xsl:when>
            <xsl:when test="@countryCode='AD'">Andorra</xsl:when>
            <xsl:when test="@countryCode='AO'">Angola</xsl:when>
            <xsl:when test="@countryCode='AI'">Anguilla</xsl:when>
            <xsl:when test="@countryCode='AQ'">Antarctica</xsl:when>
            <xsl:when test="@countryCode='AG'">Antigua and Barbuda</xsl:when>
            <xsl:when test="@countryCode='AR'">Argentina</xsl:when>
            <xsl:when test="@countryCode='AM'">Armenia</xsl:when>
            <xsl:when test="@countryCode='AW'">Aruba</xsl:when>
            <xsl:when test="@countryCode='AU'">Australia</xsl:when>
            <xsl:when test="@countryCode='AT'">Austria</xsl:when>
            <xsl:when test="@countryCode='AZ'">Azerbaijan</xsl:when>
            <xsl:when test="@countryCode='BS'">Bahamas</xsl:when>
            <xsl:when test="@countryCode='BH'">Bahrain</xsl:when>
            <xsl:when test="@countryCode='BD'">Bangladesh</xsl:when>
            <xsl:when test="@countryCode='BB'">Barbados</xsl:when>
            <xsl:when test="@countryCode='BY'">Belarus</xsl:when>
            <xsl:when test="@countryCode='BE'">Belgium</xsl:when>
            <xsl:when test="@countryCode='BZ'">Belize</xsl:when>
            <xsl:when test="@countryCode='BJ'">Benin</xsl:when>
            <xsl:when test="@countryCode='BM'">Bermuda</xsl:when>
            <xsl:when test="@countryCode='BT'">Bhutan</xsl:when>
            <xsl:when test="@countryCode='BO'">Bolivia</xsl:when>
            <xsl:when test="@countryCode='BA'">Bosnia and Herzegowina</xsl:when>
            <xsl:when test="@countryCode='BW'">Botswana</xsl:when>
            <xsl:when test="@countryCode='BV'">Bouvet Island</xsl:when>
            <xsl:when test="@countryCode='BR'">Brazil</xsl:when>
            <xsl:when test="@countryCode='IO'">British Indian Ocean Territory</xsl:when>
            <xsl:when test="@countryCode='BN'">Brunei Darussalam</xsl:when>
            <xsl:when test="@countryCode='BG'">Bulgaria</xsl:when>
            <xsl:when test="@countryCode='BF'">Burkina Faso</xsl:when>
            <xsl:when test="@countryCode='BI'">Burundi</xsl:when>
            <xsl:when test="@countryCode='KH'">Cambodia</xsl:when>
            <xsl:when test="@countryCode='CM'">Cameroon</xsl:when>
            <xsl:when test="@countryCode='CA'">Canada</xsl:when>
            <xsl:when test="@countryCode='CV'">Cape Verde</xsl:when>
            <xsl:when test="@countryCode='KY'">Cayman Islands</xsl:when>
            <xsl:when test="@countryCode='CF'">Central African Republic</xsl:when>
            <xsl:when test="@countryCode='TD'">Chad</xsl:when>
            <xsl:when test="@countryCode='CL'">Chile</xsl:when>
            <xsl:when test="@countryCode='CN'">China</xsl:when>
            <xsl:when test="@countryCode='CX'">Christmas Island</xsl:when>
            <xsl:when test="@countryCode='CC'">Cocos (Keeling) Islands</xsl:when>
            <xsl:when test="@countryCode='CO'">Colombia</xsl:when>
            <xsl:when test="@countryCode='KM'">Comoros</xsl:when>
            <xsl:when test="@countryCode='CD'">Congo, Democratic Republic Of</xsl:when>
            <xsl:when test="@countryCode='CG'">Congo, Republic Of</xsl:when>
            <xsl:when test="@countryCode='CK'">Cook Islands</xsl:when>
            <xsl:when test="@countryCode='CR'">Costa Rica</xsl:when>
            <xsl:when test="@countryCode='CI'">Cote D'ivoire</xsl:when>
            <xsl:when test="@countryCode='HR'">Croatia</xsl:when>
            <xsl:when test="@countryCode='CU'">Cuba</xsl:when>
            <xsl:when test="@countryCode='CW'">Cura√ßao</xsl:when>
            <xsl:when test="@countryCode='CY'">Cyprus</xsl:when>
            <xsl:when test="@countryCode='CZ'">Czech Republic</xsl:when>
            <xsl:when test="@countryCode='DK'">Denmark</xsl:when>
            <xsl:when test="@countryCode='DJ'">Djibouti</xsl:when>
            <xsl:when test="@countryCode='DM'">Dominica</xsl:when>
            <xsl:when test="@countryCode='DO'">Dominican Republic</xsl:when>
            <xsl:when test="@countryCode='EC'">Ecuador</xsl:when>
            <xsl:when test="@countryCode='EG'">Egypt</xsl:when>
            <xsl:when test="@countryCode='SV'">El Salvador</xsl:when>
            <xsl:when test="@countryCode='GQ'">Equatorial Guinea</xsl:when>
            <xsl:when test="@countryCode='ER'">Eritrea</xsl:when>
            <xsl:when test="@countryCode='EE'">Estonia</xsl:when>
            <xsl:when test="@countryCode='ET'">Ethiopia</xsl:when>
            <xsl:when test="@countryCode='FK'">Falkland Islands (Malvinas)</xsl:when>
            <xsl:when test="@countryCode='FO'">Faroe Islands</xsl:when>
            <xsl:when test="@countryCode='FJ'">Fiji</xsl:when>
            <xsl:when test="@countryCode='FI'">Finland</xsl:when>
            <xsl:when test="@countryCode='FR'">France</xsl:when>
            <xsl:when test="@countryCode='GF'">French Guiana</xsl:when>
            <xsl:when test="@countryCode='PF'">French Polynesia</xsl:when>
            <xsl:when test="@countryCode='TF'">French Southern Territories</xsl:when>
            <xsl:when test="@countryCode='GA'">Gabon</xsl:when>
            <xsl:when test="@countryCode='GM'">Gambia</xsl:when>
            <xsl:when test="@countryCode='GE'">Georgia</xsl:when>
            <xsl:when test="@countryCode='DE'">Germany</xsl:when>
            <xsl:when test="@countryCode='GH'">Ghana</xsl:when>
            <xsl:when test="@countryCode='GI'">Gibraltar</xsl:when>
            <xsl:when test="@countryCode='GR'">Greece</xsl:when>
            <xsl:when test="@countryCode='GL'">Greenland</xsl:when>
            <xsl:when test="@countryCode='GD'">Grenada</xsl:when>
            <xsl:when test="@countryCode='GP'">Guadeloupe</xsl:when>
            <xsl:when test="@countryCode='GU'">Guam</xsl:when>
            <xsl:when test="@countryCode='GT'">Guatemala</xsl:when>
            <xsl:when test="@countryCode='GN'">Guinea</xsl:when>
            <xsl:when test="@countryCode='GW'">Guinea-Bissau</xsl:when>
            <xsl:when test="@countryCode='GY'">Guyana</xsl:when>
            <xsl:when test="@countryCode='HT'">Haiti</xsl:when>
            <xsl:when test="@countryCode='HM'">Heard and Mc Donald Islands</xsl:when>
            <xsl:when test="@countryCode='HN'">Honduras</xsl:when>
            <xsl:when test="@countryCode='HK'">Hong Kong</xsl:when>
            <xsl:when test="@countryCode='HU'">Hungary</xsl:when>
            <xsl:when test="@countryCode='IS'">Iceland</xsl:when>
            <xsl:when test="@countryCode='IN'">India</xsl:when>
            <xsl:when test="@countryCode='ID'">Indonesia</xsl:when>
            <xsl:when test="@countryCode='IR'">Iran (Islamic Republic Of)</xsl:when>
            <xsl:when test="@countryCode='IQ'">Iraq</xsl:when>
            <xsl:when test="@countryCode='IE'">Ireland</xsl:when>
            <xsl:when test="@countryCode='IL'">Israel</xsl:when>
            <xsl:when test="@countryCode='IT'">Italy</xsl:when>
            <xsl:when test="@countryCode='JM'">Jamaica</xsl:when>
            <xsl:when test="@countryCode='JP'">Japan</xsl:when>
            <xsl:when test="@countryCode='JO'">Jordan</xsl:when>
            <xsl:when test="@countryCode='KZ'">Kazakhstan</xsl:when>
            <xsl:when test="@countryCode='KE'">Kenya</xsl:when>
            <xsl:when test="@countryCode='KI'">Kiribati</xsl:when>
            <xsl:when test="@countryCode='KP'">Korea, Democratic People's Republic Of</xsl:when>
            <xsl:when test="@countryCode='KR'">Korea, Republic Of</xsl:when>
            <xsl:when test="@countryCode='KW'">Kuwait</xsl:when>
            <xsl:when test="@countryCode='XK'">Kosovo</xsl:when>
            <xsl:when test="@countryCode='KG'">Kyrgyzstan</xsl:when>
            <xsl:when test="@countryCode='LA'">Lao People's Democratic Republic</xsl:when>
            <xsl:when test="@countryCode='LV'">Latvia</xsl:when>
            <xsl:when test="@countryCode='LB'">Lebanon</xsl:when>
            <xsl:when test="@countryCode='LS'">Lesotho</xsl:when>
            <xsl:when test="@countryCode='LR'">Liberia</xsl:when>
            <xsl:when test="@countryCode='LY'">Libyan Arab Jamahiriya</xsl:when>
            <xsl:when test="@countryCode='LI'">Liechtenstein</xsl:when>
            <xsl:when test="@countryCode='LT'">Lithuania</xsl:when>
            <xsl:when test="@countryCode='LU'">Luxembourg</xsl:when>
            <xsl:when test="@countryCode='MO'">Macau</xsl:when>
            <xsl:when test="@countryCode='MK'">Macedonia, The Former Yugoslav Republic Of</xsl:when>
            <xsl:when test="@countryCode='MG'">Madagascar</xsl:when>
            <xsl:when test="@countryCode='MW'">Malawi</xsl:when>
            <xsl:when test="@countryCode='MY'">Malaysia</xsl:when>
            <xsl:when test="@countryCode='MV'">Maldives</xsl:when>
            <xsl:when test="@countryCode='ML'">Mali</xsl:when>
            <xsl:when test="@countryCode='MT'">Malta</xsl:when>
            <xsl:when test="@countryCode='MH'">Marshall Islands</xsl:when>
            <xsl:when test="@countryCode='MQ'">Martinique</xsl:when>
            <xsl:when test="@countryCode='MR'">Mauritania</xsl:when>
            <xsl:when test="@countryCode='MU'">Mauritius</xsl:when>
            <xsl:when test="@countryCode='YT'">Mayotte</xsl:when>
            <xsl:when test="@countryCode='MX'">Mexico</xsl:when>
            <xsl:when test="@countryCode='FM'">Micronesia, Federated States Of</xsl:when>
            <xsl:when test="@countryCode='MD'">Moldova, Republic Of</xsl:when>
            <xsl:when test="@countryCode='MC'">Monaco</xsl:when>
            <xsl:when test="@countryCode='MN'">Mongolia</xsl:when>
            <xsl:when test="@countryCode='ME'">Montenegro</xsl:when>
            <xsl:when test="@countryCode='MS'">Montserrat</xsl:when>
            <xsl:when test="@countryCode='MA'">Morocco</xsl:when>
            <xsl:when test="@countryCode='MZ'">Mozambique</xsl:when>
            <xsl:when test="@countryCode='MM'">Myanmar</xsl:when>
            <xsl:when test="@countryCode='NA'">Namibia</xsl:when>
            <xsl:when test="@countryCode='NR'">Nauru</xsl:when>
            <xsl:when test="@countryCode='NP'">Nepal</xsl:when>
            <xsl:when test="@countryCode='NL'">Netherlands</xsl:when>
            <xsl:when test="@countryCode='AN'">Netherlands Antilles</xsl:when>
            <xsl:when test="@countryCode='NC'">New Caledonia</xsl:when>
            <xsl:when test="@countryCode='NZ'">New Zealand</xsl:when>
            <xsl:when test="@countryCode='NI'">Nicaragua</xsl:when>
            <xsl:when test="@countryCode='NE'">Niger</xsl:when>
            <xsl:when test="@countryCode='NG'">Nigeria</xsl:when>
            <xsl:when test="@countryCode='NU'">Niue</xsl:when>
            <xsl:when test="@countryCode='NF'">Norfolk Island</xsl:when>
            <xsl:when test="@countryCode='TRNC'">Northern Cyprus</xsl:when>
            <xsl:when test="@countryCode='MP'">Northern Mariana Islands</xsl:when>
            <xsl:when test="@countryCode='NO'">Norway</xsl:when>
            <xsl:when test="@countryCode='OM'">Oman</xsl:when>
            <xsl:when test="@countryCode='PK'">Pakistan</xsl:when>
            <xsl:when test="@countryCode='PW'">Palau</xsl:when>
            <xsl:when test="@countryCode='PS'">Palestinian Territory, Occupied</xsl:when>
            <xsl:when test="@countryCode='PA'">Panama</xsl:when>
            <xsl:when test="@countryCode='PG'">Papua New Guinea</xsl:when>
            <xsl:when test="@countryCode='PY'">Paraguay</xsl:when>
            <xsl:when test="@countryCode='PE'">Peru</xsl:when>
            <xsl:when test="@countryCode='PH'">Philippines</xsl:when>
            <xsl:when test="@countryCode='PN'">Pitcairn</xsl:when>
            <xsl:when test="@countryCode='PL'">Poland</xsl:when>
            <xsl:when test="@countryCode='PT'">Portugal</xsl:when>
            <xsl:when test="@countryCode='PR'">Puerto Rico</xsl:when>
            <xsl:when test="@countryCode='QA'">Qatar</xsl:when>
            <xsl:when test="@countryCode='RE'">Reunion</xsl:when>
            <xsl:when test="@countryCode='RO'">Romania</xsl:when>
            <xsl:when test="@countryCode='RU'">Russian Federation</xsl:when>
            <xsl:when test="@countryCode='RW'">Rwanda</xsl:when>
            <xsl:when test="@countryCode='SH'">Saint Helena</xsl:when>
            <xsl:when test="@countryCode='KN'">Saint Kitts and Nevis</xsl:when>
            <xsl:when test="@countryCode='LC'">Saint Lucia</xsl:when>
            <xsl:when test="@countryCode='PM'">Saint Pierre and Miquelon</xsl:when>
            <xsl:when test="@countryCode='VC'">Saint Vincent and The Grenadines</xsl:when>
            <xsl:when test="@countryCode='WS'">Samoa</xsl:when>
            <xsl:when test="@countryCode='SM'">San Marino</xsl:when>
            <xsl:when test="@countryCode='ST'">Sao Tome and Principe</xsl:when>
            <xsl:when test="@countryCode='SA'">Saudi Arabia</xsl:when>
            <xsl:when test="@countryCode='SN'">Senegal</xsl:when>
            <xsl:when test="@countryCode='CS'">Serbia and Montenegro</xsl:when>
            <xsl:when test="@countryCode='SC'">Seychelles</xsl:when>
            <xsl:when test="@countryCode='RS'">Serbia</xsl:when>
            <xsl:when test="@countryCode='SL'">Sierra Leone</xsl:when>
            <xsl:when test="@countryCode='SG'">Singapore</xsl:when>
            <xsl:when test="@countryCode='SK'">Slovakia</xsl:when>
            <xsl:when test="@countryCode='SI'">Slovenia</xsl:when>
            <xsl:when test="@countryCode='SB'">Solomon Islands</xsl:when>
            <xsl:when test="@countryCode='SO'">Somalia</xsl:when>
            <xsl:when test="@countryCode='ZA'">South Africa</xsl:when>
            <xsl:when test="@countryCode='GS'">South Georgia and The South Sandwich Islands</xsl:when>
            <xsl:when test="@countryCode='SS'">South Sudan</xsl:when>
            <xsl:when test="@countryCode='ES'">Spain</xsl:when>
            <xsl:when test="@countryCode='LK'">Sri Lanka</xsl:when>
            <xsl:when test="@countryCode='SD'">Sudan</xsl:when>
            <xsl:when test="@countryCode='SR'">Suriname</xsl:when>
            <xsl:when test="@countryCode='SJ'">Svalbard and Jan Mayen Islands</xsl:when>
            <xsl:when test="@countryCode='SZ'">Swaziland</xsl:when>
            <xsl:when test="@countryCode='SE'">Sweden</xsl:when>
            <xsl:when test="@countryCode='CH'">Switzerland</xsl:when>
            <xsl:when test="@countryCode='SY'">Syrian Arab Republic</xsl:when>
            <xsl:when test="@countryCode='TW'">Taiwan</xsl:when>
            <xsl:when test="@countryCode='TJ'">Tajikistan</xsl:when>
            <xsl:when test="@countryCode='TZ'">Tanzania, United Republic Of</xsl:when>
            <xsl:when test="@countryCode='TH'">Thailand</xsl:when>
            <xsl:when test="@countryCode='TL'">Timor-Leste</xsl:when>
            <xsl:when test="@countryCode='TG'">Togo</xsl:when>
            <xsl:when test="@countryCode='TK'">Tokelau</xsl:when>
            <xsl:when test="@countryCode='TO'">Tonga</xsl:when>
            <xsl:when test="@countryCode='TT'">Trinidad and Tobago</xsl:when>
            <xsl:when test="@countryCode='TN'">Tunisia</xsl:when>
            <xsl:when test="@countryCode='TR'">Turkey</xsl:when>
            <xsl:when test="@countryCode='TM'">Turkmenistan</xsl:when>
            <xsl:when test="@countryCode='TC'">Turks and Caicos Islands</xsl:when>
            <xsl:when test="@countryCode='TV'">Tuvalu</xsl:when>
            <xsl:when test="@countryCode='UG'">Uganda</xsl:when>
            <xsl:when test="@countryCode='UA'">Ukraine</xsl:when>
            <xsl:when test="@countryCode='AE'">United Arab Emirates</xsl:when>
            <xsl:when test="@countryCode='GB'">United Kingdom</xsl:when>
            <xsl:when test="@countryCode='US'">United States</xsl:when>
            <xsl:when test="@countryCode='UM'">United States Minor Outlying Islands</xsl:when>
            <xsl:when test="@countryCode='UY'">Uruguay</xsl:when>
            <xsl:when test="@countryCode='UZ'">Uzbekistan</xsl:when>
            <xsl:when test="@countryCode='VU'">Vanuatu</xsl:when>
            <xsl:when test="@countryCode='VA'">Vatican City State (Holy See)</xsl:when>
            <xsl:when test="@countryCode='VE'">Venezuela</xsl:when>
            <xsl:when test="@countryCode='VN'">Viet Nam</xsl:when>
            <xsl:when test="@countryCode='VG'">Virgin Islands (British)</xsl:when>
            <xsl:when test="@countryCode='VI'">Virgin Islands (U.S.)</xsl:when>
            <xsl:when test="@countryCode='WF'">Wallis and Futuna Islands</xsl:when>
            <xsl:when test="@countryCode='EH'">Western Sahara</xsl:when>
            <xsl:when test="@countryCode='YE'">Yemen</xsl:when>
            <xsl:when test="@countryCode='ZM'">Zambia</xsl:when>
            <xsl:when test="@countryCode='ZW'">Zimbabwe</xsl:when>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>