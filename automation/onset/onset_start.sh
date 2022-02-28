czas=$(date +%s%N | cut -b1-16)
echo $czas
sed -i 's/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/'$czas'/g' onset_event_start
cat onset_event_start

curl https://portal.api.simpledemo.onap.org:30226/events/unauthenticated.DCAE_CL_OUTPUT/?timeout=5000 -i -k -X POST\
  --header 'accept: application/json' \
  --header 'cache-control: no-cache' \
  --header 'Content-type: application/json' \
 -d '@onset_event_start'

