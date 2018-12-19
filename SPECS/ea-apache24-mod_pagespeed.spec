%global ns_name ea-apache24
%global module_name mod_pagespeed

Summary: 		Apache module created by Google to help Make the Web Faster by rewriting web pages to reduce latency and bandwidth.
Name: 			ea-apache24-mod_pagespeed
Version: 		stable
%define 		release_prefix 5
Release: 		%{release_prefix}%{?dist}.cpanel
License: 		Apache Software License
Group: 			System Environment/Daemons
URL: 			http://modpagespeed.com/
Source0: 		466_pagespeed.conf
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
%if %{__isa_bits} == 64
	/bin/mv ../SOURCES/mod-pagespeed-stable_current_x86_64.rpm mod-pagespeed-stable.rpm
%endif
%if %{__isa_bits} == 32
	/bin/mv ../SOURCES/mod-pagespeed-stable_current_i386.rpm mod-pagespeed-stable.rpm
%endif

%build
rpm2cpio mod-pagespeed-stable.rpm  | cpio -idmv
%if %{__isa_bits} == 64
mv usr/lib64/httpd/modules/mod_pagespeed{,_ap24}.so .
%endif
%if %{__isa_bits} == 32
mv usr/lib/httpd/modules/mod_pagespeed{,_ap24}.so .
%endif
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

%clean
rm -rf %{buildroot}

%files
%defattr(0640,root,root,0755)
%attr(755,root,root)%{_libdir}/apache2/modules/*.so
%attr(644,root,root)%{_sysconfdir}/apache2/conf.modules.d/466_pagespeed.conf
%config(noreplace) %{_sysconfdir}/apache2/conf.modules.d/*.conf
%attr(755,nobody,nobody) %dir %{_localstatedir}/mod_pagespeed
%attr(755,nobody,nobody) %dir %{_localstatedir}/mod_pagespeed/cache

%changelog
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
