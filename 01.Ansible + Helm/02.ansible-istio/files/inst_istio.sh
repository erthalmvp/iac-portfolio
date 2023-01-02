#!/bin/bash

# Specify the Istio version that will be leveraged throughout these instructions
ISTIO_VERSION=1.4.0
cd /tmp
curl -sL "https://github.com/istio/istio/releases/download/$ISTIO_VERSION/istio-$ISTIO_VERSION-linux.tar.gz" | tar xz
cp istio-1.4.0/bin/istioctl /usr/local/bin/
