

trackingfile=/tmp/trackingfile$$
echo "Logging in $trackingfile..."

echo "CTRL+C to stop"

URL=https://pdf-amit-65aqzgjh5a-uc.a.run.app 

function perf {
  curl -o /dev/null -s -w "%{time_connect} + %{time_starttransfer} = %{time_total}\n" "$1" >> $trackingfile &
}

while [ $index -gt 0 ] ; do

    perf $URL 

index=$((index-1))
done