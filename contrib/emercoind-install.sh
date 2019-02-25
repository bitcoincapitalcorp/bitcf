#!/bin/sh
# Install script for FirstBitcoinCapitalCorp Daemin and 2 cli - mainnet/testnet
# Before install, you needed to create usernames/group:

BITGROUP=bitcf
BITUSER=bit
TBITUSER=tbit

DST=${1:-'/usr/local/bin'}

function install_cli() {
  cp bitcf-cli $DST/$1
  chown $1:$BITGROUP $DST/$1
  chmod 4750 $DST/$1
}

echo "Install bitcf to: $DST"
cp bitcfd $DST/bitcfd
chown root:$BITGROUP $DST/bitcfd
chmod 750  $DST/bitcfd

install_cli $BITUSER
install_cli $TBITUSER

