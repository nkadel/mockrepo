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

MOCKPKGS+=distribution-gpg-keys-srpm
MOCKPKGS+=mock-core-configs-srpm
MOCKPKGS+=mock-srpm
MOCKPKGS+=pyliblzma-srpm
MOCKPKGS+=pylint-srpm
MOCKPKGS+=pytest-srpm
MOCKPKGS+=python3-mockbuild-srpm
MOCKPKGS+=python-isort-srpm
MOCKPKGS+=python-pytest-mock-srpm
MOCKPKGS+=python-pytest-runner-srpm


REPOS+=mockrepo/el/7
#REPOS+=mockrepo/el/8
REPOS+=mockrepo/fedora/30

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=mockrepo-7-x86_64.cfg
#CFGS+=mockrepo-8-x86_64.cfg
CFGS+=mockrepo-f30-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-7-x86_64.cfg
#MOCKCFGS+=epel-8-x86_64.cfg
MOCKCFGS+=fedora-30-x86_64.cfg

all:: $(CFGS) $(MOCKCFGS)
all:: $(REPODIRS)
all:: $(MOCKPKGS)

all getsrc install clean:: FORCE
	@for name in $(MOCKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# Build for locacl OS
build:: FORCE
	@for name in $(MOCKPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done

# Dependencies
python-py2pack-srpm:: python-metaextract-srpm

# Actually build in directories
$(MOCKPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo -q `dirname $@`


.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

mockrepo-7-x86_64.cfg: /etc/mock/epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/mockrepo-7-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@~
	@mv $@~ $@

mockrepo-8-x86_64.cfg: /etc/mock/epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-8-x86_64/mockrepo-8-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/el/8/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@~
	@mv $@~ $@

mockrepo-f30-x86_64.cfg: /etc/mock/fedora-30-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-30-x86_64/mockrepo-f30-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[mockrepo]' >> $@
	@echo 'name=mockrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/mockrepo/fedora/30/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@~
	@mv $@~ $@


$(MOCKCFGS)::
	ln -sf --no-dereference /etc/mock/$@ $@


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
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(MOCKPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(MOCKPKGS)

FORCE::
