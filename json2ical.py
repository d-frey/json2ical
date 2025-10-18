#!/usr/bin/env python3
import sys
import json
import icalendar
import zoneinfo
from datetime import datetime

file = open( sys.argv[ 1 ] )
data = json.load( file )

cal = icalendar.Calendar()
cal[ 'prodid' ] = '-//json2ical//github.com/d-frey/json2ical//'
cal[ 'version' ] = '2.0'

if 'summary' in data:
    cal[ 'summary' ] = data[ 'summary' ]

for entry in data[ 'events' ]:
    if 'timezone' in entry:
        tz = zoneinfo.ZoneInfo( entry[ 'timezone' ] )
    else:
        tz = None

    event = icalendar.Event()
    event.add( 'dtstart', datetime.fromisoformat( entry[ 'start' ] ).replace( tzinfo=tz ) )
    if 'end' in entry:
        event.add( 'dtend', datetime.fromisoformat( entry[ 'end' ] ).replace( tzinfo=tz ) )
    if 'stamp' in entry:
        event.add( 'dtstamp', entry[ 'stamp' ] )
    if 'summary' in entry:
        event.add( 'summary', entry[ 'summary' ] )
    if 'description' in entry:
        event.add( 'description', entry[ 'description' ] )
    if 'url' in entry:
        event.add( 'url', entry[ 'url' ] )
    if 'location' in entry:
        event.add( 'location', entry[ 'location' ] )
    if 'uid' in entry:
        event.add( 'uid', entry[ 'uid' ] )

    cal.add_component( event )

if len( sys.argv ) == 2:
    print( cal.to_ical().decode( 'utf-8' ).replace( '\r\n', '\n' ).strip() )
else:
    out = open( sys.argv[ 2 ], 'wb' )
    out.write( cal.to_ical() )
    out.close()
