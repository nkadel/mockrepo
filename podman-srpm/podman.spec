%global with_check 0

%define gobuild(o:) \
GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -linkmode=external -compressdwarf=false -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v %{?**};

%global import_path github.com/containers/podman
%global branch v4.6.1-rhel
%global commit0 ea33dce70f1b9d6f60faa405f57ed791a89cd751
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global cataver 0.1.7
#%%global dnsnamever 1.3.0
%global commit_dnsname 18822f9a4fb35d1349eb256f4cd2bfd372474d84
%global shortcommit_dnsname %(c=%{commit_dnsname}; echo ${c:0:7})
%global gvproxyrepo gvisor-tap-vsock
%global gvproxyver 0.6.1
%global commit_gvproxy 407efb5dcdb0f4445935f7360535800b60447544

Epoch: 2
Name: podman
Version: 4.6.1
#Release: 5%%{?dist}
Release: 0.5%{?dist}
Summary: Manage Pods, Containers and Container Images
License: Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0
URL: https://%{name}.io/
%if 0%{?branch:1}
Source0: https://%{import_path}/tarball/%{commit0}/%{branch}-%{shortcommit0}.tar.gz
%else
Source0: https://%{import_path}/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
%endif
Source1: https://github.com/openSUSE/catatonit/archive/v%{cataver}.tar.gz
#Source2: https://github.com/containers/dnsname/archive/v%%{dnsnamever}.tar.gz
Source2: https://github.com/containers/dnsname/archive/%{commit_dnsname}/dnsname-%{shortcommit_dnsname}.tar.gz
Source4: https://github.com/containers/gvisor-tap-vsock/archive/%{commit_gvproxy}/gvisor-tap-vsock-%{commit_gvproxy}.tar.gz
# https://fedoraproject.org/wiki/PackagingDrafts/Go#Go_Language_Architectures
ExclusiveArch: %{go_arches}
Provides: %{name}-manpages = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-manpages < %{epoch}:%{version}-%{release}
Provides: %{name}-catatonit = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-catatonit < 2:4.4.0
BuildRequires: gettext
BuildRequires: golang >= 1.17.5
BuildRequires: glib2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: git-core
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: libgpg-error-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: ostree-devel
BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires: shadow-utils-subid-devel
# these BRs are for catatonit
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: file
BuildRequires: gcc
BuildRequires: libtool
Requires: containers-common >= 2:1-27
Suggests: containernetworking-plugins >= 0.9.1-1
Requires: netavark
Requires: iptables
Requires: nftables
Obsoletes: oci-systemd-hook < 1
Requires: libseccomp >= 2.5
Requires: conmon >= 2.0.25
Requires: (container-selinux if selinux-policy)
Requires: slirp4netns >= 0.4.0-1
Recommends: crun
Requires: fuse-overlayfs
Requires: oci-runtime
Provides: podmansh = %{epoch}:%{version}-%{release}
Provides: podman-podmansh = %{epoch}:%{version}-%{release}
Provides: podman-shell = %{epoch}:%{version}-%{release}

%description
%{name} (Pod Manager) is a fully featured container engine that is a simple
daemonless tool.  %{name} provides a Docker-CLI comparable command line that
eases the transition from other container engines and allows the management of
pods, containers and images.  Simply put: alias docker=%{name}.
Most %{name} commands can be run as a regular user, without requiring
additional privileges.

%{name} uses Buildah(1) internally to create container images.
Both tools share image (not container) storage, hence each can use or
manipulate images (but not containers) created by the other.

%{summary}
%{name} Simple management tool for pods, containers and images

%package docker
Summary: Emulate Docker CLI using %{name}
BuildArch: noarch
Requires: %{name} = %{epoch}:%{version}-%{release}
Provides: docker = %{epoch}:%{version}-%{release}

%description docker
This package installs a script named docker that emulates the Docker CLI by
executes %{name} commands, it also creates links between all Docker CLI man
pages and %{name}.

%package remote
Summary: A remote CLI for Podman: A Simple management tool for pods, containers and images

%description remote
%{name}-remote provides a local client interacting with a Podman backend
node through a RESTful API tunneled through a ssh connection. In this context,
a %{name} node is a Linux system with Podman installed on it and the API
service activated.

Credentials for this session can be passed in using flags, environment
variables, or in containers.conf.

%package plugins
Summary: Plugins for %{name}
Requires: dnsmasq
Recommends: %{name}-gvproxy = %{epoch}:%{version}-%{release}

%description plugins
This plugin sets up the use of dnsmasq on a given CNI network so
that Pods can resolve each other by name.  When configured,
the pod and its IP address are added to a network specific hosts file
that dnsmasq will read in.  Similarly, when a pod
is removed from the network, it will remove the entry from the hosts
file.  Each CNI network will have its own dnsmasq instance.

%package tests
Summary: Tests for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
#Requires: bats  (which RHEL8 doesn't have. If it ever does, un-comment this)
Requires: nmap-ncat
Requires: httpd-tools
Requires: jq
Requires: socat
Requires: skopeo
Requires: openssl
Requires: buildah
Requires: gnupg
Requires: git-daemon

%description tests
%{summary}

This package contains system tests for %{name}

%package gvproxy
Summary: Go replacement for libslirp and VPNKit

%description gvproxy
A replacement for libslirp and VPNKit, written in pure Go.
It is based on the network stack of gVisor. Compared to libslirp,
gvisor-tap-vsock brings a configurable DNS server and
dynamic port forwarding.

%prep
%if 0%{?branch:1}
%autosetup -Sgit -n containers-%{name}-%{shortcommit0}
%else
%autosetup -Sgit -n %{name}-%{commit0}
%endif
sed -i 's;@@PODMAN@@\;$(BINDIR);@@PODMAN@@\;%{_bindir};' Makefile
sed -i 's,-Werror,,' pkg/rootless/rootless_linux.go
tar fx %{SOURCE1}
pushd catatonit-%{cataver}
sed -i '$d' configure.ac
popd
tar fx %{SOURCE2}
tar fx %{SOURCE4}

# this is shipped by skopeo: containers-common subpackage
rm -rf docs/source/markdown/containers-mounts.conf.5.md

%build
# build catatonit first because C code
pushd catatonit-%{cataver}
autoreconf -fi
%configure
CFLAGS="%{optflags} -fPIE -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
%{__make} %{?_smp_mflags}
# Make sure we *always* build a static binary for catatonit. Otherwise we'll break containers
# that don't have the necessary shared libs.
file catatonit | grep 'statically linked'
if [ $? != 0 ]; then
   echo "ERROR: catatonit binary must be statically linked!"
   exit 1
fi
popd

export GO111MODULE=on
export GOPATH=$(pwd)/_build:$(pwd)
CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
# These extra flags present in $CFLAGS have been skipped for now as they break the build
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-flto=auto//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-Wp,D_GLIBCXX_ASSERTIONS//g')
CGO_CFLAGS=$(echo $CGO_CFLAGS | sed 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//g')

%ifarch x86_64
export CGO_CFLAGS+=" -m64 -mtune=generic -fcf-protection=full"
%endif

mkdir _build
pushd _build
mkdir -p src/github.com/containers
ln -s ../../../../ src/github.com/containers/podman
popd
ln -s vendor src

rm -rf vendor/github.com/containers/storage/drivers/register/register_btrfs.go

unset LDFLAGS
# build date. FIXME: Makefile uses '/v2/libpod', that doesn't work here?
LDFLAGS="-X %{import_path}/libpod/define.buildInfo=$(date +%s)"

# build rootlessport
%gobuild -o bin/rootlessport %{import_path}/cmd/rootlessport

export BUILDTAGS="seccomp btrfs_noversion exclude_graphdriver_devicemapper exclude_graphdriver_btrfs $(hack/libdm_tag.sh) $(hack/selinux_tag.sh) $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh)"
%gobuild -o bin/%{name} %{import_path}/cmd/%{name}

# build %%{name}-remote
export BUILDTAGS="remote $BUILDTAGS"
%gobuild -o bin/%{name}-remote %{import_path}/cmd/%{name}

# build quadlet
%gobuild -o bin/quadlet %{import_path}/cmd/quadlet

%{__make} docs
%{__make} docker-docs

# build dnsname plugin
unset LDFLAGS
pushd dnsname-%{commit_dnsname}
mkdir _build
pushd _build
mkdir -p src/github.com/containers
ln -s ../../../../ src/github.com/containers/dnsname
popd
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd)
%gobuild -o bin/dnsname github.com/containers/dnsname/plugins/meta/dnsname
popd

pushd gvisor-tap-vsock-%{commit_gvproxy}
mkdir _build
pushd _build
mkdir -p src/github.com/containers
ln -s ../../../../ src/github.com/containers/gvisor-tap-vsock
popd
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd)
%gobuild -o bin/gvproxy github.com/containers/gvisor-tap-vsock/cmd/gvproxy
popd

%install
PODMAN_VERSION=%{version} %{__make} PREFIX=%{buildroot}%{_prefix} ETCDIR=%{buildroot}%{_sysconfdir} \
        install.bin \
        install.remote \
        install.man \
        install.systemd \
        install.completions \
        install.docker \
        install.docker-docs

sed -i 's;%{buildroot};;g' %{buildroot}%{_bindir}/docker

# remove unwanted man pages
rm -f %{buildroot}%{_mandir}/man5/docker*.5

# install test scripts, but not the internal helpers.t meta-test
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor
install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav test/system %{buildroot}/%{_datadir}/%{name}/test/
rm -f               %{buildroot}/%{_datadir}/%{name}/test/system/*.t

# do not include docker and podman-remote man pages in main package
for file in `find %{buildroot}%{_mandir}/man[15] -type f | sed "s,%{buildroot},," | grep -v -e remote -e docker`; do
    echo "$file*" >> podman.file-list
done

# install catatonit
install -dp %{buildroot}%{_libexecdir}/podman
install -dp %{buildroot}%{_datadir}/licenses/podman
install -p catatonit-%{cataver}/catatonit %{buildroot}%{_libexecdir}/podman/catatonit
install -p catatonit-%{cataver}/COPYING %{buildroot}%{_datadir}/licenses/podman/COPYING-catatonit

# install dnsname plugin
pushd dnsname-%{commit_dnsname}
%{__make} PREFIX=%{_prefix} DESTDIR=%{buildroot} install
popd

# install gvproxy
pushd gvisor-tap-vsock-%{commit_gvproxy}
install -dp %{buildroot}%{_libexecdir}/%{name}
install -p -m0755 bin/gvproxy %{buildroot}%{_libexecdir}/%{name}
popd

%check
%if 0%{?with_check}
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/cmd/%{name}
%gotest %{import_path}/libkpod
%gotest %{import_path}/libpod
%gotest %{import_path}/pkg/registrar
%endif

%triggerpostun -- %{name} < 1.1
%{_bindir}/%{name} system renumber
exit 0

%preun
if [ $1 == 0 ]; then
  systemctl stop podman.service > /dev/null 2>&1
  systemctl stop podman.socket > /dev/null 2>&1
  systemctl disable podman.service > /dev/null 2>&1
  systemctl disable podman.socket > /dev/null 2>&1
fi
:

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files -f podman.file-list
%license LICENSE COPYING-catatonit
%doc README.md CONTRIBUTING.md install.md transfer.md
%{_bindir}/%{name}
%{_bindir}/%{name}sh
%{_libexecdir}/%{name}/quadlet
%{_libexecdir}/%{name}/rootlessport
%{_datadir}/bash-completion/completions/%{name}
# By "owning" the site-functions dir, we don't need to Require zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%ghost %dir %{_sysconfdir}/cni/net.d
%ghost %{_sysconfdir}/cni/net.d/87-%{name}-bridge.conflist
%{_unitdir}/*.service
%{_unitdir}/*.socket
%{_unitdir}/*.timer
%{_userunitdir}/*.service
%{_userunitdir}/*.socket
%{_userunitdir}/*.timer
%{_usr}/lib/tmpfiles.d/%{name}.conf
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/catatonit
%{_usr}/lib/systemd/system-generators/podman-system-generator
%{_usr}/lib/systemd/user-generators/podman-user-generator


%files docker
%{_bindir}/docker
%{_mandir}/man1/docker*.1*
%{_tmpfilesdir}/%{name}-docker.conf
%{_user_tmpfilesdir}/%{name}-docker.conf

%files remote
%license LICENSE
%{_bindir}/%{name}-remote
%{_mandir}/man1/%{name}-remote*.*
%{_datadir}/bash-completion/completions/%{name}-remote
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}-remote.fish
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}-remote

%files plugins
%license dnsname-%{commit_dnsname}/LICENSE
%doc dnsname-%{commit_dnsname}/{README.md,README_PODMAN.md}
%{_libexecdir}/cni/dnsname

%files tests
%license LICENSE
%{_datadir}/%{name}/test

%files gvproxy
%license gvisor-tap-vsock-%{commit_gvproxy}/LICENSE
%doc gvisor-tap-vsock-%{commit_gvproxy}/README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/gvproxy

%changelog
* Fri Aug 25 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.1-5
- update to the latest content of https://github.com/containers/podman/tree/v4.6.1-rhel
  (https://github.com/containers/podman/commit/ea33dce)
- Related: #2176063

* Tue Aug 22 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.1-4
- amend podmansh provides
- Related: #2176063

* Tue Aug 22 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.1-3
- update to the latest content of https://github.com/containers/podman/tree/v4.6.1-rhel
  (https://github.com/containers/podman/commit/8bb0204)
- Related: #2176063

* Wed Aug 16 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.1-2
- update to the latest content of https://github.com/containers/podman/tree/v4.6.1-rhel
  (https://github.com/containers/podman/commit/1b2fadd)
- Resolves: #2232127

* Fri Aug 11 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.1-1
- update to latest content of https://github.com/containers/podman/releases/tag/4.6.1
- Related: #2176063

* Fri Aug 04 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.0-3
- build podman 4.6.0 off main branch for early testing of zstd compression
- Related: #2176063

* Fri Aug 04 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.0-2
- update license token to be SPDX compatible
- Related: #2176063

* Fri Jul 21 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.0-1
- update to latest content of https://github.com/containers/podman/releases/tag/4.6.0
  (https://github.com/containers/podman/commit/38e6fab9664c6e59b66e73523b307a56130316ae)

* Fri Jul 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.0-0.3
- rebuild with the new bats
- Related: #2176063

* Fri Jul 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.0-0.2
- update to 4.6.0-rc2
- Related: #2176063

* Mon Jul 10 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.6.0-0.1
- update to 4.6.0-rc1
- Related: #2176063

* Wed Jun 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.5.1-5
- rebuild for following CVEs:
CVE-2023-25173 CVE-2022-41724 CVE-2022-41725 CVE-2023-24537 CVE-2023-24538 CVE-2023-24534 CVE-2023-24536 CVE-2022-41723 CVE-2023-24539 CVE-2023-24540 CVE-2023-29400
- Resolves: #2175071
- Resolves: #2179950
- Resolves: #2187318
- Resolves: #2187366
- Resolves: #2203681
- Resolves: #2207512

* Wed Jun 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.5.1-4
- update to https://github.com/containers/gvisor-tap-vsock/releases/tag/v0.6.1
- Related: #2176063

* Wed Jun 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.5.1-3
- rebuild for following CVEs:
CVE-2023-25173 CVE-2022-41724 CVE-2022-41725 CVE-2023-24537 CVE-2023-24538 CVE-2023-24534 CVE-2023-24536 CVE-2022-41723 CVE-2023-24539 CVE-2023-24540 CVE-2023-29400
- Resolves: #2175074
- Resolves: #2179966
- Resolves: #2187322
- Resolves: #2187383
- Resolves: #2203702
- Resolves: #2207522

* Fri Jun 09 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.5.1-2
- rebuild
- Resolves: #2177611

* Fri Jun 02 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.5.1-1
- update to https://github.com/containers/podman/releases/tag/v4.5.1
- Related: #2176063

* Wed Apr 19 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.5.0-1
- update to 4.5.0
- Related: #2176063

* Tue Apr 18 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-10
- build and add missing docker man pages
- Resolves: #2187187

* Fri Apr 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-9
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/fd0ea3b)
- Resolves: #2173089

* Mon Apr 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-8
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/05037d3)
- Resolves: #2178263

* Fri Mar 31 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-7
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/67f7e1e)
- Related: #2176063

* Fri Mar 24 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-6
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/4461c9c)
- Related: #2176063

* Tue Mar 21 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-5
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/bf400bd)
- Related: #2176063

* Mon Mar 20 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-4
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/ffc2614)
- Resolves: #2179450

* Tue Feb 21 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-3
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/e1703bb)
- Related: #2124478

* Mon Feb 20 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-2
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/0b38633)
- Related: #2124478

* Thu Feb 09 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-1
- update to the latest content of https://github.com/containers/podman/tree/v4.4.1-rhel
  (https://github.com/containers/podman/commit/d4e285a)
- Related: #2124478

* Wed Feb 08 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.1-0.1
- update to the latest content of https://github.com/containers/podman/tree/v4.4
  (https://github.com/containers/podman/commit/f5670f0)
- Related: #2124478

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-1
- update to podman-4.4 release
- Related: #2124478

* Wed Feb 01 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.10
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/68bbdc2)
- Related: #2124478

* Mon Jan 30 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.9
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/323b515)
- Related: #2124478

* Wed Jan 25 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.8
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/c35e74f)
- Related: #2124478

* Tue Jan 24 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.7
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/ce504bb)
- Related: #2124478

* Thu Jan 19 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.6
- add quadlet to tests
- Related: #2124478

* Wed Jan 18 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.5
- obsolete podman-catatonit in order to not to file conflict with catatonit
- Related: #2124478

* Wed Jan 18 2023 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.4.0-0.4
- build v4.4.0-rc2
- Related: #2124478

* Tue Jan 17 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.3
- remove podman-machine-cni, it is now part of podman 4.0 or newer
- Related: #2124478

* Tue Jan 17 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.2
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/07ba51d)
- update gvisor-tap-vsock to 0.5.0
- Related: #2124478

* Fri Jan 13 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.4.0-0.1
- podman-4.4.0-rc1
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/f1af5b3)
- Related: #2124478

* Wed Jan 11 2023 Jindrich Novy <jnovy@redhat.com> - 2:4.3.1-4
- podman shouldn't provide and file conflict with catatonit in CRB
- Resolves: #2151322

* Mon Nov 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.3.1-3
- fix 'podman manifest add' is not concurrent safe
- Resolves: #2105173

* Sat Nov 26 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.3.1-2
- properly obsolete catatonit
- Resolves: #2123319

* Wed Nov 16 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.3.1-1
- update to https://github.com/containers/podman/releases/tag/v4.3.1
- Related: #2124478

* Tue Nov 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.3.0-2
- rebuild to fix CVE-2022-30629
- Related: #2102994

* Thu Nov 03 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.3.0-1
- update to https://github.com/containers/podman/releases/tag/v4.3.0
- Related: #2124478

* Mon Aug 22 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.2.0-3
- fix dependency in test subpackage
- Related: #2061316

* Mon Aug 22 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.2.0-2
- readd catatonit
- Related: #2061316

* Thu Aug 11 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.2.0-1
- update to latest content of https://github.com/containers/podman/releases/tag/4.2.0
  (https://github.com/containers/podman/commit/7fe5a419cfd2880df2028ad3d7fd9378a88a04f4)
- Related: #2061316

* Wed Aug 10 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.2.0-0.3rc3
- require catatonit for gating tests
- Related: #2061316

* Fri Aug 05 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.2.0-0.2rc3
- update to 4.2.0-rc3
- Related: #2061316

* Mon Aug 01 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.2.0-0.1rc2
- update to 4.2.0-rc2
- Related: #2061316

* Thu Jul 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.1-6
- convert catatonit dependency to soft dep as catatonit is
  no longer in Appstream but in CRB
- Related: #2061316

* Fri Jul 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.1.1-5
- rebuild for combined gating with catatonit
- Related: #2097694

* Tue Jul 19 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.1.1-4
- catatonit is now a standalone package
- Related: #2097694

* Fri Jul 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.1-3
- update to the latest content of https://github.com/containers/podman/tree/v4.1.1-rhel
  (https://github.com/containers/podman/commit/fa692a6)
- Related: #2097694

* Fri Jul 01 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.1-2
- be sure podman services/sockets are stopped upon package removal
- Related: #2061316

* Wed Jun 15 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.1-1
- update to https://github.com/containers/podman/releases/tag/v4.1.1
- Related: #2061316

* Mon May 23 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.0-4
- don't require runc and Recommends: crun
- Related: #2061316

* Fri May 13 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.0-3
- Re-enable LTO and debuginfo
- Related: #2061316

* Wed May 11 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.0-2
- update gvisor-tap-vsock to 0.2.0 to fix compilation with golang 1.18
- Related: #2061316

* Mon May 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.1.0-1
- update to https://github.com/containers/podman/releases/tag/v4.1.0
- Related: #2061316

* Tue May 03 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.3-2
- require netavark and move CNI to soft dependencies
- Related: #2061316

* Fri Apr 01 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.3-1
- update to https://github.com/containers/podman/releases/tag/v4.0.3
- Related: #2061316

* Fri Mar 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.2-3
- bump minimal libseccomp version requirement
- Related: #2061316

* Mon Mar 14 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.2-2
- rebuilt with golang >= 1.17.5 (CVE-2021-44716, CVE-2021-44717)
- Related: #2061316

* Wed Mar 02 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.2-1
- update to https://github.com/containers/podman/releases/tag/v4.0.2
- Related: #2059681

* Mon Feb 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.1-1
- update to https://github.com/containers/podman/releases/tag/v4.0.1
- Related: #2000051

* Tue Feb 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.0.0-6
- set catatonit cflags after configure step, don't explicitly set ldflags
- Related: #2054115

* Tue Feb 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.0.0-5
- revert previous change and run `set_build_flags` before the build process
- Related: #2054115

* Tue Feb 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.0.0-4
- add -D_FORTIFY_SOURCE=2 for podman-catatonit
- Related: #2054115

* Tue Feb 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.0.0-3
- depend on containers-common >= 2:1-28
- Related: #2000051

* Mon Feb 21 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:4.0.0-2
- use correct commit 49f8da72 for podman, previous commit said 4.0.1-dev
- Related: #2000051

* Fri Feb 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-1
- update to podman-4.0.0 release
- Related: #2000051

* Thu Feb 17 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.32
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/a34f279)
- Related: #2000051

* Tue Feb 15 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.31
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/ab3e566)
- Related: #2000051

* Mon Feb 14 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.30
- fix linker flags to assure -D_FORTIFY_SOURCE=2 is present at the command line
- Related: #2000051

* Mon Feb 14 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.29
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/b0a445e)
- Related: #2000051

* Fri Feb 11 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.28
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/c4a9aa7)
- Related: #2000051

* Thu Feb 10 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.27
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/5b2d96f)
- Related: #2000051

* Wed Feb 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.26
- set CGO_CFLAGS explicitly
- Related: #2000051

* Tue Feb 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.25
- bump to 0.25 to have highest NVR
- Related: #2000051

* Tue Feb 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.4
- rebuilt
- Related: #2000051

* Mon Feb 07 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.3
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/2dca7b2)
- Related: #2000051

* Fri Feb 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.2
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/4ad9e00)
- Related: #2000051

* Fri Feb 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:4.0.0-0.1
- update to the latest content of https://github.com/containers/podman/tree/v4.0
  (https://github.com/containers/podman/commit/337f706)
- Related: #2000051

* Thu Jan 27 2022 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.8
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/a54320a)
- Related: #2000051

* Wed Jan 19 2022 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.7
- add rootless_role (Ed Santiago)
- Related: #2000051

* Mon Jan 17 2022 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.6
- add git-daemon to test subpackage
  (https://github.com/containers/podman/issues/12851)
- Related: #2000051

* Thu Jan 13 2022 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.5
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/63134a1)
- Related: #2000051

* Tue Jan 11 2022 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.4
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/3f57b6e)
- Related: #2000051

* Fri Dec 17 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.3
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/17788ed)
- Related: #2000051

* Thu Dec 09 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.2
- incorporate gating test fixes from Ed Santiago:
  - remove buildah and skopeo (unused)
  - bump BATS from v1.1 to v1.5
  - rename "nonroot" to "rootless"
- Related: #2000051

* Thu Dec 09 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.5-0.1
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/b8fde5c)
- Related: #2000051

* Tue Dec 07 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.4-0.1
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/49f589d)
- Related: #2000051

* Tue Dec 07 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.3-0.11
- remove downstream patch already applied upstream
- Related: #2000051

* Mon Dec 06 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.3-0.10
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/fe44757)
- Related: #2000051

* Thu Dec 02 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.3-0.9
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/815f36a)
- Related: #2000051

* Wed Dec 01 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.3-0.8
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/31bc358)
- Related: #2000051

* Tue Nov 30 2021 Jindrich Novy <jnovy@redhat.com> - 2:3.4.3-0.7
- bump Epoch to not to pull in older versions built off upstream main branch
- Related: #2000051

* Tue Nov 23 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.3-0.6
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/e3a7a74)
- add libsubid_tag.sh into BUILDTAGS
- Related: #2000051

* Mon Nov 22 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.3-0.5
- do not put patch URL as the backported patch will get overwritten when
  "spectool -g -f" is executed
- Related: #2000051

* Mon Nov 22 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.3-0.4
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/7203178)
- Related: #2000051

* Tue Nov 16 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.3-0.3
- remove -t 0 from podman gating test
- Related: #2000051

* Mon Nov 15 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.3-0.2
- add BuildRequires: shadow-utils-subid-devel
- Related: #2000051

* Mon Nov 15 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.3-0.1
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/4808a63)
- Related: #2000051

* Fri Nov 12 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.8
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/fd010ad)
- Related: #2000051

* Thu Nov 11 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.7
- backport https://github.com/containers/podman/pull/12118 to 3.4
  in attempt to fix gating tests
- Related: #2000051

* Thu Nov 11 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.6
- add Requires: gnupg
  (https://github.com/containers/podman/pull/12270)
- Related: #2000051

* Tue Nov 09 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.5
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/8de9950)
- Related: #2000051

* Mon Nov 08 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.4
- update catatonit to 1.7
- Related: #2000051

* Tue Nov 02 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.3
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/75023e9)
- Related: #2000051

* Thu Oct 21 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.2
- compile catatonit library as PIE
- Related: #2000051

* Thu Oct 21 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.2-0.1
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/09aade7)
- Related: #2000051

* Tue Oct 19 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.1-2
- more dependency tightening - thanks to Michael Rochefort for noticing
- Related: #2000051

* Mon Oct 18 2021 Jindrich Novy <jnovy@redhat.com> - 1:3.4.1-1
- update to the latest content of https://github.com/containers/podman/tree/v3.4
  (https://github.com/containers/podman/commit/c15c154)
- Related: #2000051

* Mon Oct 18 2021 Jindrich Novy <jnovy@redhat.com> - 1:4.0.0-0.24
- respect Epoch in subpackage dependencies
- Related: #2000051

* Fri Oct 15 2021 Jindrich Novy <jnovy@redhat.com> - 1:4.0.0-0.23
- bump Epoch to preserve upgrade path from RHEL8
- Related: #2000051

* Mon Oct 11 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.22
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/ea86893)
- Related: #2000051

* Fri Oct 08 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.21
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/14c0fcc)
- Related: #2000051

* Thu Oct 07 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.20
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/bfb904b)
- Related: #2000051

* Wed Oct 06 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.19
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/8bcc086)
- Related: #2000051

* Tue Oct 05 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.18
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/c963a50)
- Related: #2000051

* Mon Oct 04 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.17
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/b9d8c63)
- Related: #2000051

* Fri Oct 01 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.16
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/317e20a)
- Related: #2000051

* Thu Sep 30 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.15
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/b187dfe)
- Related: #2000051

* Wed Sep 29 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.14
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/cd10304)
- Related: #2000051

* Mon Sep 27 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.13
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/e19a09c)
- Related: #2000051

* Fri Sep 24 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.12
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/800d594)
- Related: #2000051

* Thu Sep 23 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.11
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/1dba601)
- Related: #2000051

* Wed Sep 22 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.10
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/8e2d25e)
- Related: #2000051

* Tue Sep 21 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.9
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/b925d70)
- Related: #2000051

* Fri Sep 17 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.8
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/6cf13c3)
- Related: #2000051

* Thu Sep 16 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.7
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/5f41ffd)
- update to https://github.com/containers/podman-machine-cni/releases/tag/v0.2.0
- Related: #2000051

* Wed Sep 15 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.6
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/4b6ffda)
- Related: #2000051

* Wed Sep 15 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.5
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/323fe36)
- Related: #2000051

* Tue Sep 14 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.4
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/b603c7a)
- Related: #2000051

* Mon Sep 13 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.3
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/0f3d3bd)
- Related: #2000051

* Fri Sep 10 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.2
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/63f6656)
- Related: #2000051

* Thu Sep 09 2021 Jindrich Novy <jnovy@redhat.com> - 4.0.0-0.1
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/26c8549)
- Related: #2000051

* Fri Sep 03 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.1-1
- update to the latest content of https://github.com/containers/podman/tree/v3.3.1-rhel
  (https://github.com/containers/podman/commit/405507a)
- Related: #2000051
- mark ghost dir correctly

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 3.3.0-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Aug 05 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-3
- update to the latest content of https://github.com/containers/podman/tree/v3.3
  (https://github.com/containers/podman/commit/57422d2)
- Related: #1970747

* Wed Aug 04 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-2
- update to the latest content of https://github.com/containers/podman/tree/v3.3
  (https://github.com/containers/podman/commit/b1d3875)
- Related: #1970747

* Tue Aug 03 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-1
- update to 3.3.0 release and switch to the v3.3 maint branch
- Related: #1970747

* Mon Aug 02 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.27
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/4244288)
- Related: #1970747

* Fri Jul 30 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.26
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/f17b810)
- Related: #1970747

* Thu Jul 29 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.25
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/2041731)
- Related: #1970747

* Thu Jul 29 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.24
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/f9395dd)
- Related: #1970747

* Wed Jul 28 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.23
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/a5de831)
- Related: #1970747

* Tue Jul 27 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.22
- bump version to follow the 3.3.0 upgrade path
- Related: #1970747

* Tue Jul 27 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.9
- update to the latest content of https://github.com/containers/podman/tree/main
  (https://github.com/containers/podman/commit/4f5b19c)
- Related: #1970747

* Mon Jul 26 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.8
- update to the latest content of https://github.com/containers/podman/tree/v3.2.3-rhel
  (https://github.com/containers/podman/commit/78f0bd7)
- Related: #1970747

* Mon Jul 19 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.7
- switch to v3.2.3-rhel branch
- Related: #1970747

* Fri Jul 16 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.6
- update to the latest content of https://github.com/containers/podman/tree/v3.2
  (https://github.com/containers/podman/commit/2eea7fe)
- Related: #1970747

* Wed Jul 14 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.5
- update to the latest content of https://github.com/containers/podman/tree/v3.2
  (https://github.com/containers/podman/commit/4136f8b)
- Related: #1970747

* Fri Jul 09 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.4
- update product version in gating.yaml
- update to the latest content of https://github.com/containers/podman/tree/v3.2
  (https://github.com/containers/podman/commit/60d12f7)
- Related: #1970747

* Thu Jul 08 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.3
- update to the latest content of https://github.com/containers/podman/tree/v3.2
  (https://github.com/containers/podman/commit/275b0d8)
- Related: #1970747

* Wed Jul 07 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.2
- put 87-podman-bridge.conflist to main podman package not podman-remote
- Related: #1970747

* Mon Jul 05 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.3-0.1
- update to the latest content of https://github.com/containers/podman/tree/v3.2
  (https://github.com/containers/podman/commit/6f0bf16)
- Related: #1970747

* Thu Jul 01 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.2-2
- remove missing unit files
- Related: #1970747

* Thu Jul 01 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.2-1
- consume content from v3.2 upstream branch
- Related: #1970747

* Wed Jun 30 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.21
- fix build
- Related: #1970747

* Wed Jun 30 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.20
- update install targets
- Related: #1970747

* Wed Jun 30 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.19
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/1846070)
- Related: #1970747

* Tue Jun 29 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.18
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/c260cbd)
- Related: #1970747

* Mon Jun 28 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.17
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/0a0ade3)
- Related: #1970747

* Fri Jun 25 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.16
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/d1f57a0)
- Related: #1970747

* Thu Jun 24 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.15
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/fc34f35)
- Related: #1970747

* Wed Jun 23 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.14
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/d3afc6b)
- Related: #1970747

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 3.3.0-0.13
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Tue Jun 22 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.12
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/be15e69)
- Related: #1970747

* Mon Jun 21 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.11
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/928687e)
- Resolves: #1970747

* Fri Jun 18 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.10
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/ce04a3e)
- Resolves: #1970747

* Thu Jun 17 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.9
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/814a8b6)
- Resolves: #1970747

* Wed Jun 16 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.8
- add new systemd unit files
- Related: #1970747

* Wed Jun 16 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.7
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/092b2ec)
- Related: #1970747

* Tue Jun 15 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.6
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/e2f51ee)
- Related: #1970747

* Mon Jun 14 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.5
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/e549ca5)
- Related: #1970747

* Mon Jun 14 2021 Jindrich Novy <jnovy@redhat.com> - 3.3.0-0.4
- update podman
- Related: #1970747

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 3.2.0-0.6
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Apr 06 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.0-0.5
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/2b13c5d)

* Thu Apr 01 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.0-0.4
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/12881ab)

* Wed Mar 31 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.0-0.3
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/a373e2f)

* Tue Mar 30 2021 Jindrich Novy <jnovy@redhat.com> - 3.2.0-0.2
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/5eb5950)

* Mon Mar 29 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.15
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/ccbe7e9)

* Fri Mar 26 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.14
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/9e23e0b)

* Thu Mar 25 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.13
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/e523d09)

* Wed Mar 24 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.12
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/860de13)

* Tue Mar 23 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.11
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/60c90c3)

* Mon Mar 22 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.10
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/ebc9871)

* Fri Mar 19 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.9
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/5d9b070)

* Thu Mar 18 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.8
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/6f6cc1c)

* Wed Mar 17 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.7
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/604459b)

* Tue Mar 16 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.6
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/e7dc592)

* Mon Mar 15 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.5
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/fc02d16)

* Fri Mar 12 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.4
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/81737b3)

* Thu Mar 11 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.3
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/e2d35e5)

* Wed Mar 10 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.2
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/09473d4)

* Tue Mar 09 2021 Jindrich Novy <jnovy@redhat.com> - 3.1.0-0.1
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/789d579)

* Mon Mar 08 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.2-0.5
- remove docker man page as it was removed upstream

* Mon Mar 08 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.2-0.4
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/b7c00f2)

* Fri Mar 05 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.2-0.3
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/4e5cc6a)

* Thu Mar 04 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.2-0.2
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/87e2056)

* Wed Mar 03 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.2-0.1
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/0a40c5a)

* Mon Feb 22 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.1-2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/9a2fc37)

* Fri Feb 19 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.1-1
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/7e286bc)

* Mon Feb 15 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/797f1ea)

* Fri Feb 12 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-1
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/ddd8a17)

* Wed Feb 10 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.29rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/2b89fe7)

* Tue Feb 09 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.28rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/a5ab59e)

* Sat Feb 06 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.27rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/288fb68)

* Thu Feb 04 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.26rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/82081e8)

* Wed Feb 03 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.25rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/978c005)

* Tue Feb 02 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.24rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/67d48c5)

* Mon Feb 01 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.23rc2
- require oci-runtime to assure either crun or runc is pulled in via
  dependencies
- Resolves: #1923547

* Sun Jan 31 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.22rc2
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/745fa4a)

* Wed Jan 27 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.21rc1
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/4dbb58d)

* Tue Jan 26 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.20rc1
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/dc2f4c6)

* Tue Jan 26 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.19rc1
- update to the latest content of https://github.com/containers/podman/tree/v3.0
  (https://github.com/containers/podman/commit/469c203)

* Mon Jan 18 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.18rc1
- switch from master to release candidate (3.0.0-rc1)

* Fri Jan 08 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.17
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/78cda71)

* Thu Jan 07 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.16
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/355e387)

* Wed Jan 06 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.15
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/ffe2b1e)

* Mon Jan 04 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.14
- re-disable LTO as it sill fails even with GCC 11
- Related: #1904567

* Mon Jan 04 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.13
- attempt to build with gcc11
- Related: #1904567

* Mon Jan 04 2021 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.12
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/23f25b8)

* Thu Dec 10 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.11
- update to https://github.com/containers/dnsname/releases/tag/v1.1.1

* Wed Dec 09 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.10
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/dd295f2)

* Mon Dec 07 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.9
- disable LTO to fix build

* Mon Dec 07 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.8
- use dedicated macro to build only on supported arches

* Mon Dec 07 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.7
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/0c96731)

* Mon Dec 07 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.6
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/0c2a43b)

* Sat Dec 05 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.5
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/8e83799)

* Fri Dec 04 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.4
- update to the latest content of https://github.com/containers/podman/tree/master
  (https://github.com/containers/podman/commit/70284b1)

* Thu Dec 03 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.3
- attempt to fix gating tests with patch from Matt Heon

* Thu Dec 03 2020 Jindrich Novy <jnovy@redhat.com> - 3.0.0-0.1
- update NVR to reflect the development version

* Thu Dec 03 2020 Jindrich Novy <jnovy@redhat.com> - 2.2.0-2
- switch to master branch
- remove varlink support
- simplify spec

* Tue Dec 01 2020 Jindrich Novy <jnovy@redhat.com> - 2.2.0-1
- update to https://github.com/containers/podman/releases/tag/v2.2.0

* Thu Nov 05 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-11
- fix branch name setup

* Wed Nov 04 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-10
- attempt to fix linker error with golang-1.15
- add Requires: httpd-tools to tests, needed to work around
  missing htpasswd in docker registry image, thanks to Ed Santiago

* Wed Nov 04 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-9
- simplify spec
- use shortcommit ID in all tarball names

* Fri Oct 23 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-8
- use shortcommit ID in branch tarball name

* Thu Oct 22 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-7
- add gating test files

* Wed Oct 21 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-6
- fix the tarball reference for consumption directly from upstream branch

* Sat Oct 17 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-5
- allow to build directly from upstream branch or release
- make varlink disabled by default

* Thu Oct 15 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-4
- add jnovy to gating test results recipients

* Thu Oct 15 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-3
- update gating tests

* Wed Sep 30 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-2
- fix the container-selinux boolean dependency

* Mon Sep 28 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.1-1
- update to https://github.com/containers/podman/releases/tag/v2.1.1

* Wed Sep 23 2020 Jindrich Novy <jnovy@redhat.com> - 2.1.0-1
- update to https://github.com/containers/podman/releases/tag/v2.1.0

* Wed Sep 23 2020 Jindrich Novy <jnovy@redhat.com> - 2.0.6-5
- allow to be built on different than RHEL OSes

* Tue Sep 22 2020 Jindrich Novy <jnovy@redhat.com> - 2.0.6-4
- include dnsname plugin
Resolves: #1877865

* Tue Sep 22 2020 Jindrich Novy <jnovy@redhat.com> - 2.0.6-3
- require container-selinux only when selinux-policy is installed
Related: #1881218

* Mon Sep 21 2020 Jindrich Novy <jnovy@redhat.com> - 2.0.6-2
- use commit ID to refer to the upstream tarball

* Fri Sep 18 2020 Jindrich Novy <jnovy@redhat.com> - 2.0.6-1
- update to https://github.com/containers/podman/releases/tag/v2.0.6

* Thu Sep 17 2020 Jindrich Novy <jnovy@redhat.com> - 2.0.5-5
- update to podman-2.0.5 in rhel8 branch

