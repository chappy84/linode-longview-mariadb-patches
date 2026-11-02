Name:           perl-DBD-MySQL-MariaDB-compat
Version:        1
Release:        1%{?dist}
Summary:        MariaDB compatibility capability for perl-DBD-MySQL
License:        BSD-3-Clause
BuildArch:      noarch

Requires:       perl-DBD-MariaDB
Provides:       perl(DBD::mysql)
Obsoletes:      perl-DBD-MySQL

%description
Compatibility package for software that requires perl-DBD-MySQL, on systems using solely MariaDB packages.
The MariaDB Perl driver is installed as the replacement.

%files
