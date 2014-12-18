import urllib2
import xml.etree.ElementTree as ET
import argparse

baseUrl = 'http://aviationweather.gov/adds/dataserver_current/httpparam?'
metarDataSource = 'datasource=metars'
tafsDataSource = 'datasource=tafs'
requestType = 'requesttype=retrieve'
mostRecentForEach = 'mostRecentForEachStation=constraint'
formatXml = 'format=xml'
formatCsv = 'format=csv'
DefaultHoursBeforeNow = 'hoursBeforeNow=1.25'

def buildStationString(stations):
    return 'stationString=' + ','.join(stations)

def buildUrl(ds, stations):
    datasource = metarDataSource
    if (ds == 'taf'):
        datasource = tafsDataSource
    return baseUrl + '&'.join([datasource, requestType, formatXml, mostRecentForEach, DefaultHoursBeforeNow, buildStationString(stations)])

#returns a list of lines to print
def prettyPrintTaf(tafString):
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
    return urllib2.urlopen(buildUrl(ds, stations)).read()

def getRawTexts(datasource, stationList):
    result = []
    xml = getXml(datasource, stationList)
    root = ET.fromstring(xml)
    for data in root.findall('data'):
        for metar in data.findall('METAR'):
            result.append(metar.find('raw_text').text)
        for taf in data.findall('TAF'):
            result.extend(prettyPrintTaf(taf.find('raw_text').text))
    return result

def main():
    parser = argparse.ArgumentParser(description='process stations')
    parser.add_argument('--stations', '-s', nargs="+", required=True, help='stations from which to get repoerts')
    parser.add_argument('--type', '-t', default='metar',help='metar or taf')
    parser.add_argument('--onlyUrl', '-u', action='store_true', help='output will only contain the url')
    parser.add_argument('--noParse','-p', action='store_true', help='output will contain raw xml')
    args = parser.parse_args()
    if (args.onlyUrl):
        print buildUrl(args.type, args.stations)
    elif (args.noParse):
        print getXml(args.type, args.stations)
    else:
        txts = getRawTexts(args.type, args.stations)
        for txt in txts:
            print txt

if __name__ == '__main__':
    main()
    

