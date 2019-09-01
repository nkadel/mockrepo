mockrepo
========

Wrapper for SRPM building tools for latest mock on RHEL 8, etc.

Git Checkout
===========

This repository relies on extensive git submodules. When cloneing it locally, use:

* git clone https://github.com/nkadel/mockrepo

*** NOTE: The git repos at github.com do not include the tarballs ***

Extracting the tarballs from the upstream git repo is a bit
complicated by mock, and mock-core-configs, both being part of the
same git repo. It takes a bit of work to repackage them in the formats
used by EPEL and which are replicated here.

* make build

Installing Samba
==============--

The relevant yum repository is built locally in samba4reepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Samba RPM Build Security
====================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPG signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

		Nico Kadel-Garcia <nkadel@gmail.com>
