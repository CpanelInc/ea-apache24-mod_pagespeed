%global ns_name ea-apache24
%global module_name mod_pagespeed

Summary: 		Apache module created by Google to help Make the Web Faster by rewriting web pages to reduce latency and bandwidth.
Name: 			ea-apache24-mod_pagespeed
Version: 		1.14.36.1
%define 		release_prefix 1
Release: 		%{release_prefix}%{?dist}.cpanel
License: 		Apache Software License
Group: 			System Environment/Daemons
URL: 			http://modpagespeed.com/
Source0: 		510_pagespeed.conf
Vendor:			cPanel Inc.
BuildRequires: 	wget cpio ea-apr-util
Conflicts: 		%{ns_name}-mod_ruid2
Requires: 	ea-apache24 ea-apache24-mod_version

# Suppres auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
Apache module created by Google to help Make the Web Faster by rewriting web pages to reduce latency and bandwidth.

%prep
/bin/mv ../SOURCES/mod-pagespeed-stable_current_x86_64.rpm mod-pagespeed-stable.rpm

%build
rpm2cpio mod-pagespeed-stable.rpm  | cpio -idmv
mv usr/lib64/httpd/modules/mod_pagespeed{,_ap24}.so .
%{__strip} -g mod_pagespeed.so
%{__strip} -g mod_pagespeed_ap24.so

%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_sysconfdir}/apache2/conf.modules.d
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/apache2/conf.modules.d/

install -d -m 0755 %{buildroot}%{_libdir}/apache2/modules/
install -m755 mod_pagespeed.so %{buildroot}%{_libdir}/apache2/modules/
install -m755 mod_pagespeed_ap24.so %{buildroot}%{_libdir}/apache2/modules/

install -d %{buildroot}%{_localstatedir}/mod_pagespeed
install -d %{buildroot}%{_localstatedir}/mod_pagespeed/cache

%post
# If we are upgrading from the old version, then the old config file will
# be named 466_pagespeed.conf, copy it to 510_pagespeed.conf
# So it will be picked up as the current config file
if [ $1 == 2 ];then
	if [ -f "/etc/apache2/conf.modules.d/466_pagespeed.conf" ]; then
		cp /etc/apache2/conf.modules.d/466_pagespeed.conf /etc/apache2/conf.modules.d/510_pagespeed.conf
		rm /etc/apache2/conf.modules.d/466_pagespeed.conf
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(0640,root,root,0755)
%attr(755,root,root)%{_libdir}/apache2/modules/*.so
%attr(644,root,root)%{_sysconfdir}/apache2/conf.modules.d/510_pagespeed.conf
%config(noreplace) %{_sysconfdir}/apache2/conf.modules.d/*.conf
%attr(755,nobody,nobody) %dir %{_localstatedir}/mod_pagespeed
%attr(755,nobody,nobody) %dir %{_localstatedir}/mod_pagespeed/cache

%changelog
* Thu Feb 04 2021 Cory McIntire <cory@cpanel.net> - 1.14.36.1-1
- EA-9563: Update ea-apache24-mod_pagespeed from vstable to v1.14.36.1
           Remove 32 bit logic and RPM

* Mon Oct 12 2020 Tim Mullin <tim@cpanel.net> - stable-9
- EA-9262: Exclude cpanel. subdomain from Pagespeed

* Thu Mar 26 2020 Tim Mullin <tim@cpanel.net> - stable-8
- EA-8945: Make sure the old config file becomes the new config file

* Tue Mar 24 2020 Cory McIntire <cory@cpanel.net> - stable-7
- EA-8527: Move into production

* Wed Feb 19 2020 Tim Mullin <tim@cpanel.net> - stable-6
- EA-8806: Bump conf file prefix from 466 to 510 so it loads after mod_version

* Wed Dec 19 2018 Tim Mullin <tim@cpanel.net> - stable-5
- EA-8095: Bump conf file prefix from 456 to 466 so it loads after mod_version

* Mon Aug 20 2018 Cory McIntire <cory@cpanel.net> - stable-4
- EA-7761: Update to version 1.13.35.2

* Fri Aug 03 2018 Tim Mullin <tim@cpanel.net> - stable-3
- EA-6948: fix up ownership and permissions on /var/mod_pagespeed and /var/mod_pagespeed/cache

* Sat Oct 28 2017 Cory McIntire <cory@cpanel.net> - stable-2
- EA-6674: fix up permissions on 456_pagespeed.conf file

* Tue Mar 14 2017 Jacob Perkins <jacob.perkins@cpanel.net> - stable-1
- Initial build
