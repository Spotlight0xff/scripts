#!/bin/sh
CURDIR=`dirname $0`
pkill -f i3-wsbar
pkill -f dzen2
sleep 1
$CURDIR/i3-wsbar | $CURDIR/dzen2 -bg "#111111" -dock b -e 'button5=exec:i3-msg workspace next;button4=exec:i3-msg workspace prev'
