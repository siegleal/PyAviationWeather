import urllib2
import xml.etree.ElementTree as ET

baseUrl = 'http://aviationweather.gov/adds/dataserver_current/httpparam?'
metarDataSource = 'datasource=metars'
tafsDataSource = 'datasource=tafs'
requestType = 'requesttype=retrieve'
mostRecentForEach = 'mostRecentForEachStation=constraint'
formatXml = 'format=xml'
formatCsv = 'format=csv'
DefaultHoursBeforeNow = 'hoursBeforeNow=1.25'

def buildStationString(stations):
    ''' Creates the url param for stationstrings
        by comma-separating the stations in the list '''
    return 'stationString=' + ','.join(stations)

def buildUrl(ds, stations):
    ''' Takes a datasource (metars or taf)
        and a list of stations and builds the aviationweather.gov url '''
    datasource = metarDataSource
    if (ds == 'taf'):
        datasource = tafsDataSource
    return baseUrl + '&'.join([datasource, requestType, formatXml, mostRecentForEach, DefaultHoursBeforeNow, buildStationString(stations)])

#returns a list of lines to print
def prettyPrintTaf(tafString):
    ''' Parses a multi-line TAF string to print in a human-readable format'''
    splittaf = tafString.split()
    index = 0
    newlist = []
    result = ['']
    while (index < len(splittaf) - 1):
        newlist.append(splittaf[index])
        if (splittaf[index + 1] == 'TEMPO' or splittaf[index + 1][:2] == 'FM'):
            result.append(' '.join(newlist))
            newlist = []
        index = index + 1
    result.append(' '.join(newlist))
    return result

def getXml(ds, stations):
    ''' Builds the URL based on the data source and station list and makes a request and returns 
        the raw XML http response '''
    return urllib2.urlopen(buildUrl(ds, stations)).read()

def getRawTexts(datasource, stationList):
    ''' Gets just the raw metar or taf for the given datasource (metar or taf) and stations in the station list '''
    result = []
    xml = getXml(datasource, stationList)
    root = ET.fromstring(xml)
    for data in root.findall('data'):
        for metar in data.findall('METAR'):
            result.append(metar.find('raw_text').text)
        for taf in data.findall('TAF'):
            result.extend(prettyPrintTaf(taf.find('raw_text').text))
    return result


