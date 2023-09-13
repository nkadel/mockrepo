#
# Makefile - build wrapper for py2pack on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	MOCKPKGS below
#
#	Set up local 

REPOBASE=file://$(PWD)
#REPOBASE=http://localhost

MOCKPKGS+=python-setuptools_scm-srpm
MOCKPKGS+=python-flit-srpm
MOCKPKGS+=python-flit-scm-srpm
MOCKPKGS+=python-pyroute2-srpm
MOCKPKGS+=python-templated-dictionary-srpm

# Build for Amazon Linux 2023
MOCKPKGS+=distribution-gpg-keys-srpm
MOCKPKGS+=gtk2-srpm
MOCKPKGS+=procenv-srpm
MOCKPKGS+=util-linux-srpm

# Requires util-linux and distribution-gpg-keys ang gtk2-devel
MOCKPKGS+=usermode-srpm

# Needs flit-scm
MOCKPKGS+=python-exceptiongroup-srpm
# Requires exceptiongroup
MOCKPKGS+=mock-core-configs-srpm
MOCKPKGS+=mock-srpm

REPOS+=mockrepo/el/8
REPOS+=mockrepo/el/9
REPOS+=mockrepo/fedora/38
REPOS+=mockrepo/amazon/2023

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=mockrepo-7-x86_64.cfg
CFGS+=mockrepo-8-x86_64.cfg
CFGS+=mockrepo-9-x86_64.cfg
CFGS+=mockrepo-f38-x86_64.cfg
CFGS+=mockrepo-amz2023-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos+epel-7-x86_64.cfg
MOCKCFGS+=centos-stream+epel-8-x86_64.cfg
MOCKCFGS+=centos-stream+epel-9-x86_64.cfg
MOCKCFGS+=fedora-38-x86_64.cfg
MOCKCFGS+=amazonlinux-2023-x86_64.cfg

all:: install

.PHONY: getsrc install clean build
install:: $(CFGS) $(MOCKCFGS) $(REPODIRS) $(MOCKPKGS)
getsrc install clean build::
	@for name in $(MOCKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done

# Build for locacl OS
build::
	@for name in $(MOCKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done

# Dependencies
python-py2pack-srpm:: python-metaextract-srpm

pyliblzma-srpm:: python2-test-srpm

#python-setuptools_scm:: python-pytest-mock-srpm

# Actually build in directories
.PHONY: $(MOCKPKGS)
$(MOCKPKGS)::
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	createrepo_c -q `dirname $@`


.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

$(MOCKCFGS)::
	@echo Generating $@ from /etc/mock/$@
	@echo "include('/etc/mock/$@')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@

mockrepo-7-x86_64.cfg: /etc/mock/centos+epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'mockrepo-{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/el/7/x86_64/' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=5' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

mockrepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'ansiblerepo-f{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['root'] = 'mockrepo-{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/el/8/x86_64/' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=5' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

mockrepo-9-x86_64.cfg: /etc/mock/centos-stream+epel-9-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'mockrepo-{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/el/9/x86_64/' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=5' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

mockrepo-f38-x86_64.cfg: /etc/mock/fedora-38-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'ansiblerepo-f{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['root'] = 'ansiblerepo-f{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/fedora/38/x86_64/' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=5' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

mockrepo-amz2023-x86_64.cfg: /etc/mock/amazonlinux-2023-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'ansiblerepo-f{{ releasever }}-{{ target_arch }}'" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/amazon/2023/x86_64/' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=5' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

repo: mockrepo.repo
mockrepo.repo:: Makefile mockrepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	elif [ -s /etc/amazon-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/amazon/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(MOCKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(MOCKPKGS)
