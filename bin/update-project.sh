#!/usr/bin/env bash

curl -XPOST \
  -k \
  --socks5-hostname localhost:8879 \
  -H 'Accepts: application/json' \
  -H 'Authorization: Bearer 9xqb2mRkTf0imqYKZ7k5A2ldZdYfXD' \
  'https://aap01.ruju.adc.lan/api/controller/v2/projects/8/update/'
