#!/bin/bash
URL=$1
echo "http://tny.im/yourls-api.php?action=shorturl\&format=simple\&url=${URL}"
echo `wget -q -O - http://tny.im/yourls-api.php?action=shorturl\&format=simple\&url=${URL}`