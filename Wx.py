import argparse
import AviationWeatherLib as awl

def main():
    parser = argparse.ArgumentParser(description='process stations')
    parser.add_argument('--stations', '-s', nargs="+", required=True, help='stations from which to get repoerts')
    parser.add_argument('--type', '-t', default='metar',help='metar or taf')
    parser.add_argument('--onlyUrl', '-u', action='store_true', help='output will only contain the url')
    parser.add_argument('--noParse','-p', action='store_true', help='output will contain raw xml')
    args = parser.parse_args()
    if (args.onlyUrl):
        print awl.buildUrl(args.type, args.stations)
    elif (args.noParse):
        print awl.getXml(args.type, args.stations)
    else:
        txts = awl.getRawTexts(args.type, args.stations)
        for txt in txts:
            print txt

if __name__ == '__main__':
    main()
    

