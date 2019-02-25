Name:           FirstBitcoinCapitalCorp
Version:        0.2.0
Release:        1%{?dist}
Summary:        FirstBitcoinCapitalCorp Wallet
Group:          Applications/Internet
Vendor:         FirstBitcoinCapitalCorp
License:        GPLv3
URL:            https://firstbitcoin.io/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  autoconf automake libtool gcc-c++ openssl-devel >= 1:1.0.2d libdb4-devel libdb4-cxx-devel miniupnpc-devel boost-devel boost-static
Requires:       openssl >= 1:1.0.2d libdb4 libdb4-cxx miniupnpc logrotate

%description
FirstBitcoinCapitalCorp Wallet

%prep
%setup -q

%build
./autogen.sh
./configure
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/etc/bitcf $RPM_BUILD_ROOT/etc/ssl/bit $RPM_BUILD_ROOT/var/lib/bit/.FirstBitcoinCapitalCorp $RPM_BUILD_ROOT/usr/lib/systemd/system $RPM_BUILD_ROOT/etc/logrotate.d
%{__install} -m 755 src/bitcfd $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 src/bitcf-cli $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 600 contrib/redhat/bitcf.conf $RPM_BUILD_ROOT/var/lib/bit/.FirstBitcoinCapitalCorp
%{__install} -m 644 contrib/redhat/bitcfd.service $RPM_BUILD_ROOT/usr/lib/systemd/system
%{__install} -m 644 contrib/redhat/bitcfd.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/bitcfd
%{__mv} -f contrib/redhat/bit $RPM_BUILD_ROOT%{_bindir}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pretrans
getent passwd bit >/dev/null && { [ -f /usr/bin/bitcfd ] || { echo "Looks like user 'bit' already exists and have to be deleted before continue."; exit 1; }; } || useradd -r -M -d /var/lib/bit -s /bin/false bit

%post
[ $1 == 1 ] && {
  sed -i -e "s/\(^rpcpassword=MySuperPassword\)\(.*\)/rpcpassword=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)/" /var/lib/bit/.FirstBitcoinCapitalCorp/bitcf.conf
  openssl req -nodes -x509 -newkey rsa:4096 -keyout /etc/ssl/bit/bitcf.key -out /etc/ssl/bit/bitcf.crt -days 3560 -subj /C=US/ST=Oregon/L=Portland/O=IT/CN=bitcf.bit
  ln -sf /var/lib/bit/.FirstBitcoinCapitalCorp/bitcf.conf /etc/bitcf/bitcf.conf
  ln -sf /etc/ssl/bit /etc/bitcf/certs
  chown bit.bit /etc/ssl/bit/bitcf.key /etc/ssl/bit/bitcf.crt
  chmod 600 /etc/ssl/bit/bitcf.key
} || exit 0

%posttrans
[ -f /var/lib/bit/.FirstBitcoinCapitalCorp/addr.dat ] && { cd /var/lib/bit/.FirstBitcoinCapitalCorp && rm -rf database addr.dat nameindex* blk* *.log .lock; }
sed -i -e 's|rpcallowip=\*|rpcallowip=0.0.0.0/0|' /var/lib/bit/.FirstBitcoinCapitalCorp/bitcf.conf
systemctl daemon-reload
systemctl status bitcfd >/dev/null && systemctl restart bitcfd || exit 0

%preun
[ $1 == 0 ] && {
  systemctl is-enabled bitcfd >/dev/null && systemctl disable bitcfd >/dev/null || true
  systemctl status bitcfd >/dev/null && systemctl stop bitcfd >/dev/null || true
  pkill -9 -u bit > /dev/null 2>&1
  getent passwd bit >/dev/null && userdel bit >/dev/null 2>&1 || true
  rm -f /etc/ssl/bit/bitcf.key /etc/ssl/bit/bitcf.crt /etc/bitcf/bitcf.conf /etc/bitcf/certs
} || exit 0

%files
%doc COPYING
%attr(750,bit,bit) %dir /etc/bitcf
%attr(750,bit,bit) %dir /etc/ssl/bit
%attr(700,bit,bit) %dir /var/lib/bit
%attr(700,bit,bit) %dir /var/lib/bit/.FirstBitcoinCapitalCorp
%attr(600,bit,bit) %config(noreplace) /var/lib/bit/.FirstBitcoinCapitalCorp/bitcf.conf
%attr(4750,bit,bit) %{_bindir}/bitcf-cli
%defattr(-,root,root)
%config(noreplace) /etc/logrotate.d/bitcfd
%{_bindir}/bitcfd
%{_bindir}/bit
/usr/lib/systemd/system/bitcfd.service

%changelog
* Thu Aug 31 2017 Aspanta Limited <info@aspanta.com> 0.6.3
- There is no changelog available. Please refer to the CHANGELOG file or visit the website.
