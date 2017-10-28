%global ns_name ea-apache24
%global module_name mod_pagespeed

Summary: 		Apache module created by Google to help Make the Web Faster by rewriting web pages to reduce latency and bandwidth.
Name: 			ea-apache24-mod_pagespeed
Version: 		stable
%define 		release_prefix 2
Release: 		%{release_prefix}%{?dist}.cpanel
License: 		Apache Software License
Group: 			System Environment/Daemons
URL: 			http://modpagespeed.com/
Source0: 		456_pagespeed.conf
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

%clean
rm -rf %{buildroot}

%files
%defattr(0640,root,root,0755)
%attr(755,root,root)%{_libdir}/apache2/modules/*.so
%attr(644,root,root)%{_sysconfdir}/apache2/conf.modules.d/456_pagespeed.conf
%config(noreplace) %{_sysconfdir}/apache2/conf.modules.d/*.conf

%changelog
* Sat Oct 28 2017 Cory McIntire <cory@cpanel.net> - stable-2
- EA-6674: fix up permissions on 456_pagespeed.conf file

* Tue Mar 14 2017 Jacob Perkins <jacob.perkins@cpanel.net> - stable-1
- Initial build
