Name:           linode-longview-mariadb-fix
Version:        1
Release:        1%{?dist}
Summary:        Re/apply local MariaDB changes to Linode Longview
License:        BSD-3-Clause
Requires:       bash
Requires:       linode-longview
Requires:       patch
Requires:       perl-DBD-MariaDB
BuildArch:      noarch

%description
Applies a locally supplied patch to Longview after its package is installed
or updated.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_datadir}/linode-longview-mariadb-fix
cp $OLDPWD/linode-longview-mariadb-fix %{buildroot}%{_libexecdir}/linode-longview-mariadb-fix
cp $OLDPWD/longview.patch %{buildroot}%{_datadir}/linode-longview-mariadb-fix/longview.patch

%files
%attr(0755,root,root) %{_libexecdir}/linode-longview-mariadb-fix
%attr(0755,root,root) %dir %{_datadir}/linode-longview-mariadb-fix
%attr(0644,root,root) %{_datadir}/linode-longview-mariadb-fix/longview.patch

%triggerin -- linode-longview
if %{_libexecdir}/linode-longview-mariadb-fix; then
    if systemctl is-active --quiet longview.service; then
        systemctl restart longview.service
    fi
fi

%post
if %{_libexecdir}/linode-longview-mariadb-fix; then
    if systemctl is-active --quiet longview.service; then
        systemctl restart longview.service
    fi
fi

%preun
if %{_libexecdir}/linode-longview-mariadb-fix remove; then
    if systemctl is-active --quiet longview.service; then
        systemctl restart longview.service
    fi
fi
