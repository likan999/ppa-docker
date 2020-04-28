%global with_devel 0
%global with_unit_test 0
%global with_debug 1

# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider_tld com
%global provider github
%global project docker
%global repo %{project}

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}

%define gobuild(o:) go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${GO_LDFLAGS:-} ${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld'" -a -v -x %{?**};

# docker
%global git_docker https://github.com/projectatomic/docker
%global commit_docker 64e9980da375aae15b467ec980bce898541fd356
%global shortcommit_docker %(c=%{commit_docker}; echo ${c:0:7})
# docker_branch used in %%check
%global docker_branch %{name}-%{version}

# d-s-s
%global git_dss https://github.com/projectatomic/container-storage-setup
%global commit_dss 413b4080c0b9346a242d88137bb3e9e0a6aa25f9
%global shortcommit_dss %(c=%{commit_dss}; echo ${c:0:7})
%global dss_libdir %{_exec_prefix}/lib/%{name}-storage-setup

# v1.10-migrator
%global git_migrator https://github.com/%{repo}/v1.10-migrator
%global commit_migrator c417a6a022c5023c111662e8280f885f6ac259be
%global shortcommit_migrator %(c=%{commit_migrator}; echo ${c:0:7})

# docker-novolume-plugin
%global git_novolume https://github.com/projectatomic/%{repo}-novolume-plugin
%global commit_novolume 385ec70baac3ef356f868f391c8d7818140fbd44
%global shortcommit_novolume %(c=%{commit_novolume}; echo ${c:0:7})

# rhel-push-plugin
#%global git_rhel_push https://github.com/projectatomic/rhel-push-plugin
#%global commit_rhel_push af9107b2aedb235338e32a3c19507cad3f218b0d
#%global shortcommit_rhel_push %(c=%{commit_rhel_push}; echo ${c:0:7})

# docker-lvm-plugin
%global git_lvm https://github.com/projectatomic/%{repo}-lvm-plugin
%global commit_lvm 20a1f68da4daecd1f7f59c5b794dd25c2f50ba02
%global shortcommit_lvm %(c=%{commit_lvm}; echo ${c:0:7})

# docker-runc
%global git_runc https://github.com/projectatomic/runc
%global commit_runc 66aedde759f33c190954815fb765eedc1d782dd9
%global shortcommit_runc %(c=%{commit_runc}; echo ${c:0:7})

# docker-containerd
%global git_containerd https://github.com/projectatomic/containerd
%global commit_containerd 9c53e35c39f214b128beed3dfb670ccf751c4173
%global shortcommit_containerd %(c=%{commit_containerd}; echo ${c:0:7})

# docker-init
%global git_tini https://github.com/krallin/tini
%global commit_tini fec3683b971d9c3ef73f284f176672c44b448662
%global shortcommit_tini %(c=%{commit_tini}; echo ${c:0:7})

# docker-proxy
%global git_libnetwork https://github.com/docker/libnetwork
%global commit_libnetwork c5d66a04ae80cd8fa2465ea99c0b2b1a6840cb93
%global shortcommit_libnetwork %(c=%{commit_libnetwork}; echo ${c:0:7})

Name: %{repo}
Epoch: 2
Version: 1.13.1
Release: 161.git%{shortcommit_docker}%{?dist}
Summary: Automates deployment of containerized applications
License: ASL 2.0
URL: https://%{import_path}
ExclusiveArch: aarch64 %{arm} ppc64le s390x x86_64 %{ix86}
Source0: %{git_docker}/archive/%{commit_docker}.tar.gz
Source2: %{git_dss}/archive/%{commit_dss}/container-storage-setup-%{shortcommit_dss}.tar.gz
Source4: %{git_novolume}/archive/%{commit_novolume}/%{repo}-novolume-plugin-%{shortcommit_novolume}.tar.gz
#Source5: %{git_rhel_push}/archive/%{commit_rhel_push}/rhel-push-plugin-%{shortcommit_rhel_push}.tar.gz
Source6: %{git_lvm}/archive/%{commit_lvm}/%{repo}-lvm-plugin-%{shortcommit_lvm}.tar.gz
Source8: %{name}.service
Source9: %{name}.sysconfig
Source10: %{name}-storage.sysconfig
Source11: %{name}-network.sysconfig
Source12: %{name}-logrotate.sh
Source13: README.%{name}-logrotate
Source14: %{name}-common.sh
Source15: README-%{name}-common
Source17: %{git_migrator}/archive/%{commit_migrator}/v1.10-migrator-%{shortcommit_migrator}.tar.gz
Source18: v1.10-migrator-helper
Source19: %{git_runc}/archive/%{commit_runc}/runc-%{shortcommit_runc}.tar.gz
Source20: %{git_containerd}/archive/%{commit_containerd}/containerd-%{shortcommit_containerd}.tar.gz
Source21: %{name}-containerd-common.sh
Source22: %{name}-containerd-shim-common.sh
Source24: %{name}d-common.sh
Source25: %{name}-cleanup.service
Source26: %{name}-cleanup.timer
Source27: daemon.json
Source29: 99-docker.conf
Source30: %{git_tini}/archive/%{commit_tini}/tini-%{shortcommit_tini}.tar.gz
Source31: %{git_libnetwork}/archive/%{commit_libnetwork}/libnetwork-%{shortcommit_libnetwork}.tar.gz
Source32: seccomp.json
# https://bugzilla.redhat.com/show_bug.cgi?id=1636244
Patch0: https://github.com/projectatomic/containerd/pull/11/commits/97eff6cf6c9b58f8239b28be2f080e23c9da62c0.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1653292
Patch1: https://github.com/projectatomic/containerd/pull/12/commits/f9a2eeb64054e740fb1ae3048dde153c257113c8.patch
Patch2: https://github.com/projectatomic/containerd/pull/12/commits/69518f0bbdb1f11113f46a4d794e09e2f21f5e91.patch
# related: https://bugzilla.redhat.com/show_bug.cgi?id=1766665 there is no CollectMode property in RHEL7 systemd
Patch3: docker-collectmode.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1784228
Patch4: bz1784228.patch
Patch5: docker-1792243.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1718441
Patch6: https://patch-diff.githubusercontent.com/raw/projectatomic/runc/pull/30.patch
# https://patch-diff.githubusercontent.com/raw/projectatomic/docker/pull/369.patch
Patch7: docker-CVE-2020-8945.patch
# related bug: https://bugzilla.redhat.com/show_bug.cgi?id=1734482
# patch:       https://github.com/projectatomic/docker/pull/370.patch
#Patch8: docker-1734482.patch
# related bug: https://bugzilla.redhat.com/show_bug.cgi?id=1804024
# patch: https://patch-diff.githubusercontent.com/raw/projectatomic/docker/pull/371.patch
Patch9: docker-1804024.patch
BuildRequires: cmake
BuildRequires: sed
BuildRequires: git
BuildRequires: glibc-static
%if 0%{?fedora}
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
%else
BuildRequires: go-toolset-1.10
BuildRequires: openssl-devel
%endif
BuildRequires: gpgme-devel
BuildRequires: device-mapper-devel
BuildRequires: pkgconfig(audit)
BuildRequires: btrfs-progs-devel
BuildRequires: sqlite-devel
BuildRequires: go-md2man >= 1.0.4
BuildRequires: pkgconfig(systemd)
BuildRequires: libseccomp-devel
BuildRequires: libassuan-devel
%if 0%{?centos}
Requires: subscription-manager-rhsm-certificates
%endif
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: %{name}-client = %{epoch}:%{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Provides: lxc-%{name} = %{epoch}:%{version}-%{release}
Provides: %{name}-io = %{epoch}:%{version}-%{release}

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%if 0%{?with_unit_test}
%package unit-test
Summary: %{summary} - for running unit tests

%description unit-test
%{summary} - for running unit tests
%endif

%package logrotate
Summary: cron job to run logrotate on Docker containers
Requires: %{name} = %{epoch}:%{version}-%{release}
Provides: %{name}-io-logrotate = %{epoch}:%{version}-%{release}

%description logrotate
This package installs %{summary}. logrotate is assumed to be installed on
containers for this to work, failures are silently ignored.

%package v1.10-migrator
License: ASL 2.0 and CC-BY-SA
Summary: Calculates SHA256 checksums for docker layer content

%description v1.10-migrator
Starting from v1.10 docker uses content addressable IDs for the images and
layers instead of using generated ones. This tool calculates SHA256 checksums
for docker layer content, so that they don't need to be recalculated when the
daemon starts for the first time.

The migration usually runs on daemon startup but it can be quite slow(usually
100-200MB/s) and daemon will not be able to accept requests during
that time. You can run this tool instead while the old daemon is still
running and skip checksum calculation on startup.

%package common
Summary: Common files for docker and docker-latest
Requires: device-mapper-libs >= 7:1.02.97
Requires: oci-umount >= 2:2.3.3-3
Requires: oci-register-machine >= 1:0-5.13
Requires: oci-systemd-hook >= 1:0.1.4-9
#Requires: %{name}-rhel-push-plugin = %{epoch}:%{version}-%{release}
Requires: xz
Requires: atomic-registries
Requires: container-selinux >= 2:2.51-1
Requires: container-storage-setup >= 0.9.0-1
# rhbz#1214070 - update deps for d-s-s
Requires: lvm2 >= 2.02.112
Requires: xfsprogs
# rhbz#1282898 - obsolete docker-storage-setup
Obsoletes: %{name}-storage-setup <= 0.0.4-2
Requires: skopeo-containers >= 1:0.1.26-2
Requires: gnupg
Requires: tar

%description common
This package contains the common files %{_bindir}/%{name} which will point to
%{_bindir}/%{name}-current or %{_bindir}/%{name}-latest configurable via
%{_sysconfdir}/sysconfig/%{repo}

%package client
Summary: Client side files for Docker
License: ASL 2.0
Requires: %{repo}-common

%description client
%{summary}

%package novolume-plugin
URL: %{git_novolume}
License: MIT
Summary: Block container starts with local volumes defined
Requires: %{name} = %{epoch}:%{version}-%{release}

%description novolume-plugin
When a volume in provisioned via the `VOLUME` instruction in a Dockerfile or
via `docker run -v volumename`, host's storage space is used. This could lead to
an unexpected out of space issue which could bring down everything.
There are situations where this is not an accepted behavior. PAAS, for
instance, can't allow their users to run their own images without the risk of
filling the entire storage space on a server. One solution to this is to deny users
from running images with volumes. This way the only storage a user gets can be limited
and PAAS can assign quota to it.

This plugin solves this issue by disallowing starting a container with
local volumes defined. In particular, the plugin will block `docker run` with:

- `--volumes-from`
- images that have `VOLUME`(s) defined
- volumes early provisioned with `docker volume` command

The only thing allowed will be just bind mounts.

#%package rhel-push-plugin
#License: GPLv2
#Summary: Avoids pushing a RHEL-based image to docker.io registry

#%description rhel-push-plugin
#In order to use this plugin you must be running at least Docker 1.10 which
#has support for authorization plugins.

#This plugin avoids any RHEL based image to be pushed to the default docker.io
#registry preventing users to violate the RH subscription agreement.

%package lvm-plugin
License: LGPLv3
Summary: Docker volume driver for lvm volumes
Requires: %{name} = %{epoch}:%{version}-%{release}

%description lvm-plugin
Docker Volume Driver for lvm volumes.

This plugin can be used to create lvm volumes of specified size, which can
then be bind mounted into the container using `docker run` command.

%{?enable_gotoolset110}

%prep
%setup -q -n %{name}-%{commit_docker}

# untar d-s-s
tar zxf %{SOURCE2}

# untar novolume-plugin
tar zxf %{SOURCE4}

# untar rhel-push-plugin
#tar zxf %{SOURCE5}

# untar lvm-plugin
tar zxf %{SOURCE6}
sed -i 's/sirupsen/Sirupsen/g' %{name}-lvm-plugin-%{commit_lvm}/Godeps/_workspace/src/%{import_path}/pkg/mount/mount.go

# systemd file
cp %{SOURCE8} .

# sysconfig file
cp %{SOURCE9} .

# storage sysconfig file
cp %{SOURCE10} .

# network sysconfig file
cp %{SOURCE11} .

# logrotate README
cp %{SOURCE13} .

# common exec README
cp %{SOURCE15} .

# untar v1.10-migrator
tar zxf %{SOURCE17}

# untar docker-runc
tar zxf %{SOURCE19}

# untar docker-containerd
tar zxf %{SOURCE20}

# untar docker-init
tar zxf %{SOURCE30}

# untar libnetwork
tar zxf %{SOURCE31}

cd containerd*
%patch0 -p1
%patch1 -p1
%patch2 -p1
cd -
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# https://bugzilla.redhat.com/show_bug.cgi?id=1734482
#%patch8 -p1
%patch9 -p1

%build
# compile docker-proxy first - otherwise deps in gopath conflict with the others below and this fails. Remove libnetwork libs then.
pushd libnetwork-%{commit_libnetwork}
mkdir -p src/github.com/%{repo}/libnetwork
ln -s $(pwd)/* src/github.com/%{repo}/libnetwork
export GOPATH=$(pwd)
export GO_LDFLAGS="-linkmode=external"
%gobuild -o %{repo}-proxy github.com/%{repo}/libnetwork/cmd/proxy
popd

mkdir _build

%global version_tag %{name}-%{version}-%{release}.%{_arch}
%{__sed} -r -i 's/^([\t ]*PkgVersion:[\t ]*)"<unknown>",$/\1"%{version_tag}",/' daemon/info.go
%{__sed} -r -i 's/^([\t ]*PkgVersion:[\t ]*)"<unknown>",$/\1"%{version_tag}",/' cli/command//system/version.go

pushd _build
  mkdir -p src/%{provider}.%{provider_tld}/{%{name},projectatomic}
  ln -s $(dirs +1 -l) src/%{import_path}
  ln -s $(dirs +1 -l)/%{repo}-novolume-plugin-%{commit_novolume} src/%{provider}.%{provider_tld}/projectatomic/%{repo}-novolume-plugin
#  ln -s $(dirs +1 -l)/rhel-push-plugin-%{commit_rhel_push} src/%{provider}.%{provider_tld}/projectatomic/rhel-push-plugin
  ln -s $(dirs +1 -l)/%{repo}-lvm-plugin-%{commit_lvm} src/%{provider}.%{provider_tld}/projectatomic/%{repo}-lvm-plugin
popd

export GOPATH=$(pwd)/%{repo}-novolume-plugin-%{commit_novolume}/Godeps/_workspace:$(pwd)/_build
pushd $(pwd)/_build/src
%gobuild %{provider}.%{provider_tld}/projectatomic/%{repo}-novolume-plugin
popd

#export GOPATH=$(pwd)/rhel-push-plugin-%{commit_rhel_push}/Godeps/_workspace:$(pwd)/_build
#pushd $(pwd)/_build/src
#%gobuild %{provider}.%{provider_tld}/projectatomic/rhel-push-plugin
#popd

export GOPATH=$(pwd)/%{repo}-lvm-plugin-%{commit_lvm}/Godeps/_workspace:$(pwd)/_build
pushd $(pwd)/_build/src
%gobuild %{provider}.%{provider_tld}/projectatomic/%{repo}-lvm-plugin
popd

pushd containerd-%{commit_containerd}
mkdir -p vendor/src/%(dirname github.com/docker/containerd)
ln -s ../../../.. vendor/src/github.com/docker/containerd
export GOPATH=$(pwd)/vendor
%gobuild -o bin/containerd github.com/docker/containerd/containerd
%gobuild -o bin/containerd-shim github.com/docker/containerd/containerd-shim
%gobuild -o bin/ctr github.com/docker/containerd/ctr
popd

export DOCKER_GITCOMMIT="%{shortcommit_docker}/%{version}"
export DOCKER_BUILDTAGS='selinux seccomp'
export GOPATH=$(pwd)/_build:$(pwd)/vendor

# build %%{name} manpages
man/md2man-all.sh
go-md2man -in %{repo}-novolume-plugin-%{commit_novolume}/man/%{repo}-novolume-plugin.8.md -out %{repo}-novolume-plugin.8
#go-md2man -in rhel-push-plugin-%{commit_rhel_push}/man/rhel-push-plugin.8.md -out rhel-push-plugin.8
go-md2man -in %{repo}-lvm-plugin-%{commit_lvm}/man/%{repo}-lvm-plugin.8.md -out %{repo}-lvm-plugin.8

# build %%{name} binary
IAMSTATIC=false DOCKER_DEBUG=1 hack/make.sh dynbinary
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

# build v1.10-migrator
pushd v1.10-migrator-%{commit_migrator}
export GOPATH=$GOPATH:$(pwd)/Godeps/_workspace
sed -i 's/godep //g' Makefile
make v1.10-migrator-local
popd

# build %%{repo}-runc
pushd runc-%{commit_runc}
export RUNC_VERSION=$(cat ./VERSION)
mkdir -p GOPATH
pushd GOPATH
mkdir -p src/%{provider}.%{provider_tld}/opencontainers
ln -s $(dirs +1 -l) src/github.com/opencontainers/runc
popd
 
pushd GOPATH/src/github.com/opencontainers/runc
export GOPATH=$(pwd)/GOPATH:$(pwd)/Godeps/_workspace
export BUILDTAGS='selinux seccomp'
export GO_LDFLAGS="-X main.gitCommit=%{commit_runc} -X main.version=$RUNC_VERSION"
%gobuild -o runc github.com/opencontainers/runc

pushd man
./md2man-all.sh
popd
popd
popd

# build docker-init
pushd tini-%{commit_tini}
cmake .
sed -i 's/#define TINI_GIT     ""/#define TINI_GIT     " - git.%{commit_tini}"/g' tiniConfig.h
make tini-static
popd

%install
# install binary
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libexecdir}/%{repo}

for x in bundles/latest; do
    if ! test -d $x/dynbinary-client; then
        continue
    fi
    rm $x/dynbinary-client/*.{md5,sha256}
    install -p -m 755 $x/dynbinary-client/%{repo}-%{version}* %{buildroot}%{_bindir}/%{name}-current
    break
done

for x in bundles/latest; do
    if ! test -d $x/dynbinary-daemon; then
    continue
    fi
    rm $x/dynbinary-daemon/*.{md5,sha256}
    install -p -m 755 $x/dynbinary-daemon/%{repo}d-* %{buildroot}%{_bindir}/%{repo}d-current
    break
done

# install daemon.json and seccomp.json
install -dp %{buildroot}%{_sysconfdir}/%{name}
install -p -m 644 %{SOURCE32} %{buildroot}%{_sysconfdir}/%{name}

#install docker-proxy
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 libnetwork-%{commit_libnetwork}/%{repo}-proxy %{buildroot}%{_libexecdir}/%{repo}/%{repo}-proxy-current

install -dp %{buildroot}%{_sysconfdir}/%{name}
install -p -m 644 %{SOURCE27} %{buildroot}%{_sysconfdir}/%{name}

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man/man1/* %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 man/man5/* %{buildroot}%{_mandir}/man5
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 man/man8/%{repo}*.8 %{buildroot}%{_mandir}/man8

# install bash completion
install -d %{buildroot}%{_datadir}/bash-completion/completions/
install -p -m 644 contrib/completion/bash/%{name} %{buildroot}%{_datadir}/bash-completion/completions/

# install fish completion
# create, install and own %%{_datadir}/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/fish/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install container logrotate cron script
install -dp %{buildroot}%{_sysconfdir}/cron.daily/
install -p -m 755 %{SOURCE12} %{buildroot}%{_sysconfdir}/cron.daily/%{name}-logrotate

# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/%{name}file.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/%{name}file.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/%{name}file.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_%{name} %{buildroot}%{_datadir}/zsh/site-functions

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p -m 755 contrib/udev/80-%{name}.rules %{buildroot}%{_udevrulesdir}

# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/%{name}

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE8} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE25} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE26} %{buildroot}%{_unitdir}

# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-storage
install -p -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-network

%if 0%{?with_unit_test}
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}-unit-test/
cp -pav VERSION Dockerfile %{buildroot}%{_sharedstatedir}/%{name}-unit-test/.
for d in */ ; do
  cp -a $d %{buildroot}%{_sharedstatedir}/%{name}-unit-test/
done
# remove %%{name}.initd as it requires /sbin/runtime no packages in Fedora
rm -rf %{buildroot}%{_sharedstatedir}/%{name}-unit-test/contrib/init/openrc/%{name}.initd
%endif

# install certs for redhat registries
mkdir -p %{buildroot}/etc/%{name}/certs.d/redhat.{com,io}
mkdir -p %{buildroot}/etc/%{name}/certs.d/registry.access.redhat.com
ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/redhat.com/redhat-ca.crt
ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/redhat.io/redhat-ca.crt
ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/registry.access.redhat.com/redhat-ca.crt

# install container-storage-setup
pushd container-storage-setup-%{commit_dss}
make install-docker DESTDIR=%{buildroot}
popd

# install %%{_bindir}/%%{name}
install -d %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE14} %{buildroot}%{_bindir}/%{name}
install -p -m 755 %{SOURCE24} %{buildroot}%{_bindir}/%{name}d
install -p -m 755 %{SOURCE21} %{buildroot}%{_bindir}/%{name}-containerd
install -p -m 755 %{SOURCE22} %{buildroot}%{_bindir}/%{name}-containerd-shim

# install novolume-plugin executable, unitfile, socket and man
install -d %{buildroot}/%{_libexecdir}/%{repo}
install -p -m 755 _build/src/%{repo}-novolume-plugin %{buildroot}/%{_libexecdir}/%{repo}/%{repo}-novolume-plugin
install -p -m 644 %{repo}-novolume-plugin-%{commit_novolume}/systemd/%{repo}-novolume-plugin.s* %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 %{repo}-novolume-plugin.8 %{buildroot}%{_mandir}/man8

# install rhel-push-plugin executable, unitfile, socket and man
#install -d %{buildroot}%{_libexecdir}/%{repo}
#install -p -m 755 _build/src/rhel-push-plugin %{buildroot}%{_libexecdir}/%{repo}/rhel-push-plugin
#install -p -m 644 rhel-push-plugin-%{commit_rhel_push}/systemd/rhel-push-plugin.service %{buildroot}%{_unitdir}/rhel-push-plugin.service
#install -p -m 644 rhel-push-plugin-%{commit_rhel_push}/systemd/rhel-push-plugin.socket %{buildroot}%{_unitdir}/rhel-push-plugin.socket
#install -d %{buildroot}%{_mandir}/man8
#install -p -m 644 rhel-push-plugin.8 %{buildroot}%{_mandir}/man8

# install %%{repo}-lvm-plugin executable, unitfile, socket and man
install -d %{buildroot}/%{_libexecdir}/%{repo}
install -p -m 755 _build/src/%{repo}-lvm-plugin %{buildroot}/%{_libexecdir}/%{repo}/%{repo}-lvm-plugin
install -p -m 644 %{repo}-lvm-plugin-%{commit_lvm}/systemd/%{repo}-lvm-plugin.s* %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 %{repo}-lvm-plugin.8 %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sysconfdir}/%{repo}
install -p -m 644 %{repo}-lvm-plugin-%{commit_lvm}%{_sysconfdir}/%{repo}/%{repo}-lvm-plugin %{buildroot}%{_sysconfdir}/%{repo}/%{repo}-lvm-plugin

# install v1.10-migrator
install -d %{buildroot}%{_bindir}
install -p -m 700 v1.10-migrator-%{commit_migrator}/v1.10-migrator-local %{buildroot}%{_bindir}/%{name}-v1.10-migrator-local

# install v1.10-migrator-helper
install -p -m 700 %{SOURCE18} %{buildroot}%{_bindir}/%{name}-v1.10-migrator-helper

# install docker-runc
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 runc-%{commit_runc}/runc %{buildroot}%{_libexecdir}/%{repo}/%{repo}-runc-current

#install docker-containerd
install -p -m 755 containerd-%{commit_containerd}/bin/containerd %{buildroot}%{_bindir}/%{repo}-containerd-current
install -p -m 755 containerd-%{commit_containerd}/bin/containerd-shim %{buildroot}%{_bindir}/%{repo}-containerd-shim-current
install -p -m 755 containerd-%{commit_containerd}/bin/ctr %{buildroot}%{_bindir}/%{repo}-ctr-current

#install sysctl knob
install -d -p %{buildroot}%{_usr}/lib/sysctl.d
install -p -m 644 %{SOURCE29} %{buildroot}%{_usr}/lib/sysctl.d

#install tini
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 tini-%{commit_tini}/tini-static %{buildroot}%{_libexecdir}/%{repo}/%{repo}-init-current

%check
[ ! -w /run/%{name}.sock ] || {
    mkdir test_dir
    pushd test_dir
    git clone https://%{provider}.%{provider_tld}/projectatomic/%{repo}.git -b %{docker_branch}
    pushd %{repo}
    make test
    popd
    popd
}

%pre
getent passwd %{name}root > /dev/null || %{_sbindir}/useradd -r -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "Docker User" %{name}root
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%post common
%sysctl_apply 99-%{name}.conf

%post lvm-plugin
%systemd_post %{name}-lvm-plugin.service

%preun lvm-plugin
%systemd_preun %{name}-lvm-plugin.service

%postun lvm-plugin
%systemd_postun_with_restart %{name}-lvm-plugin.service

%post novolume-plugin
%systemd_post %{name}-novolume-plugin.service

%preun novolume-plugin
%systemd_preun %{name}-novolume-plugin.service

%postun novolume-plugin
%systemd_postun_with_restart %{name}-novolume-plugin.service

#%post rhel-push-plugin
#%systemd_post rhel-push-plugin.service

#%preun rhel-push-plugin
#%systemd_preun rhel-push-plugin.service

#%postun rhel-push-plugin
#%systemd_postun_with_restart rhel-push-plugin.service

%posttrans
# Install a default docker-storage-setup based on kernel version.
if [ ! -e %{_sysconfdir}/sysconfig/%{name}-storage-setup ]; then
    # Import /etc/os-release
    . %{_sysconfdir}/os-release || :

    case "$VERSION_ID" in
        7.0 | 7.1 | 7.2 | 7.3 | 7.4)
           echo "STORAGE_DRIVER=devicemapper" >> %{_sysconfdir}/sysconfig/%{name}-storage-setup || :
           echo "CONTAINER_THINPOOL=docker-pool" >> %{_sysconfdir}/sysconfig/%{name}-storage-setup || :
        ;;
    *)
        # 7.5 onwards, switch to overlay2 by default.
        echo "STORAGE_DRIVER=overlay2" >> %{_sysconfdir}/sysconfig/%{name}-storage-setup || :
    ;;
    esac
fi

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE*
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md MAINTAINERS NOTICE README*.md
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/sysconfig/%{name}-storage
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-network
# Use ghost to not package default file installed by "make install-docker".
# Instead we will install a default based on kernel version in %%posttrans.
%ghost %{_sysconfdir}/sysconfig/%{name}-storage-setup
%config(noreplace) %{_sysconfdir}/%{name}/daemon.json
%config(noreplace) %{_sysconfdir}/%{name}/seccomp.json
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}d-current
%{_bindir}/%{name}-storage-setup
%{_bindir}/%{name}-containerd-current
%{_bindir}/%{name}-containerd-shim-current
%{_bindir}/%{name}-ctr-current
%{_sysconfdir}/%{name}/certs.d
%{_mandir}/man1/%{name}*.1.gz
%{_mandir}/man5/*.5.gz
%{_mandir}/man8/%{name}d.8.gz
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-storage-setup.service
%{_datadir}/bash-completion/completions/%{name}
%dir %attr(711, root, root) %{_sharedstatedir}/%{name}
%{_udevrulesdir}/80-%{name}.rules
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/%{name}file.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/%{name}file.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/%{name}file.vim
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{_libexecdir}/%{repo}
%{_libexecdir}/%{repo}/%{repo}-runc-current
%{_libexecdir}/%{repo}/%{repo}-proxy-current
%{_libexecdir}/%{repo}/%{repo}-init-current
%{_unitdir}/%{name}-cleanup.service
%{_unitdir}/%{name}-cleanup.timer
#%%{_unitdir}/%%{repo}-containerd.service

%if 0%{?with_unit_test}
%files unit-test
%{_sharedstatedir}/%{name}-unit-test/
%endif

%files logrotate
%doc README.%{name}-logrotate
%{_sysconfdir}/cron.daily/%{name}-logrotate

%files common
%doc README-%{name}-common
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}d
%{_bindir}/%{name}-containerd
%{_bindir}/%{name}-containerd-shim
%dir %{_libexecdir}/%{repo}
%{_usr}/lib/sysctl.d/99-%{name}.conf

%files client
%license LICENSE*
%{_bindir}/%{name}-current

%files novolume-plugin
%license %{repo}-novolume-plugin-%{commit_novolume}/LICENSE
%doc %{repo}-novolume-plugin-%{commit_novolume}/README.md
%{_mandir}/man8/%{repo}-novolume-plugin.8.gz
%{_libexecdir}/%{repo}/%{repo}-novolume-plugin
%{_unitdir}/%{repo}-novolume-plugin.*

#%files rhel-push-plugin
#%license rhel-push-plugin-%{commit_rhel_push}/LICENSE
#%doc rhel-push-plugin-%{commit_rhel_push}/README.md
#%{_mandir}/man8/rhel-push-plugin.8.gz
#%{_libexecdir}/%{repo}/rhel-push-plugin
#%{_unitdir}/rhel-push-plugin.*

%files lvm-plugin
%license %{repo}-lvm-plugin-%{commit_lvm}/LICENSE
%doc %{repo}-lvm-plugin-%{commit_lvm}/README.md
%config(noreplace) %{_sysconfdir}/%{repo}/%{repo}-lvm-plugin
%{_mandir}/man8/%{repo}-lvm-plugin.8.gz
%{_libexecdir}/%{repo}/%{repo}-lvm-plugin
%{_unitdir}/%{repo}-lvm-plugin.*

%files v1.10-migrator
%license v1.10-migrator-%{commit_migrator}/LICENSE.{code,docs}
%doc v1.10-migrator-%{commit_migrator}/{CONTRIBUTING,README}.md
%{_bindir}/%{name}-v1.10-migrator-*

%changelog
* Tue Mar 03 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-161.git64e9980
- make failure message for CVE-2020-1702 more obvious (#1804024)
- drop patch for #1734482 as it breaks compilation

* Mon Mar 02 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-160.git64e9980
- fix "dockerd leaks SELinux MCS labels" (#1734482)

* Fri Feb 21 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-159.git64e9980
- fix CVE-2020-8945 (#1784838)

* Fri Feb 14 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-158.git64e9980
- add missing patch for #1718441

* Tue Feb 11 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-157.git64e9980
- fix CVE-2020-1702 (#1792796)

* Fri Jan 24 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-156.gitcccb291
- resurrect s390x arch as kernel there now has the renameat2 syscall (#1773504)

* Thu Jan 23 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-155.gitcccb291
- use runc sources off 66aedde7 commit in docker-1.13.1-rhel branch (#1791870)
- use docker sources off cccb291 commit in docker-1.13.1-rhel branch
- do not use CollectMode systemd property in RHEL7

* Mon Jan 20 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-154.git4ef4b30
- Fix thread safety of gpgme (#1792243)

* Thu Jan 16 2020 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-153.git4ef4b30
- temporary disable s390x arch due to #1773504 causing fuse-overlayfs
  failing to build - skopeo/contaners-common requires it

* Mon Dec 23 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-152.git4ef4b30
- patch also local seccomp.json (#1784228)

* Fri Dec 20 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-151.git4ef4b30
- whitelist statx syscall (#1784228)
- remove garbage at the end of if statements in spec
- remove unreferenced bz1784228.patch from dist-git

* Fri Dec 13 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-150.git4ef4b30
- revert fix for #1766665 as RHEL 7 systemd does not have the CollectMode
  property
- bump release to not to clash with RHEL7.7 builds

* Fri Dec 06 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-107.git4ef4b30
- bump version to assure upgrade path

* Thu Dec 05 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-106.git4ef4b30
- fix "libcontainerd: failed to receive event from containerd:" error (#1636244)
- fix "Pods stuck in terminating state with rpc error: code = 2" (#1653292)
- fix "Docker panics when performing `docker search` due to potential
  Search bug when using multiple registries" (#1732626)
- fix race condition in kubelet cgroup destroy process (#1766665)

* Thu Nov 21 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-105.git4ef4b30
- update runc
- Resolves: #1718441

* Tue Sep 24 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-104.git4ef4b30
- Resolves: #1653292, #1741718, #1739315, #1733941
- built docker @projectatomic/docker-1.13.1-rhel commit 4ef4b30

* Fri Aug 02 2019 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-103.git7f2769b
- update RHEL7u7 branch with new version

* Thu Jul 11 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-102.git7f2769b
- Resolves: #1727488, #1723491

* Thu Jul 04 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-101.git61c8524
- Resolves: #1492113, #1653292
- built docker @projectatomic/docker-1.13.1-rhel commit 61c8524
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 9c53e35

* Tue Jun 25 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-100.gite467576
- Resolves: #1714032
- unitfile patch from Ulrich Obergfell <uobergfe@redhat.com>

* Mon Jun 24 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-99.gite467576
- Resolves: #1714722, #1717087 - CVE-2018-15664

* Thu Jun 20 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-98.gitb2f74b2
- Resolves: #1720363
- build -97 wasn't quite right, reverted and skipped from changelogs

* Tue Apr 02 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-96.gitb2f74b2
- Resolves: #1695305
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 9c3c5f8

* Tue Apr 02 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-95.gitb2f74b2
- Resolves: #1587898
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 16883c4

* Tue Feb 26 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-94.gitb2f74b2
- Resolves: #1556901, #1678096 
- built docker-runc @projectatomic/docker-1.13.1-rhel commit df5c38a

* Tue Feb 19 2019 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-93.gitb2f74b2
- rebased containerd to 7989550b83317f799af20ab4df3a5b6487767fc9
- Resolves: #1671861

* Mon Feb 11 2019 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-92.gitb2f74b2
- rebase

* Sat Feb 09 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-91.git07f3374
- Resolves: #1665326 - CVE-2019-5736
 
* Wed Jan 16 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-90.git07f3374
- Resolves: #1662700
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit b968034

* Tue Jan 08 2019 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-89.git07f3374
- Resolves: #1661622 - fix docker-runc build
- use an additional GO_LDFLAGS to keep flags separate from those for tini

* Thu Dec 06 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-88.git07f3374
- Resolves: #1655214 - build with the correct golang deps

* Wed Nov 21 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-87.git07f3374
- buildrequires for centos

* Tue Nov 20 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-86.git07f3374
- build tini without -DMINIMAL

* Thu Nov 15 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-85.git07f3374
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 290a336
- Resolves: #1557426

* Tue Nov 06 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-84.git07f3374
- built docker-containerd commit 923a387

* Tue Nov 06 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-83.git07f3374
- built docker @projectatomic/docker-1.13.1-rhel commit 07f3374
- built container-storage-setup commit 413b408
- built docker-lvm-plugin commit 20a1f68
- built docker-containerd commit 296f1f8
- built docker-init commit fec3683
- built libnetwork commit c5d66a0
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 5eda6f6

* Sun Oct 21 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-82.git9e82212
- Resolves: #1628262
- built docker @projectatomic/docker-1.13.1-rhel commit 9e82212

* Thu Oct 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-81.git8865aaa
- Resolves: #1636244
- built docker @projectatomic/docker-1.13.1-rhel commit 8865aaa

* Tue Oct 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-80.git8633870
- Resolves: #1629733
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 2d876b8

* Tue Oct 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-79.git8633870
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 2d876b8

* Mon Oct 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-78.git8633870
- Resolves: #1592413
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 72e088c

* Mon Oct 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-77.git8633870
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 5382663

* Fri Oct 05 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-76.git8633870
- Resolves: #1629733
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 13b17fe

* Wed Sep 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-75.git8633870
- Resolves: #1625457, #1625022
- built docker @projectatomic/docker-1.13.1-rhel commit 8633870
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 20a1f68
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 5eda6f6
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit c769d58
- built docker-init commit fec3683
- built libnetwork commit a5a6ca3

* Wed Aug 01 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-74.git6e3bb8e
- Resolves: #1603201
- built docker @projectatomic/docker-1.13.1-rhel commit 6e3bb8e
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 20a1f68
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 5eda6f6
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit c769d58
- built docker-init commit fec3683
- built libnetwork commit d00ceed

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-73.git6f36bd4
- enable debuginfo - no idea why it was removed, but that's wrong

* Sun Jul 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-72.git6f36bd4
- Resolves: #1598581, #1598630 - CVE-2018-10892
- built docker @projectatomic/docker-1.13.1-rhel commit 6f36bd4
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 20a1f68
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 5eda6f6
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit c769d58
- built docker-init commit fec3683
- built libnetwork commit d00ceed
- update comment about registries.conf in /etc/sysconfig/docker
  From: Tom Sweeney <tsweeney@redhat.com>  

* Tue Jun 26 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-71.gitdded712
- requires: subscription-manager-rhsm-certificates (centos only)

* Tue Jun 26 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-70.gitdded712
- Resolves: #1595390 - NotifyAccess=main in unitfile

* Tue Jun 19 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-69.gitdded712
- built docker @projectatomic/docker-1.13.1-rhel commit dded712
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 6675634
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 5eda6f6
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit c769d58
- built docker-init commit fec3683
- built libnetwork commit 19279f0

* Tue Jun 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.13.1-68.gitdded712
- built docker @projectatomic/docker-1.13.1-rhel commit dded712
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 6675634
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 5eda6f6
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit fec3683
- built libnetwork commit 19279f0

* Tue Jun 12 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-67.gitdded712
- built docker @projectatomic/docker-1.13.1-rhel commit dded712
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 6675634
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit fec3683
- built libnetwork commit 19279f0

* Mon Jun 11 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-66.gitdded712
- Resolves: #1588773
- built docker @projectatomic/docker-1.13.1-rhel commit dded712
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 6675634
- built docker-runc @projectatomic/docker-1.13.1-rhel commit a9d1096
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit fec3683
- built libnetwork commit 19279f0

* Wed Jun 06 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-65.git6c336e4
- remove outdated comment about docker_transition_unconfined

* Mon Jun 04 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-64.git6c336e4
- built docker @projectatomic/docker-1.13.1-rhel commit 6c336e4
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 04caa55
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 5b117de
- built libnetwork commit 5c1218c

* Mon Apr 30 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-63.git94f4240
- built docker @projectatomic/docker-1.13.1-rhel commit 94f4240

* Tue Apr 10 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-62.gitc6c9b51
- built docker @projectatomic/docker-1.13.1-rhel commit c6c9b51
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 04caa55
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built oci-umount commit 
- built docker-init commit 5b117de
- built libnetwork commit 5c1218c

* Fri Apr 06 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-61.git87f2fab
- do not change commit id for docker at this stage

* Fri Apr 06 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-60.git2d99c6f
- remove dep on subscription-manager-plugin-container

* Mon Mar 26 2018 Daniel J Walsh <dwalsh@redhat.com> - 2:1.13.1-59.git2d99c6f
- built docker @projectatomic/docker-1.13.1-rhel commit 2d99c6f
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built oci-umount commit 
- built docker-init commit 5b117de
- built libnetwork commit 2bf6330

* Mon Mar 19 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-58.git87f2fab
- built docker @projectatomic/docker-1.13.1-rhel commit 87f2fab
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built oci-umount commit 
- built docker-init commit 5b117de
- built libnetwork commit 2bf6330

* Wed Mar 14 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-57.gitaacbc4b
- Resolves: #1489517
- built docker @projectatomic/docker-1.13.1-rhel commit aacbc4b
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 5b117de
- built libnetwork commit 8892d75

* Sat Mar 10 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-56.git774336d
- Resolves: #1485832
- bump deps on container-selinux and oci-umount to the latest shipped

* Tue Feb 20 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-55.rhel75.git774336d
- Re: #1540540
- built docker @projectatomic/docker-1.13.1-rhel commit 774336d
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 5b117de
- built libnetwork commit 14db3c4

* Mon Feb 12 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-54.rhel75.gitce62987
- built docker @projectatomic/docker-1.13.1-rhel commit ce62987
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit e9c345b
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 0effd37
- built libnetwork commit 1ba8194

* Tue Feb 06 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13.1-50.gitec9911e
- Requires: container-storage-setup >= 0.9.0-1

* Tue Feb 06 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-49.gitec9911e
- Resolves: #1441743 - remove MountFlags=slave from unitfile

* Mon Feb 05 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-48.gitec9911e
- Resolves: #1536726 - bump skopeo-containers dependency

* Mon Feb 05 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-47.gitec9911e
- oci-register-machine >= 1:0-5.13 (RE: #1542112)

* Mon Feb 05 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-46.gitec9911e
- Resolves: #1542112 - depend on oci-register-machine (disabled in config file)
- revert removal of oci-register-machine done in 2:1.13.1-1

* Thu Feb 01 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-45.gitec9911e
- c-s-s >= 0.7.0-1

* Thu Feb 01 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-44.gitec9911e
- built docker @projectatomic/docker-1.13.1-rhel commit ec9911e
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 518736e
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 0effd37
- built libnetwork commit 20dd462

* Tue Jan 30 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-43.gitec9911e
- built docker @projectatomic/docker-1.13.1-rhel commit ec9911e
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 518736e
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 0effd37
- built libnetwork commit 20dd462

* Wed Jan 24 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.13.1-1.gitddee18e
- built docker @projectatomic/docker-1.13.1-rhel commit ddee18e
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.13.1-rhel commit 518736e
- built docker-containerd @projectatomic/docker-1.13.1-rhel commit 296f1f8
- built docker-init commit 0effd37
- built libnetwork commit 5ab4ab8

* Wed Dec 13 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.12.6-71.git3e8e77d
- rebased to 3e8e77dcb88db0530c839b249bea7d75f9cd01d7
- https://bugzilla.redhat.com/show_bug.cgi?id=1518519

* Tue Dec 12 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-70.gitec8512b
- Resolves: #1524634 - start daemon after registries.service

* Wed Nov 22 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-69.gitec8512b
- use oci-register-machine >= 1:0-3.14

* Thu Nov 16 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-68.gitec8512b
- revert some docker.sysconfig deletions wrongly done in commit 3b003db

* Thu Nov 09 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-67.gitec8512b
- built docker @projectatomic/docker-1.12.6 commit ec8512b
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit c5d3116
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Thu Nov 09 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-66.gitd6f7b83
- built docker @projectatomic/docker-1.12.6 commit d6f7b83
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit c5d3116
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Tue Nov 07 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-65.git61aa37c
- adjust sources file

* Fri Nov 03 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-64.git61aa37c
- Resolves: #1498553
- built docker @projectatomic/docker-1.12.6 commit 61aa37c
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit c5d3116
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Thu Nov 02 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-63.git6f58874
- built docker @projectatomic/docker-1.12.6 commit 6f58874
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit c5d3116
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Thu Oct 19 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-62.git85d7426
- rhel subscription secrets info moved to skopeo-containers
- require skopeo-containers >= 0.1.24-3

* Tue Sep 26 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-61.git85d7426
- reverted sources, the same file name should not have a different name

* Tue Sep 26 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-60.git85d7426
- Resolves: #1475768
- built docker @projectatomic/docker-1.12.6 commit 85d7426
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit c5d3116
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Fri Sep 22 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.12.6-59.git85d7426
- reverted sources, the same file name should not have a different hash

* Thu Sep 21 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-58.git85d7426
- Resolves: #1455071
- built docker @projectatomic/docker-1.12.6 commit 85d7426
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit c5d3116
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Wed Sep 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-57.git85d7426
- built docker @projectatomic/docker-1.12.6 commit 85d7426
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 31a9f6e
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d

* Mon Sep 18 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-56.git638a809
- built docker @projectatomic/docker-1.12.6 commit 638a809
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 31a9f6e
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit 21c84aa

* Thu Aug 24 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-55.gitc4618fb
- Resolves: #1477787
- built oci-umount commit 6f0317a

* Tue Aug 22 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-54.gitc4618fb
- built oci-umount commit 8377044
- ensure diff between 1.12.6-51 and latest is only container-selinux NVR

* Tue Aug 22 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-53.gitc4618fb
- Resolves: #1484146
- need container-selinux >= 2:2.21-2

* Tue Aug 15 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-52.gitc4618fb
- built docker @projectatomic/docker-1.12.6 commit c4618fb
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 31a9f6e
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit 299e781

* Tue Aug 08 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-51.gitc4618fb
- Resolves: #1472974
- built docker @projectatomic/docker-1.12.6 commit c4618fb
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 31a9f6e
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit 8377044

* Wed Aug 02 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-50.git0fdc778
- Resolves: #1428142, #1454371, #1454420, #1456184, #1470261, #1430905
- Resolves: #1446526, #1450221, #1451474, #1459268, #1461024, #1461071
- Resolves: #1464188, #1466242, #1464933, #1470640
- built docker @projectatomic/docker-1.12.6 commit 0fdc778
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 31a9f6e
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit 8377044

* Tue Jul 25 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.12.6-49.git0fdc778
- changed permissions of /var/lib/docker and /etc/sysconfig/docker-storage, #1473785 

* Thu Jul 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-48.git0fdc778
- built docker @projectatomic/docker-1.12.6 commit 0fdc778
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 79c3939
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit 8377044

* Wed Jul 19 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-47.git0fdc778
- Resolves: #1471218
- built docker @projectatomic/docker-1.12.6 commit 0fdc778
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 79c3939
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit 4f960ae

* Wed Jul 19 2017 fkluknav <fkluknav@redhat.com> - 2:1.12.6-46.git1680dd8
- rebased runc to 79c3939053c870fbb4de5484d98640d5ba028ef4, #1471803

* Wed Jul 12 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-45.git1680dd8
- Resolves: #1467350, #1463824, #1460931, #1446635, #1436731, #1418173
- Resolves: #1413536, #1412881, #1389545, #1366803, #1264971
- add bzs fixed so far ^
- built docker @projectatomic/docker-1.12.6 commit 1680dd8
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit f572169
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d
- built oci-umount commit afbf716

* Tue Jul 11 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-44.gitf55a118
- Resolves: #1454371 - depend on subscription-manager-plugin-container

* Tue Jul 11 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-43.gitf55a118
- built docker @projectatomic/docker-1.12.6 commit 1680dd8
- built oci-umount commit afbf716

* Tue Jul 11 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.12.6-42.1.gitf55a118
- /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt symlink added, #1428142

* Mon Jul 03 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-41.1.gitf55a118
- Resolves: #1468249, #1468244
- record exact commits rebased to in previous build
- built oci-umount commit c134575

* Mon Jul 03 2017 fkluknav <fkluknav@redhat.com> - 2:1.12.6-40.1.gitf55a118
- rebased docker and containerd
- built docker @projectatomic/docker-1.12.6 commit f55a118
- built docker-containerd @projectatomic/docker-1.12.6 commit fa8fb3d 

* Wed Jun 14 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-39.1.git6ffd653
- enable all arches

* Tue Jun 13 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-38.1.git6ffd653
- disable s390x again

* Tue Jun 13 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-37.1.git6ffd653
- enable all arches again

* Tue Jun 13 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-36.1.git6ffd653
- disable s390x temporarily because of indefinite wait time on brew

* Tue Jun 13 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-35.1.git6ffd653
- Resolves: #1460266, #1460326
- built docker @projectatomic/docker-1.12.6 commit 6ffd653
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit f572169
- built docker-containerd @projectatomic/docker-1.12.6 commit d4e2f9d

* Thu Jun 08 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-34.1.git3a6eaeb
- built docker @projectatomic/docker-1.12.6 commit 3a6eaeb
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit af9107b
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit f572169
- built docker-containerd @projectatomic/docker-1.12.6 commit d4e2f9d

* Thu Apr 27 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-18.1.gitc14458a
- Resolves: #1400255 - enable criu
- built docker @projectatomic/docker-1.12.6 commit c14458a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit 70653ed
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 81b2542
- built docker-containerd @projectatomic/docker-1.12.6 commit f3f35e9

* Fri Mar 24 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-17.1
- rebuild for all available arches for 7.4 Extras

* Tue Mar 21 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-16
- require oci-register-machine >= 1:0-3.10

* Mon Mar 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-15
- require: container-selinux >= 2:2.10-2 (RE: #1433223)
- Resolves: #1427332 - container-selinux removal should remove docker as well
- move cleanup unitfiles to docker package
- remove /etc/docker/daemon.json

* Thu Mar 16 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-14
- built docker @projectatomic/docker-1.12.6 commit 3a094bd
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit 70653ed
- built docker-lvm-plugin commit 8647404
- built docker-runc @docker-1.12.6 commit 81b2542
- built docker-containerd @projectatomic/docker-1.12.4 commit 471f03c

* Fri Mar 03 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-13
- move docker-cleanup unitfiles to docker-common

* Thu Mar 02 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-12
- built docker @projectatomic/docker-1.12.6 commit 3a094bd
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit 70653ed
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 81b2542
- built docker-containerd @projectatomic/docker-1.12.4 commit 471f03c

* Thu Feb 23 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-11
- Resolves: #1426290
- built docker @projectatomic/docker-1.12.6 commit 96d83a5

* Tue Feb 21 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-10
- Resolves: #1360892
- From: Luwen Su <lsu@redhat.com>

* Tue Feb 21 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-9
- Resolves: #1420147
- built docker @projectatomic/docker-1.12.6 commit 7f3e2af
- require container-selinux >= 2:2.9-4

* Mon Feb 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-8
- bump to -8 for consistent nvr with docker-latest

* Mon Feb 20 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-7
- require container-selinux >= 2:2.9-3

* Thu Feb 16 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-6
- Resolves: #1415850

* Wed Feb 15 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-5
- Resolves: #1421714
- built docker @projectatomic/docker-1.12.6 commit ddff1c3
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit 70653ed
- built docker-lvm-plugin commit 8647404
- built docker-runc @projectatomic/docker-1.12.6 commit 81b2542
- built docker-containerd @projectatomic/docker-1.12.4 commit 471f03c

* Tue Feb 14 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-4
- Resolves: #1360892 - handle plugin restart
- From: Dan Walsh <dwalsh@redhat.com>

* Mon Feb 13 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-3
- Resolves: #1420591
- requires: container-selinux >= 2:2.9-1

* Tue Feb 07 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-2
- built docker @projectatomic/docker-1.12.6 commit dfc4aea
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit 70653ed
- built docker-lvm-plugin commit 8647404
- built docker-runc commit 81b2542
- built docker-containerd commit 471f03c

* Wed Jan 18 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.6-1
- Resolves: #1413535 - container-selinux should obsolete docker-selinux
- Resolves: #1411980 - honor the --default-runtime flag
- Resolves: #1414250 - /usr/bin/dockerd execs dockerd-[current|latest]
- Resolves: #1414436 - enable --restart=on-failure
- Resolves: #1381929 - update manpages for '--format' example
- built docker @projectatomic/docker-1.12.6 commit 037a2f5
- built container-selinux commit 1169298
- built d-s-s commit f7a3746
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit 8647404
- built docker-runc commit 81b2542
- built docker-containerd commit 471f03c

* Thu Jan 12 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-15
- use oci-systemd-hook >= 1:0.1.4-9

* Wed Jan 11 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-14
- reference correct container-selinux commit id (58209b8)
in 2:1.12.5-13 changelog

* Wed Jan 11 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-13
- Resolves: #1412385 - SELinux issues
- built container-selinux origin/RHEL-1.12 commit 58209b8

* Tue Jan 10 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-12
- relabel docker-latest unitfiles as well

* Tue Jan 10 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-11
- enforce min version-release for oci-register-machine and oci-systemd-hook

* Tue Jan 10 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-10
- Resolves: #1409706 - *CVE-2016-9962* - set init processes as non-dumpable,
runc patch from Michael Crosby <crosbymichael@gmail.com>

* Thu Jan 05 2017 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-9
- Resolves: #1403264 - friendlier error message if no /usr/bin/docker-current
or /usr/bin/docker-latest found.
- Resolves: #1410434 - fix panic on push
- built docker @projectatomic/docker-1.12.5 commit 047e51b
- built container-selinux commit a85092b
- built d-s-s commit 6709fe6
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit 8647404
- built docker-runc commit b8dbc3b
- built docker-containerd commit 471f03c

* Wed Dec 21 2016 Dan Walsh <dwalsh@redhat.com> - 2:1.12.5-8
- Fix handling of container-selinux update and relabel
- Resolves: #1404372, #1395401, #1368092, #1405464, #1400372, #1381929,
- Resolves: #1351609, #1404298, #1368426, #1399398, #1244300, #1374514,
- Resolves: #1400228, #1405306, #1405888, #1403270

* Tue Dec 20 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-7
- remove DOCKER_PROXY_BINARY env var

* Tue Dec 20 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-6
- version-release consistent with docker-latest

* Tue Dec 20 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-5
- Resolves: #1406460 - add --userland-proxy-path option to unitfile
- Resolves: #1406446 - add --signature-verification=false to $OPTIONS in
/etc/sysconfig/docker

* Mon Dec 19 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-4
- Resolves: #1405989
- From: Jan Pazdziora <jpazdziora@redhat.com>

* Fri Dec 16 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-3
- built docker @projectatomic/docker-1.12.5 commit 6009905
- built container-selinux commit a85092b
- built d-s-s commit b7175b4
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 471f03c

* Fri Dec 16 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-2
- built docker @projectatomic/docker-1.12.5 commit 6009905
- built container-selinux commit a85092b
- built d-s-s commit b7175b4
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 471f03c

* Fri Dec 16 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.5-1
- built docker @projectatomic/docker-1.12.5 commit 6009905
- built container-selinux commit a85092b
- built d-s-s commit b7175b4
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 471f03c

* Tue Dec 13 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.4-3
- docker requires docker-client

* Tue Dec 13 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.4-2
- built docker @projectatomic/docker-1.12.4 commit 1b5971a
- built container-selinux commit cc14935
- built d-s-s commit 0d53efa
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 471f03c

* Tue Dec 13 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.4-1
- Resolves: #1403264 - packaging fixes (from runcom@redhat.com)
- Resolves: #1403843 - disable any existing gear modules (from
dwalsh@redhat.com)
- built docker @projectatomic/docker-1.12.4 commit 1b5971a
- built container-selinux commit cc14935
- built d-s-s commit 0d53efa
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 471f03c

* Mon Dec 12 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.3-11
- Resolves: #1403370 - fix relabeling of /usr/bin/docker*
- built docker @projectatomic/docker-1.12.3 commit 0423d89
- built container-selinux commit 554f844
- built d-s-s commit 0d53efa
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 9f45393

* Thu Dec 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.3-10
- move docker-proxy to /usr/libexec/docker/
- append '-current' to files inside /usr/libexec/docker/

* Wed Dec 07 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.12.3-9
- Resolves: #1402677 - create a docker-client subpackage
- built docker @projectatomic/docker-1.12.3 commit 3abc089
- built container-selinux commit bdad20c
- built d-s-s commit 0d53efa
- built v1.10-migrator commit c417a6a
- built docker-novolume-plugin commit 385ec70
- built rhel-push-plugin commit eb9e6be
- built docker-lvm-plugin commit d918081
- built docker-runc commit b8dbc3b
- built docker-containerd commit 9f45393

* Sat Nov 19 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.10.3-59
- correct typo

* Fri Nov 18 2016 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.10.3-58
- Resolves: #1382997 - correctly remove docker-selinux policies when the
subpackage is removed, remove docker policy if it is installed at 100, 200 or
400 levels
- Resolves: #1346206 - do not override DOCKER_CERT_PATH if it's already set
- Resolves: #1389328, #1393443 - rhel-push-plugin fixes
- bump Epoch to 2, since the recent 1.12.3 was already on Epoch: 1
- move docker-selinux to container-selinux   
- built rhel-push-plugin commit eb9e6be
- built container-selinux origin/RHEL-1.12 commit 98617f3
- built dss commit 0d53efa

* Thu Oct 20 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-57
- Resolves: #1385641 - additional policy rules for RHEL rpms

* Tue Oct 18 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-56
- Resolves: #1380474
- built docker projectatomic/rhel7-1.10.3 commit 30bf0b8

* Mon Sep 19 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-55
- Resolves: #1376950, #1376953
- built docker-novolume-plugin commit c521254
- built rhel-push-plugin commit d89861d

* Mon Sep 12 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-54
- Resolves: #1374265
- built commit 25e0f0e

* Wed Sep 07 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-53
- Resolves: #1373952 - typebounds can't be used in rhel yet
- re-add v1.10-migrator
- built docker-selinux commit 583a67f
- built v1.10-migrator commit c417a6a

* Tue Sep 06 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-52
- Resolves: #1370935 - fs_rw_nsfs_files broken in selinux-policy, included in
docker-selinux
- built docker-selinux commit 3d17c3f

* Tue Sep 06 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-51
- Resolves: #1370935 - remove label for kubelet directory from docker-selinux
- Resolves: #1357121 - install cron job to cleanup dead containers
- Resolves: #1303123, #1330141, #1336857, #1346185, #1353626, #1355783,
- Resolves: #1362611, #1370935
- built docker projectatomic/rhel7-1.10.3 commit ef55c88
- built docker-selinux commit edbbfc9
- built docker-lvm-plugin commit bc03b53
- built d-s-s commit 95194cb

* Wed Aug 31 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-50
- built docker-selinux commit 45be230

* Fri Aug 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-49
- built docker-selinux commit dba8e03
- update oci-* dependency NVRs

* Tue Aug 16 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-48
- built docker projectatomic/rhel7-1.10.3 commit f9d4a2c
- built docker-selinux commit 69140d6
- built d-s-s commit 338cf62
- built rhel-push-plugin commit 4eaaf33
- built docker-lvm-plugin commit 532c7ad

* Thu Jun 23 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-47
- 46.x release tag used for 7.2.6, use 47 and up for 7.3

* Thu Jun 23 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-45
- built docker-selinux commit 7419650
- use selinux-policy >= 3.13.1-64 [rhel-7.3]

* Fri Jun 17 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-44
- Resolves: #1311544 (bz added, no other change since -43)

* Fri Jun 17 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-43
- add MountFlags=slave to unitfile

* Mon Jun 13 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-42
- Resolves: #1344448
- built rhel-push-plugin commit 1a0046f

* Mon Jun 13 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-41
- Resolves: #1341171 - docker should require oci-register-machine and oci-systemd-hook
- Resolves: #1342274 - docker doesn't own /etc/docker/docker-lvm-plugin

* Thu Jun 09 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-40
- bump release tag to make it consistent with docker-latest
 
* Thu Jun 09 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-39
- bump release tag to make it consistent with docker-latest

* Thu Jun 09 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-38
- built docker projectatomic/rhel7-1.10.3 commit a46c31a
- fixes a panic

* Wed Jun 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-37
- migrator doesn't require docker at runtime either
- From: Jonathan Lebon <jlebon@redhat.com>

* Wed Jun 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-36
- Do not run migrator script via %%triggerin
- If the docker daemon is already running prior, the new daemon will be
restarted which will handle migration
- Remove migrator subpackage from docker runtime deps
- From: Jonathan Lebon <jlebon@redhat.com>

* Wed Jun 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-35
- Resolves: #1338894, #1324150, #1343702, #1339146, #1304808, #1286787,
#1323819, #1283891, #1339164, #1328917, #1317096,
#1318690, #1309900, #1245325
- same as previous build, bugs referenced

* Tue Jun 07 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-34
- Patch0 in previous build has been merged in projectatomic/docker rhel7-1.10.3 branch
- built docker projectatomic/rhel7-1.10.3 commit 6baafd8
- define docker_branch macro to be used in %%check

* Tue Jun 07 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-33
- Patch0 used in previous build updated

* Mon Jun 06 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-32
- Resolves: #1341906 - use RWMutex to acces container store

* Thu Jun 02 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-31
- Resolves: #1342274 - update file listings to avoid file ownerships by
multiple subpackages
- update docker.sysconfig to include --log-driver=journald in OPTIONS

* Thu Jun 02 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-30
- Resolves: #1342149 - v1.10-migrator shipped separately in both docker and
docker-latest
- The v1.10-migrator subpackage in docker-latest has executables prepended 
with 'docker-latest-', while there's no change in the ones shipped with 
docker (RE: #1342149)

* Thu Jun 02 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-29
- Resolves: #1342149 - docker-v1.10-migrator obsoletes
docker-latest-v1.10-migrator

* Wed Jun 01 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-28
- Resolves: #1341789 - update unitfile to use systemd for cgroups

* Wed Jun 01 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-27
- Resolves: #1341328 - include v1.10-migrator-helper script in the migrator
subpackage
- Resolves: #1335635 - solve log spam issues
- built docker projectatomic/rhel7-1.10.3 commit 4779225
- built dss commit 194eca2

* Sat May 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-26
- Resolves: #1341171 - add oci-register-machine and oci-systemd-hook subpackages
- built oci-register-machine commit 7d4ce65
- built oci-systemd-hook commit 41491a3

* Sat May 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-25
- docker requires docker-rhel-push-plugin

* Sat May 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-24
- docker unitfile updates to include rhel-push-plugin

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-23
- bump release tag to obsolete packages in docker-latest

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-1
- Resolves: #1335597 - rebase to v1.10.3 + rh patches
- add subpackages for novolume-plugin, lvm-plugin, rhel-push-plugin, v1.10-migrator
- BR: libseccomp-devel
- built docker @projectatomic/rhel7-1.10.3 commit 86bbf84
- built docker-selinux @origin/rhel7-1.10 commit 032bcda
- built d-s-s commit df2af94
- built forward-journald commit 77e02a9
- built novolume-plugin commit 7715854
- built rhel-push-plugin commit 904c0ca
- built lvm-plugin commit 3253f53
- built v1.10-migrator commit c417a6a

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-40
- Resolves: #1332592 - requires docker-common = version-release
- From: Ed Santiago <santiago@redhat.com>

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-39
- Resolves: #1332016, #1329743
- built docker projectatomic/rhel7-1.9 commit ab77bde
- built docker-selinux origin/rhel-1.10 commit 032bcda

* Wed Apr 27 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-38
- Resolves: #1331007 - fix selinux labels for new docker execs names
- built docker-selinux commit#501ea4c

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-37
- Resolves: #1330622 - /usr/bin/docker handles docker/docker-latest
conditions
- Resolves: #1330290 - d-s-s: do not pass devices which have 'creation of
device node' in progress
- built d-s-s commit#df2af94

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-36
- Resolves: #1330622 - don't allow $DOCKERBINARY==/usr/bin/docker

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-35
- #1330595 fix From: Ed Santiago <santiago@redhat.com>

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-34
- Resolves: #1330595
- use correct exec path for docker-current in unitfile

* Mon Apr 25 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-33
- Resolves: #1328219 - include docker-common subpackage
- docker-common is a runtime requirement for both docker and docker-latest

* Thu Apr 21 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-32
- update upstream URL
- Resolves: #1329423 - skip /dev setup in container when it's bind mounted in
- Resolves: #1329452 - CVE-2016-3697
- built docker @projectatomic/rhel7-1.9 commit#639e055
- built docker-selinux commit#39c092c
- built d-s-s commit#04a3847
- built forward-journald commit#77e02a9

* Thu Apr 21 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-31
- test-fix for https://github.com/openshift/openshift-ansible/issues/1779

* Mon Apr 18 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-30
- Bump release - previous git log had 2 docker commit values
- built docker @projectatomic/rhel7-1.9 commit#a1c9058
- built docker-selinux commit#39c092c
- built d-s-s commit#04a3847
- built forward-journald commit#77e02a9

* Mon Apr 18 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-29
- Resolves: #1283718, #1277982, #1126555 #1134424, #1186066,
    #1228777, #1255060, #1256832, #1261565, #1264562, #1266307,
    #1266525 #1266902 #1268059 #1272143 #1277982 #1283718 #1300033,
    #1303110 #1309739 #1316651 #1319783
- remove conflicts with atomic-openshift and origin
- built docker @projectatomic/rhel7-1.9 commit#a1c9058
- built docker-selinux commit#39c092c
- built d-s-s commit#04a3847
- built forward-journald commit#77e02a9
- do not even build dockerinit

* Sun Apr 10 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-28
- built docker @projectatomic/rhel7-1.9 commit#b795b73
- built docker-selinux commit#39c092c
- built d-s-s commit#ac50cee
- built docker-utils commit#b851c03
- built v1.10-migrator commit#c417a6a
- built forward-journald commit#77e02a9

* Sun Apr 10 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-27
- split docker-utils into a subpackage so docker-latest can reuse it.
- docker requires docker-utils at runtime
- do not ship dockerinit
- spec cleanups

* Mon Apr 04 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-26
- Resolves: rhbz#1323819 - allow images with VOLUME(s) when binds destination
override volume definition
- built docker @projectatomic/rhel7-1.9 commit#b795b73
- built docker-selinux commit#e72d8d7
- built d-s-s commit#346018e
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Wed Mar 23 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-25
- Resolves: rhbz#1320302 - Backport fix for --cgroup-parent in docker
- same commits as release -24, only added bug number

* Wed Mar 23 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-24
- built docker @projectatomic/rhel7-1.9 commit#78ee77d
- built docker-selinux commit#8718b62
- built d-s-s commit#c6f0553
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Thu Mar 17 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-23
- Resolves: rhbz#1318360 - delete bounds checking rules
- built docker @projectatomic/rhel7-1.9 commit#f97fb16
- built docker-selinux commit#8718b62
- built d-s-s commit#c6f0553
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Tue Mar 15 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-22
- Resolves: rhbz#1317991 - Set Delegate=yes for cgroup transient units
- built docker @projectatomic/rhel7-1.9 commit#f97fb16
- built docker-selinux commit#69be4dc
- built d-s-s commit#03dfc7b
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Mon Mar 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-21
- Resolves: rhbz#1317662 - include manpage for docker daemon (corrected)

* Mon Mar 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-20
- Resolves: rhbz#1317662 - include manpage for docker run
- Resolves: rhbz#1317627 - ensure that we join all the cgroups
- built docker @projectatomic/rhel7-1.9 commit#0275914
- built docker-selinux commit#69be4dc
- built d-s-s commit#03dfc7b
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Wed Mar 09 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-19
- Resolves: rhbz#1316190 - set NotifyAccess=all in unitfile

* Tue Mar 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-18
- Resolves: rhbz#1286765 - set TimeoutStartSec=0 in unitfile
- Resolves: rhbz#1298363, rhbz#1300076, rhbz#1304038, rhbz#1302418
- built forward-journald commit#77e02a9 - other subpackage commits same as
previous build

* Tue Mar 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-17
- built docker @projectatomic/rhel7-1.9 commit#185277d
- built docker-selinux commit#e2e1f22
- built d-s-s commit#03dfc7b
- built docker-utils commit#b851c03
- built forward-journald commit#48b9599

* Tue Feb 02 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-16
- Resolves: rhbz#1304038 - conflict with openshift 3.1
- allow golang >= 1.4.2

* Thu Jan 28 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-15
- Resolves: rhbz#1302411
- built docker @projectatomic/rhel7-1.9 commit#50e78a0
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Tue Jan 26 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-14
- built docker @projectatomic/rhel7-1.9 commit#fe0b590
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Mon Jan 25 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-13
- Resolves: rhbz#1301199 - do not append distro tag to docker version

* Wed Jan 20 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-12
- built docker @projectatomic/rhel7-1.9 commit#2dbcc37
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Fri Jan 15 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-11
- built docker @projectatomic/rhel7-1.9 commit#2dbcc37
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Mon Jan 11 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-10
- built docker @projectatomic/rhel7-1.9 commit#26797f7
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Sat Dec 12 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-9
- built docker @projectatomic/rhel7-1.9 commit#401dfee
- built docker-selinux commit#e2e1f22
- built d-s-s commit#91d6cfd
- built docker-utils commit#dab51ac

* Fri Dec 04 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-8
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#441f312
- built d-s-s commit#e38b94d
- built docker-utils commit#dab51ac

* Wed Dec 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-7
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#441f312
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Wed Dec 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-6
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#441f312
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Mon Nov 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-5
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Wed Nov 25 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-4
- Resolves: rhbz#1275399
- built docker @projectatomic/rhel7-1.9 commit#390a466
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-3
- built docker @projectatomic/rhel7-1.9 commit#698d463
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-2
- Resolves: rhbz#1263394 - set unitfile to 5 mins

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-1
- use correct version number, no other change since last build

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-11
- built docker @projectatomic/rhel7-1.9 commit#f1cda67
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Mon Nov 23 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-10
- Resolves: rhbz#1283718
- built docker @projectatomic/rhel7-1.9 commit#0ba2491
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Thu Nov 19 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-9
- built docker @projectatomic/rhel7-1.9 commit#eb84909
- built docker-selinux commit#dbfad05
- built d-s-s commit#c638a60
- built docker-utils commit#dab51ac

* Wed Nov 11 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-10
- Resolves: rhbz#1281805, rhbz#1271229, rhbz#1276346
- Resolves: rhbz#1275376, rhbz#1282898

* Wed Nov 11 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-9
- Resolves: rhbz#1280068 - Build docker with DWARF
- Move back to 1.8.2
- built docker @rhatdan/rhel7-1.8 commit#a01dc02
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Mon Nov 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-8
- Resolves: rhbz#1225093 (partially)
- built docker @projectatomic/rhel7-1.9 commit#cdd3941
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Wed Oct 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-7
- Resolves: rhbz#1275554
- built docker @projectatomic/rhel7-1.9 commit#61fd965
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Wed Oct 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-6
- built docker @projectatomic/rhel7-1.9 commit#166d43b
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Mon Oct 26 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-5
- built docker @projectatomic/rhel7-1.9 commit#6897d78
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Fri Oct 23 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-4
- built docker @projectatomic/rhel7-1.9 commit#0bb2bf4
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Thu Oct 22 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-3
- built docker @projectatomic/rhel7-1.9 commit#1ea7f30
- built docker-selinux commit#dbfad05
- built d-s-s commit#01df512
- built docker-utils commit#dab51ac

* Thu Oct 22 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-2
- built docker @projectatomic/rhel7-1.9 commit#1ea7f30
- built docker-selinux commit#fe61432
- built d-s-s commit#01df512
- built docker-utils commit#dab51ac

* Wed Oct 14 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-8
- built docker @rhatdan/rhel7-1.8 commit#a01dc02
- built docker-selinux master commit#e2a5226
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac

* Fri Oct 09 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-7
- https://github.com/rhatdan/docker/pull/127 (changes for libcontainer/user)
- https://github.com/rhatdan/docker/pull/128 (/dev mount from host)

* Wed Oct 07 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-6
- built docker @rhatdan/rhel7-1.8 commit#bb472f0
- built docker-selinux master commit#44abd21
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac

* Wed Sep 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-5
- Resolves: rhbz#1267743
- https://github.com/docker/docker/pull/16639
- https://github.com/opencontainers/runc/commit/c9d58506297ed6c86c9d8a91d861e4de3772e699

* Wed Sep 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-4
- built docker @rhatdan/rhel7-1.8 commit#23f26d9
- built docker-selinux master commit#2ed73eb
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac

* Wed Sep 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-3
- Resolves: rhbz#1264557 (extras-rhel-7.1.6) - rebase to 1.8.2
- Resolves: rhbz#1265810 (extras-rhel-7.2) - rebase to 1.8.2
- built docker @rhatdan/rhel7-1.8 commit#23f26d9
- built docker-selinux master commit#d6560f8
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac
- use golang == 1.4.2

* Mon Sep 21 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.8.2-2
- built docker-selinux master commit#d6560f8

* Fri Sep 18 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.8.2-1
- package only provides docker, docker-selinux and docker-logrotate
- Resolves: rhbz#1261329, rhbz#1263394, rhbz#1264090
- built docker @rhatdan/rhel7-1.8 commit#23f26d9
- built d-s-s master commit#6898d43
- built docker-selinux master commit#b5281b7
- built docker-utils master commit#dab51ac

* Thu Aug 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-115
- Resolves: rhbz#1252421
- built docker @rhatdan/rhel7-1.7 commit#446ad9b
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#d3b9ba7
- built atomic master commit#011a826
- built docker-selinux master commit#6267b83
- built docker-utils master commit#dab51ac

* Mon Aug 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-114
- Resolves: rhbz#1255874 - (#1255488 is for 7.2)

* Fri Aug 21 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-113
- Resolves: rhbz#1255488
- built docker @rhatdan/rhel7-1.7 commit#4136d06
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#d3b9ba7
- built atomic master commit#995a223
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Thu Aug 20 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-112
- Resolves: rhbz#1255051
- built docker @rhatdan/rhel7-1.7 commit#4136d06
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#ac1b30e
- built atomic master commit#53169d5
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Tue Aug 18 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-111
- built docker @rhatdan/rhel7-1.7 commit#9fe211a
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#ac1b30e
- built atomic master commit#53169d5
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Mon Aug 17 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-110
- built docker @rhatdan/rhel7-1.7 commit#ba2de95
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#ac1b30e
- built atomic master commit#53169d5
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Mon Aug 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-109
- Resolves: rhbz#1249651 - unpin python-requests requirement
- update python-websocket-client to 0.32.0

* Tue Jul 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-108
- built docker @rhatdan/rhel7-1.7 commit#3043001
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#a4442c4
- built docker-selinux master commit#bebf349
- built docker-utils master commit#dab51ac

* Fri Jul 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-107
- built docker @rhatdan/rhel7-1.7 commit#3043001
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#52d695c
- built docker-selinux master commit#bebf349

* Thu Jul 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-106
- built docker @rhatdan/rhel7-1.7 commit#3043001
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#52d695c
- built docker-selinux master commit#bebf349

* Thu Jul 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-105
- Resolves: rhbz#1245325
- built docker @rhatdan/rhel7-1.7 commit#ac162a3
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#ac162a3
- built docker-selinux master commit#ac162a3
- disable dockerfetch and dockertarsum

* Wed Jul 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-104
- use a common release tag for all subpackages, much easier to update via
rpmdev-bumpspec

* Wed Jul 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-1
- built docker @rhatdan/rhel7-1.7 commit#d2fbc0b
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#d2fbc0b
- built docker-selinux master commit#d2fbc0b

* Fri Jul 17 2015 Jonathan Lebon <jlebon@redhat.com> - 1.7.0-5
- Add patch for atomic.sysconfig
- Related: https://github.com/projectatomic/atomic/pull/94

* Wed Jul 15 2015 Jan Chaloupka <jchaloup@redhat.com> - 1.7.0-3.1
- Add unit-test subpackage

* Thu Jul 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.0-3
- built docker @rhatdan/rhel7-1.7 commit#4740812

* Wed Jul 08 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.0-2
- increment all release tags to make koji happy

* Wed Jul 08 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.0-1
- Resolves: rhbz#1241186 - rebase to v1.7.0 + rh patches
- built docker @rhatdan/rhel7-1.7 commit#0f235fc
- built docker-selinux master commit#bebf349
- built d-s-s master commit#e9c3a4c
- built atomic master commit#f133684
- rebase python-docker-py to upstream v1.2.3
- disable docker-fetch for now, doesn't build

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-14
- Resolves: rhbz#1218639, rhbz#1225556 (unresolved in -11)
- build docker @lsm5/rhel7-1.6 commit#ba1f6c3

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-13
- Resolves: rhbz#1222453

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-12
- build docker-selinux master commit#9c089c6

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-11
- Resolves: rhbz#1231936 (clone of fedora rhbz#1231134), rhbz#1225556, rhbz#1215819
- build docker @rhatdan/rhel7-1.6 commit#7b32c6c

* Wed Jun 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-10
- correct typo

* Wed Jun 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-9
- Resolves: rhbz#1214070 - update d-s-s related deps
- Resolves: rhbz#1229374 - use prior existing metadata volume if any
- Resolves: rhbz#1230192 (include d-s-s master commit#eefbef7)
- build docker @rhatdan/rhel7-1.6 commit#b79465d

* Mon Jun 08 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-8
- Resolves: rhbz#1229319 - do not claim /run/secrets
- Resolves: rhbz#1228167
- build docker rhatdan/rhel7-1.6 commit#ac7d43f
- build atomic master commit#f863afd

* Thu Jun 04 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-7
- Resolves: rhbz#1228397 - install manpage for d-s-s
- Resolves: rhbz#1228459 - solve 'Permission denied' error for d-s-s
- Resolves: rhbz#1228685 - don't append dist tag to docker version
(revert change in 1.6.2-4)

* Tue Jun 02 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-6
- build docker rhatdan/rhel7-1.6 commit#f1561f6

* Tue Jun 02 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-5
- build docker-selinux master commit#99c4c77
- build atomic master commit#2f1398c
- include docker-storage-setup in docker itself, no subpackage created
- docker.service Wants=docker-storage-setup.service

* Mon Jun 01 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-4
- include dist tag in 'docker version' to tell a distro build from a docker
upstream rpm

* Mon Jun 01 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-3
- Resolves: rhbz#1226989 - correct install path for docker-stroage-setup
config file
- Resolves: rhbz#1227040 - docker requires docker-storage-setup at runtime
- built docker @rhatdan/rhel7-1.6 commit#a615a49
- built atomic master commit#2f1398c
- built d-s-s master commit#0f2b772

* Thu May 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-2
- build docker @rhatdan/rhel7-1.6 commit#175dd9c

* Thu May 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-1
- Resolves: rhbz#1225965 - rebase to 1.6.2
- Resolves: rhbz#1226320, rhbz#1225549, rhbz#1225556
- Resolves: rhbz#1219705 - CVE-2015-3627
- Resolves: rhbz#1219701 - CVE-2015-3629
- Resolves: rhbz#1219709 - CVE-2015-3630
- Resolves: rhbz#1219713 - CVE-2015-3631
- build docker @rhatdan/rhel7-1.6 commit#d8675b5
- build atomic master commit#ec592be
- build docker-selinux master commit#e86b2bc

* Tue May 26 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-15
- d-s-s br: pkgconfig(systemd)
- Resolves: rhbz#1214070 enforce min NVR for lvm2

* Tue May 26 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-14
- build atomic master commit#cc9aed4
- build docker-utils master commit#562e2c0
- build docker-selinux master commit#ba1ff3c
- include docker-storage-setup subpackage, use master commit#e075395
- Resolves: rhbz#1216095

* Mon May 25 2015 Michal Minar <miminar@redhat.com> - 1.6.0-13
- Remove all repositories when removing image by ID.
- Resolves: #1222784

* Thu Apr 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-11
- build docker @rhatdan/rhel7-1.6 commit#8aae715
- build atomic @projectatomic/master commit#5b2fa8d (fixes a typo)
- Resolves: rhbz#1207839
- Resolves: rhbz#1211765
- Resolves: rhbz#1209545 (fixed in 1.6.0-10)
- Resolves: rhbz#1151167 (fixed in 1.6.0-6)

* Tue Apr 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-10
- Resolves: rhbz#1215768
- Resolves: rhbz#1212579
- build docker @rhatdan/rhel7-1.6 commit#0852937

* Fri Apr 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-9
- build docker @rhatdan/rhel7-1.6 commit#6a57386
- fix registry unit test

* Wed Apr 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-8
- build docker @rhatdan/rhel7-1.6 commit#7bd2216

* Tue Apr 21 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-7
- build docker @rhatdan/rhel7-1.6 commit#c3721ce
- build atomic master commit#7b136161
- Resolves: rhbz#1213636

* Fri Apr 17 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-6
- Rebuilt with golang 1.4.2
- Resolves: rhbz#1212813

* Fri Apr 17 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-5
- build docker @rhatdan/rhel7-1.6 commit#9c42d44
- build docker-selinux master commit#d59539b
- Resolves: rhbz#1211750

* Thu Apr 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-4
- build docker @rhatdan/rhel7-1.6 commit#c1a573c
- includes 1.6.0 release + redhat patches
- include docker-selinux @fedora-cloud/master commit#d74079c

* Thu Apr 16 2015 Michal Minar <miminar@redhat.com> - 1.6.0-3
- Fixed login command
- Resolves: rhbz#1212188

* Wed Apr 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-2
- Resolves: rhbz#1211292 - move GOTRACEBACK=crash to unitfile
- build docker @rhatdan/rhel7-1.6 commit#fed6da1
- build atomic master commit#e5734c4

* Tue Apr 14 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-1
- use docker @rhatdan/rhel7-1.6 commit#a8ccea4

* Fri Apr 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-30
- use docker @rhatdan/1.6 commit#24bc1b9

* Fri Mar 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-29
- use docker @rhatdan/1.6 commit#2d06cf9

* Fri Mar 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-28
- Resolves: rhbz#1206443 - CVE-2015-1843

* Wed Mar 25 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-27
- revert rhatdan/docker commit 72a9000fcfa2ec5a2c4a29fb62a17c34e6dd186f
- Resolves: rhbz#1205276

* Tue Mar 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-26
- revert rhatdan/docker commit 74310f16deb3d66444bb461c29a09966170367db

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-25
- don't delete autogen in hack/make.sh
- re-enable docker-fetch

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-24
- bump release tags for all

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-23
- Resolves: rhbz#1204260 - do not delete linkgraph.db before starting service

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-22
- increment release tag (no other changes)

* Sun Mar 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-21
- install cert for redhat.io authentication

* Mon Mar 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-20
- Resolves: rhbz#1202517 - fd leak
- build docker rhatdan/1.5.0 commit#ad5a92a
- build atomic master commit#4ff7dbd

* Tue Mar 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-19
- Resolves: rhbz#1200394 - don't mount /run as tmpfs if mounted as a volume
- Resolves: rhbz#1187603 - 'atomic run' no longer ignores new image if
container still exists
- build docker rhatdan/1.5.0 commit#5992901
- no rpm change, ensure release tags in changelogs are consistent

* Tue Mar 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-18
- handle updates smoothly from a unified docker-python to split out
docker-python and atomic

* Tue Mar 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-17
- build docker @rhatdan/1.5.0 commit#d7dfe82
- Resolves: rhbz#1198599 - use homedir from /etc/passwd if $HOME isn't set
- atomic provided in a separate subpackage

* Mon Mar 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-16
- build docker @rhatdan/1.5.0 commit#867ff5e
- build atomic master commit#
- Resolves: rhbz#1194445 - patch docker-python to make it work with older
python-requests
- Resolves: rhbz#1200104 - dns resolution works with selinux enforced

* Mon Mar 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-15
- Resolves: rhbz#1199433 - correct install path for 80-docker.rules

* Mon Mar 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-14
- build docker, @rhatdan/1.5.0 commit#365cf68
- build atomic, master commit#f175fb6

* Fri Mar 06 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-13
- build docker, @rhatdan/1.5.0 commit#e0fdceb
- build atomic, master commit#ef2b661

* Thu Mar 05 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-12
- Resolves: rhbz#1198630
- build docker, @rhatdan/1.5.0 commit#233dc3e
- build atomic, master commit#c6390c7

* Tue Mar 03 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-11
- build docker rhatdan/1.5.0 commit#3a4d0f1
- build atomic master commit#d68d76b
- Resolves: rhbz#1188252 - rm /var/lib/docker/linkgraph.db in unit file
before starting docker daemon

* Mon Mar 02 2015 Michal Minar <miminar@redhat.com> - 1.5.0-10
- Fixed and speeded up repository searching

* Fri Feb 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-9
- increment all release tags

* Fri Feb 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-9
- increment docker release tag

* Thu Feb 26 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-7
- Resolves: rhbz#1196709 - fix docker build's authentication issue
- Resolves: rhbz#1197158 - fix ADD_REGISTRY and BLOCK_REGISTRY in unitfile
- Build docker-utils commit#dcb4518
- update docker-python to 1.0.0
- disable docker-fetch (not compiling currently)

* Tue Feb 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-6
- build docker rhatdan/1.5.0 commit#e5d3e08
- docker registers machine with systemd
- create journal directory so that journal on host can see journal content in
container
- build atomic commit#a7ff4cb

* Mon Feb 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-5
- use docker rhatdan/1.5.0 commit#1a4e592
- Complete fix for rhbz#1192171 - patch included in docker tarball
- use docker-python 0.7.2
- Resolves: rhbz#1192312 - solve version-release requirements for
subpackages

* Mon Feb 16 2015 Michal Minar <miminar@redhat.com> - 1.5.0-4
- Readded --(add|block)-registry flags.

* Fri Feb 13 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-2
- Resolves: rhbz#1192312 - custom release numbers for 
python-websocket-client and docker-py
- Resolves: rhbz#1192171 - changed options and env vars for
adding/replacing registries

* Thu Feb 12 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-1
- build docker rhatdan/1.5 a06d357
- build atomic projectaomic/master d8c35ce

* Thu Feb 05 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-39
- Resolves: rhbz#1187993 - allow core dump with no size limit
- build atomic commit#98c21fd

* Mon Feb 02 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-38
- Resolves: rhbz#1188318
- atom commit#ea7ab31

* Fri Jan 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-37
- add extra options to /etc/sysconfig/docker to add/block registries
- build atom commit#3d4fd20

* Fri Jan 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-36
- remove dependency on python-backports

* Fri Jan 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-35
- build atomic rhatdan/master commit#973142b
- build docker rhatdan/1.4.1-beta2 commit#d26b358

* Fri Jan 30 2015 Michal Minar <miminar@redhat.com> - 1.4.1-34
- added patch fixed tagging issue

* Fri Jan 30 2015 Michal Minar <miminar@redhat.com> - 1.4.1-33
- build docker rhatdan/1.4.1-beta2 commit#b024f0f
- --registry-(replace|preprend) replaced with --(add|block)-registry

* Thu Jan 29 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-32
- build atom commit#567c2c8

* Thu Jan 29 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-31
- build atom commit#b9e02ad

* Wed Jan 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-30
- Require python-backports >= 1.0-8 for docker-python

* Wed Jan 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-29
- build docker rhatdan/1.4.1-beta2 commit#0af307b
- --registry-replace|prepend flags via Michal Minar <miminar@redhat.com>
- build atomic rhatdan/master commit#37f9be0

* Tue Jan 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-27
- patch to avoid crash in atomic host

* Tue Jan 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-26
- build docker rhatdan/1.4.1-beta2 commit#0b4cade
- build atomic rhatdan/master commit#b8c7b9d
- build docker-utils vbatts/master commit#fb94a28

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-25
- build atomic commit#fcbc57b with fix for install/upgrade/status
- build docker rhatdan/1.4.1-beta2 commit#f476836

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-24
- install dockertarsum from github.com/vbatts/docker-utils

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-23
- build rhatdan/atom commit#ef16d40
- try urlparse from six, else from argparse

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-22
- use python-argparse to provide urlparse

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-21
- move atomic bits into -python subpackage

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-20
- update atom commit#10fc4c8

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-19
- build rhatdan/1.4.1-beta2 commit#35a8dc5
- --registry-prepend instead of --registry-append

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-18
- don't install nsinit

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-17
- install atomic and manpages
- don't provide -devel subpackage

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-16
- install python-websocket-client and python-docker as subpackages

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-15
- build rhatdan/1.4.1-beta2 commit#06670da
- install subscription manager

* Tue Jan 20 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-14
- increment release number to avoid conflict with 7.0

* Tue Jan 20 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-13
- build rhatdan/1.4.1-beta2 commit#2de8e5d
- Resolves: rhbz#1180718 - MountFlags=slave in unitfile

* Mon Jan 19 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-12
- build rhatdan/1.4.1-beta2 commit#218805f

* Mon Jan 19 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-11
- build rhatdan/1.4.1-beta2 commit#4b7addf

* Fri Jan 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-10
- build rhatdan/1.4.1-beta2 commit #a0c7884
- socket activation not used
- include docker_transition_unconfined boolean info and disable socket
activation in /etc/sysconfig/docker
- docker group not created

* Fri Jan 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-9
- run all tests and not just unit tests
- replace codegansta.tgz with codegangsta-cli.patch

* Thu Jan 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-8
- build rhatdan/1.4.1-beta2 commit #6ee2421

* Wed Jan 14 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-7
- build rhatdan/1.4.1-beta2 01a64e011da131869b42be8b2f11f540fd4b8f33
- run tests inside a docker repo during check phase

* Mon Jan 12 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-6
- build rhatdan/1.4.1-beta2 01a64e011da131869b42be8b2f11f540fd4b8f33

* Wed Jan 07 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-5
- own /etc/docker
- include check for unit tests

* Fri Dec 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-4
- Install vim and shell completion files in main package itself

* Thu Dec 18 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-3
- rename cron script
- change enable/disable to true/false

* Thu Dec 18 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-2
- Enable the logrotate cron job by default, disable via sysconfig variable
- Install docker-network and docker-container-logrotate sysconfig files

* Thu Dec 18 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-1
- Resolves: rhbz#1174351 - update to 1.4.1
- Provide subpackages for fish and zsh completion and vim syntax highlighting
- Provide subpackage to run logrotate on running containers as a daily cron
job

* Mon Dec 15 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.0-1
- Resolves: rhbz#1174266 - update to 1.4.0
- Fixes: CVE-2014-9357, CVE-2014-9358
- uses /etc/docker as cert path
- create dockerroot user
- skip btrfs version check

* Fri Dec 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-4
- update libcontainer paths
- update docker.sysconfig to include DOCKER_TMPDIR
- update docker.service unitfile
- package provides docker-io-devel

* Mon Dec 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-3
- revert docker.service change, -H fd:// in sysconfig file

* Mon Dec 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-2
- update systemd files

* Tue Nov 25 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-1
- Resolves: rhbz#1167870 - update to v1.3.2
- Fixes CVE-2014-6407, CVE-2014-6408

* Fri Nov 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.1-2
- remove unused buildrequires

* Thu Nov 13 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.1-1
- bump to upstream v1.3.1
- patch to vendor in go-md2man and deps for manpage generation

* Thu Oct 30 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.8
- Remove docker-rhel entitlment patch. This was buggy and is no longer needed

* Mon Oct 20 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.7
- Add 404 patch to allow docker to continue to try to download updates with 
- different certs, even if the registry returns 404 error

* Tue Oct 7 2014 Eric Paris <eparis@redhat.com> - 1.2.0-1.6
- make docker.socket start/restart when docker starts/restarts

* Tue Sep 30 2014 Eric Paris <eparis@redhat.com> - 1.2.0-1.5
- put docker.socket back the right way

* Sat Sep 27 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.4
- Remove docker.socket

* Mon Sep 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.2
- Fix docker.service file to use /etc/sysconfig/docker-storage.service

* Mon Sep 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.1
- Bump release to 1.2.0
- Add support for /etc/sysconfig/docker-storage
- Add Provides:golang(github.com/docker/libcontainer)
- Add provides docker-io to get through compatibility issues
- Update man pages
- Add missing pieces of libcontainer
- Devel now obsoletes golang-github-docker-libcontainer-devel
- Remove runtime dependency on golang
- Fix secrets patch
- Add -devel -pkg-devel subpackages
- Move libcontainer from -lib to -devel subpackage
- Allow docker to use /etc/pki/entitlement for certs
- New sources that satisfy nsinit deps
- Change docker client certs links
- Add nsinit

* Tue Sep 2 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-10
- Add  docker client entitlement certs

* Fri Aug 8 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-9
- Add Matt Heon patch to allow containers to work if machine is not entitled

* Thu Aug 7 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-8
- Fix handing of rhel repos

* Mon Aug 4 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-6
- Update man pages

* Mon Jul 28 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-5
- Fix environment patch
- Add /etc/machine-id patch

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-4
- Add Secrets Patch back in

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-3
- Pull in latest docker-1.1.2 code

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-2
- Update to the latest from upstream
- Add comment and envoroment patches to allow setting of comments and 
- enviroment variables from docker import

* Wed Jul 23 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-3
- Install docker bash completions in proper location
- Add audit_write as a default capability

* Tue Jul 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-2
- Update man pages
- Fix docker pull registry/repo

* Fri Jul 18 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-1
- Update to latest from upstream

* Mon Jul 14 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-10
- Pass otions from /etc/sysconfig/docker into docker.service unit file

* Thu Jul 10 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-9
- Fix docker-registry patch to handle search

* Thu Jul 10 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-8
- Re-add %%{_datadir}/rhel/secrets/rhel7.repo

* Wed Jul 9 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-7
- Patch: Save "COMMENT" field in Dockerfile into image content.
- Patch: Update documentation noting that SIGCHLD is not proxied.
- Patch: Escape control and nonprintable characters in docker ps
- Patch: machine-id: add container id access
- Patch: Report child error better (and later)
- Patch: Fix invalid fd race
- Patch: Super minimal host based secrets
- Patch: libcontainer: Mount cgroups in the container
- Patch: pkg/cgroups Add GetMounts() and GetAllSubsystems()
- Patch: New implementation of /run support
- Patch: Error if Docker daemon starts with BTRFS graph driver and SELinux enabled
- Patch: Updated CLI documentation for docker pull with notes on specifying URL
- Patch: Updated docker pull manpage to reflect ability to specify URL of registry.
- Patch: Docker should use /var/tmp for large temporary files.
- Patch: Add --registry-append and --registry-replace qualifier to docker daemon
- Patch: Increase size of buffer for signals
- Patch: Update documentation noting that SIGCHLD is not proxied.
- Patch: Escape control and nonprintable characters in docker ps

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-4
- Documentation update for --sig-proxy
- increase size of buffer for signals
- escape control and nonprintable characters in docker ps

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-3
- Resolves: rhbz#1111769 - CVE-2014-3499

* Thu Jun 19 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-2
- Resolves: rhbz#1109938 - upgrade to upstream version 1.0.0 + patches
  use repo: https://github.com/lsm5/docker/commits/htb2
- Resolves: rhbz#1109858 - fix race condition with secrets
- add machine-id patch:
https://github.com/vbatts/docker/commit/4f51757a50349bbbd2282953aaa3fc0e9a989741

* Wed Jun 18 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1
- Resolves: rhbz#1109938 - upgrade to upstream version 1.0.0 + patches
  use repo: https://github.com/lsm5/docker/commits/2014-06-18-htb2
- Resolves: rhbz#1110876 - secrets changes required for subscription
management
- btrfs now available (remove old comment)

* Fri Jun 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-19
- build with golang-github-kr-pty-0-0.19.git98c7b80.el7

* Fri Jun 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-18
- update manpages
- use branch: https://github.com/lsm5/docker/commits/2014-06-06-2

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-17
- use branch: https://github.com/lsm5/docker/commits/2014-06-05-final2

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-16
- latest repo: https://github.com/lsm5/docker/commits/2014-06-05-5
- update secrets symlinks

* Mon Jun 02 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-15
- correct the rhel7.repo symlink

* Mon Jun 02 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-14
- only symlink the repo itself, not the dir

* Sun Jun 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-13
- use the repo dir itself and not repo for second symlink

* Sat May 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-12
- create symlinks at install time and not in scriptlets
- own symlinks in /etc/docker/secrets

* Sat May 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-11
- add symlinks for sharing host entitlements

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-10
- /etc/docker/secrets has permissions 750

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-9
- create and own /etc/docker/secrets

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-8
- don't use docker.sysconfig meant for sysvinit (just to avoid confusion)

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-7
- install /etc/sysconfig/docker for additional args
- use branch 2014-05-29 with modified secrets dir path

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-6
- secret store patch

* Thu May 22 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-5
- native driver: add required capabilities (dotcloud issue #5928)

* Thu May 22 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-4
- branch 2014-05-22
- rename rhel-dockerfiles dir to dockerfiles

* Wed May 21 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-3
- mount /run with correct selinux label

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-2
- add btrfs

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-1
- use latest master
- branch: https://github.com/lsm5/docker/commits/2014-05-09-2

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-13
- add registry search list patch

* Wed May 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-12
- include dockerfiles for postgres, systemd/{httpd,mariadb}

* Mon May 12 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-11
- add apache, mariadb and mongodb dockerfiles
- branch 2014-05-12

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-10
- add rhel-dockerfile/mongodb

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-9
- use branch: https://github.com/lsm5/docker/commits/2014-05-09
- install rhel-dockerfile for apache
- cleanup: get rid of conditionals
- libcontainer: create dirs/files as needed for bind mounts

* Thu May 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-8
- fix docker top

* Tue May 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-7
- set container pid for process in native driver

* Tue May 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-6
- ensure upstream PR #5529 is included

* Mon May 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-5
- block push to docker index

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-4
- enable selinux in unitfile

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-3
- branch https://github.com/lsm5/docker/commits/2014-05-01-2

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-2
- branch https://github.com/lsm5/docker/tree/2014-05-01

* Fri Apr 25 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-1
- renamed (docker-io -> docker)
- rebased on 0.10.0
- branch used: https://github.com/lsm5/docker/tree/2014-04-25
- manpages packaged separately (pandoc not available on RHEL-7)

* Tue Apr 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-4.collider
- manpages merged, some more patches from alex

* Thu Apr 03 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-3.collider
- fix --volumes-from mount failure, include docker-images/info/tag manpages

* Tue Apr 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-2.collider
- solve deadlock issue

* Mon Mar 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-1.collider
- branch 2014-03-28, include additional docker manpages from whenry

* Thu Mar 27 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-7.collider
- env file support (vbatts)

* Mon Mar 17 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-6.collider
- dwalsh's selinux patch rewritten
- point to my docker repo as source0 (contains all patches already)
- don't require tar and libcgroup

* Fri Mar 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-5.collider
- add kraman's container-pid.patch

* Fri Mar 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-4.collider
- require docker.socket in unitfile

* Thu Mar 13 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-3.collider
- use systemd socket activation

* Wed Mar 12 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-2.collider
- add collider tag to release field

* Tue Mar 11 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-1
- upstream version bump to 0.9.0

* Mon Mar 10 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-3
- add alexl's patches upto af9bb2e3d37fcddd5e041d6ae45055f649e2fbd4
- add guelfey/go.dbus to BR

* Sun Mar 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-2
- use upstream commit 3ace9512bdf5c935a716ee1851d3e636e7962fac
- add dwalsh's patches for selinux, emacs-gitignore, listen_pid and
remount /var/lib/docker as --private

* Wed Feb 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-1
- Bug 1066841 - upstream version bump to v0.8.1
- use sysvinit files from upstream contrib
- BR golang >= 1.2-7

* Thu Feb 13 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.8.0-3
- Remove unneeded sysctl settings in initscript
  https://github.com/dotcloud/docker/pull/4125

* Sat Feb 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-2
- ignore btrfs for rhel7 and clones for now
- include vim syntax highlighting from contrib/syntax/vim

* Wed Feb 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-1
- upstream version bump
- don't use btrfs for rhel6 and clones (yet)

* Mon Jan 20 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-2
- bridge-utils only for rhel < 7
- discard freespace when image is removed

* Thu Jan 16 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-1
- upstream version bump v0.7.6
- built with golang >= 1.2

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.5-1
- upstream version bump to 0.7.5

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.4-1
- upstream version bump to 0.7.4 (BZ #1049793)
- udev rules file from upstream contrib
- unit file firewalld not used, description changes

* Mon Jan 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-3
- udev rules typo fixed (BZ 1048775)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-2
- missed commit value in release 1, updated now
- upstream release monitoring (BZ 1048441)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-1
- upstream release bump to v0.7.3

* Thu Dec 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-2
- require xz to work with ubuntu images (BZ #1045220)

* Wed Dec 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-1
- upstream release bump to v0.7.2

* Fri Dec 06 2013 Vincent Batts <vbatts@redhat.com> - 0.7.1-1
- upstream release of v0.7.1

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-14
- sysvinit patch corrected (epel only)
- 80-docker.rules unified for udisks1 and udisks2

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-13
- removed firewall-cmd --add-masquerade

* Sat Nov 30 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-12
- systemd for fedora >= 18
- firewalld in unit file changed from Requires to Wants
- firewall-cmd --add-masquerade after docker daemon start in unit file
  (Michal Fojtik <mfojtik@redhat.com>), continue if not present (Michael Young
  <m.a.young@durham.ac.uk>)
- 80-docker.rules included for epel too, ENV variables need to be changed for
  udisks1

* Fri Nov 29 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-11
- Redirect docker log to /var/log/docker (epel only)
- Removed the '-b none' parameter from sysconfig, it's unnecessary since
  we create the bridge now automatically (epel only)
- Make sure we have the cgconfig service started before we start docker,
    RHBZ#1034919 (epel only)

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-10
- udev rules added for fedora >= 19 BZ 1034095
- epel testing pending

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-9
- requires and started after firewalld

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-8
- iptables-fix patch corrected

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-7
- use upstream tarball and patch with mgoldman's commit

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-6
- using mgoldman's shortcommit value 0ff9bc1 for package (BZ #1033606)
- https://github.com/dotcloud/docker/pull/2907

* Wed Nov 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7.0-5
- Fix up EL6 preun/postun to not fail on postun scripts

* Wed Nov 27 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-4
- brctl patch for rhel <= 7

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-3
- Patch how the bridge network is set up on RHEL (BZ #1035436)

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-2
- add libcgroup require (BZ #1034919)

* Tue Nov 26 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-1
- Upstream release 0.7.0
- Using upstream script to build the binary

* Mon Nov 25 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.20.rc7
- correct the build time defines (bz#1026545). Thanks dan-fedora.

* Fri Nov 22 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7-0.19.rc7
- Remove xinetd entry, added sysvinit

* Fri Nov 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.18.rc7
- rc version bump

* Wed Nov 20 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.17.rc6
- removed ExecStartPost lines from docker.service (BZ #1026045)
- dockerinit listed in files

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.16.rc6
- adding back the none bridge patch

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.15.rc6
- update docker source to crosbymichael/0.7.0-rc6
- bridge-patch is not needed on this branch

* Tue Nov 19 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.14.rc5
- update docker source to crosbymichael/0.7-rc5
- update docker source to 457375ea370a2da0df301d35b1aaa8f5964dabfe
- static magic
- place dockerinit in a libexec
- add sqlite dependency

* Sat Nov 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.13.dm
- docker.service file sets iptables rules to allow container networking, this
    is a stopgap approach, relevant pull request here:
    https://github.com/dotcloud/docker/pull/2527

* Sat Oct 26 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.12.dm
- dm branch
- dockerinit -> docker-init

* Tue Oct 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.11.rc4
- passing version information for docker build BZ #1017186

* Sat Oct 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.10.rc4
- rc version bump
- docker-init -> dockerinit
- zsh completion script installed to /usr/share/zsh/site-functions

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.9.rc3
- lxc-docker version matches package version

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.8.rc3
- double quotes removed from buildrequires as per existing golang rules

* Fri Oct 11 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.7.rc3
- xinetd file renamed to docker.xinetd for clarity

* Thu Oct 10 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.6.rc3
- patched for el6 to use sphinx-1.0-build

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.5.rc3
- rc3 version bump
- exclusivearch x86_64

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.4.rc2
- debuginfo not Go-ready yet, skipped

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.3.rc2
- debuginfo package generated
- buildrequires listed with versions where needed
- conditionals changed to reflect systemd or not
- docker commit value not needed
- versioned provides lxc-docker

* Mon Oct 07 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-2.rc2
- rc branch includes devmapper
- el6 BZ #1015865 fix included

* Sun Oct 06 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-1
- version bump, includes devicemapper
- epel conditionals included
- buildrequires sqlite-devel

* Fri Oct 04 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-4.devicemapper
- docker-io service enables IPv4 and IPv6 forwarding
- docker user not needed
- golang not supported on ppc64, docker-io excluded too

* Thu Oct 03 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-3.devicemapper
- Docker rebuilt with latest kr/pty, first run issue solved

* Fri Sep 27 2013 Marek Goldmann <mgoldman@redhat.com> - 0.6.3-2.devicemapper
- Remove setfcap from lxc.cap.drop to make setxattr() calls working in the
  containers, RHBZ#1012952

* Thu Sep 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.3-1.devicemapper
- version bump
- new version solves docker push issues

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-14.devicemapper
- package requires lxc

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-13.devicemapper
- package requires tar

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-12.devicemapper
- /var/lib/docker installed
- package also provides lxc-docker

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-11.devicemapper
- better looking url

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-10.devicemapper
- release tag changed to denote devicemapper patch

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-9
- device-mapper-devel is a buildrequires for alex's code
- docker.service listed as a separate source file

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-8
- install bash completion
- use -v for go build to show progress

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-7
- build and install separate docker-init

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-4
- update to use new source-only golang lib packages

* Sat Sep 21 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-3
- man page generation from docs/.
- systemd service file created
- dotcloud/tar no longer required

* Fri Sep 20 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-2
- patched with alex larsson's devmapper code

* Wed Sep 18 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-1
- Version bump

* Tue Sep 10 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-2
- buildrequires updated
- package renamed to docker-io
 
* Fri Aug 30 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-1
- Version bump
- Package name change from lxc-docker to docker
- Makefile patched from 0.5.3

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-5
- File permissions settings included

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-4
- Credits in changelog modified as per reference's request

* Tue Aug 27 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-3
- Dependencies listed as rpm packages instead of tars
- Install section added

* Mon Aug 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-2
- Github packaging
- Deps not downloaded at build time courtesy Elan Ruusamäe
- Manpage and other docs installed

* Fri Aug 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-1
- Initial fedora package
- Some credit to Elan Ruusamäe (glen@pld-linux.org)
