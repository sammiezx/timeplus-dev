#!/bin/bash

TIMEPLUS_VERSION=2.4.11
TIMEPLUS_DOWNLOAD_URL=https://timeplus.io/dist/timeplus_enterprise/timeplus-enterprise-v${TIMEPLUS_VERSION}-linux-amd64.tar.gz
TIMEPLUS_TAR=timeplus-enterprise-v${TIMEPLUS_VERSION}-linux-amd64.tar.gz

# sudo apt-get update
# sudo apt-get install -y wget tar build-essential gcc g++ make python3 python3-pip python3-venv

wget ${TIMEPLUS_DOWNLOAD_URL}
tar xfv ${TIMEPLUS_TAR}
rm ${TIMEPLUS_TAR}


virtualenv env 
source env/bin/activate
pip install -r requirements.txt

# sudo kill -9 <pid> for port/s: [5432]
timeplus/bin/timeplus start &
sleep 30 #IMPORTANT! CREATE A ACCOUNT OR LOGIN FROM THE WEB INTERFACE ON PORT 8000

python3 src/builders/build_jupiter_token_table.py 
sleep 5
python3 src/builders/build_ingestion.py 

wait
