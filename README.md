# Linode Longview MariaDB Patches

This repo contains packages to ensure Longview can work with MariaDB

There's two dependency packages:

### 1. linode-longview-mariadb-fix
Note, you need [linode-longview repo](https://techdocs.akamai.com/cloud-computing/docs/getting-started-with-longview#manual-installation) added to use this rpm.

When using MariaDB, instead of MySQL, this is primarily intended to install the required MariaDB perl dependency from the package manager, and ensure that the core utilises use the different DB library. It [patches](linode-longview-mariadb-fix/longview.patch) the [longview source perl code](https://github.com/linode/longview/blob/master/Linode/Longview/DataGetter/Applications/MySQL.pm)

Longview's code won't be able to connect to MariaDB using the default `mysql-libs` that provides `libmysqlclient.so.21`. `perl-DBD-MySQL` requires this `libmysqlclient.so.21`, and it's not available if you're using `MariaDB-common` from the [MariaDB repo](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/installing-mariadb/binary-packages/rpm/yum).

If `linode-longview` is ever updated, this will automatically re-patch it to ensure everything works going forward.

### 2. perl-DBD-MySQL-MariaDB-compat

This is intended to fix a dependency hell issue I came across when I already had MariaDB installed from the MariaDB repo, and longview installed from the longview repo.

Basically:

*  `perl-DBD-MySQL` from `appstream` requires `libmysqlclient.so.21`
*  `mysql-libs` from `appstream` requires `mysql-common`
*  `MariaDB-common` from `mariadb` obsoletes `mysql-common`
*  `MariaDB-common` was already installed
*  `MariaDB-common` was required by other packages
*  This resulted in conflicting requests

I couldn't uninstall `perl-DBD-MySQL` without uninstalling `longview`, due to the [forced dependency](https://github.com/linode/longview/blob/master/Extras/specs/centos-longview.spec#L8) in the package (even if you don't run mysql).  
I couldn't update `perl-DBD-MySQL` due to the above dependency hell, so the only easy way I could see to successfully run longview, and easily run `dnf update`, was to either:  
1. Tell the package manager to replace the `perl-DBD-MySQL` package with the `perl-DBD-MariaDB` package, since I wasn't going to require both on my system, or  
1. Forcibly install the updated `perl-DBD-MySQL` package using `rpm`, telling it to ignore dependencies. Then have to deal with each update to the package manually, or add in a different hook / script to check for updates. This seemed like a massive hack, and by far the least preferable of the two.

This rpm tells the package manager to install `perl-DBD-MariaDB` whenever a package requires `perl-DBD-MySQL`, as with this, it obsoletes the MySQL package, and the updated code requires the MariaDB package. You don't then need to worry about dealing with updates in a hacky way, and the MySQL package isn't installed causing issues.


## Using the longview fix without the rpms

Make sure you've got the `perl-DBD-MariaDB` package installed.

You can download the [patch](linode-longview-mariadb-fix/longview.patch), and then deal with any dependency issues yourself

```
curl -o longview.patch https://raw.githubusercontent.com/chappy84/linode-longview-mariadb-patches/refs/heads/master/linode-longview-mariadb-fix/longview.patch
cd /opt/linode/longview 
patch --forward -p1 < /path/to/longview.patch
```
And you can reverse it as-well:

```
cd /opt/linode/longview
patch --reverse -p1 < /path/to/longview.patch
```

There's also the updater that you can link into your package manager.

```
curl -o linode-longview-mariadb-patches-master.tar.gz https://github.com/chappy84/linode-longview-mariadb-patches/tarball/master
tar xfz linode-longview-mariadb-patches-master.tar.gz
mkdir -p /usr/share/linode-longview-mariadb-fix
mv linode-longview-mariadb-fix/longview.patch /usr/share/linode-longview-mariadb-fix/
chmod +x linode-longview-mariadb-fix
./linode-longview-mariadb-fix
```
(if your distro's `datadir` is somewhere different to /usr/share, put the `linode-longview-mariadb-fix` dir containing the `longview.patch` in there instead)

just call the script with `remove` to revert the patch

```
./linode-longview-mariadb-fix remove
```

You can use the `linode-longview-mariadb-fix` script with your package manager to deal with any changes, or fall back on using it manually. For an idea of how to use it with your package manager, see the included [rpm spec](linode-longview-mariadb-fix/rhel-derivatives.spec).

