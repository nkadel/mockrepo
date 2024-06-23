# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# RHEL does not include the test dependencies
%bcond tests %{undefined rhel}

Name:           python-poetry-core
Version:        1.8.1
Release:        3%{?dist}
Summary:        Poetry PEP 517 Build Backend
# SPDX
License:        MIT
URL:            https://github.com/python-poetry/poetry-core
Source0:        %{url}/archive/%{version}/poetry-core-%{version}.tar.gz

# This patch moves the vendored requires definition
# from vendors/pyproject.toml to pyproject.toml
# Intentionally contains the removed hunk to prevent patch aging
Patch1:         poetry-core-1.8.1-devendor.patch
Patch2: python-poetry-core-c99.patch

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

# Addes for RHEL
BuildRequires:  python%{python3_pkgversion}-fastjsonschema
BuildRequires:  python%{python3_pkgversion}-lark

%if %{with tests}
# for tests (only specified via poetry poetry.dev-dependencies with pre-commit etc.)
BuildRequires:  python%{python3_pkgversion}-build
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-mock
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-tomli-w
BuildRequires:  python%{python3_pkgversion}-virtualenv
BuildRequires:  gcc
BuildRequires:  git-core
%endif


%global _description %{expand:
A PEP 517 build backend implementation developed for Poetry.
This project is intended to be a light weight, fully compliant, self-contained
package allowing PEP 517 compatible build frontends to build Poetry managed
projects.}

%description %_description

%package -n python%{python3_pkgversion}-poetry-core
Summary:        %{summary}

# Previous versions of poetry included poetry-core in it
Conflicts:      python%{python3_version}dist(poetry) < 1.1

%py_provides python%{python3_pkgversion}-poetry-core

%description -n python%{python3_pkgversion}-poetry-core %_description


%prep
%autosetup -p1 -n poetry-core-%{version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
# we debundle the deps after we use the bundled deps in previous step to parse the deps 🤯
rm -r src/poetry/core/_vendor

%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files poetry


%check
%if %{with tests}
# don't use %%tox here because tox.ini runs "poetry install"
# TODO investigate failures in test_default_with_excluded_data, test_default_src_with_excluded_data
%pytest -k "not with_excluded_data"
%else
%pyproject_check_import
%endif


%files -n python%{python3_pkgversion}-poetry-core -f %{pyproject_files}
%doc README.md
%license LICENSE


%changelog
* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.8.1-1
- Update to 1.8.1
- Fixes: rhbz#2247249

* Thu Jan 04 2024 Florian Weimer <fweimer@redhat.com> - 1.7.0-2
- Backport upstream patch to fix C compatibility issue

* Fri Sep 01 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.7.0-1
- Update to 1.7.0
- Fixes: rhbz#2232934

* Wed Aug 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.6.1-2
- Drop unwanted tomli dependency

* Wed Jul 26 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.6.1-1
- Update to 1.6.1
- Fixes: rhbz#2144878

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.4.0-4
- Rebuilt for Python 3.12

* Mon May 29 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.0-3
- Disable tests in RHEL builds

* Sat Feb 25 2023 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-2
- Remove unused build dependency on python3-pep517

* Mon Feb 20 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Fixes: rhbz#1944752

* Wed Nov 16 2022 Lumír Balhar <lbalhar@redhat.com> - 1.2.0-2
- Add missing buildrequire - setuptools (#2142040)

* Fri Sep 30 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.8-2
- Rebuilt for Python 3.11

* Mon Mar 07 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.8-1
- Update to 1.0.8

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.7-1
- Update to 1.0.7

* Fri Oct 01 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.6-1
- Update to 1.0.6

* Tue Sep 07 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Thu Aug 19 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.3-5
- Bundle vendored libraries again, to fix poetry install

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Lumír Balhar <lbalhar@redhat.com> - 1.0.3-3
- Allow newer packaging version
- Allow newer pyrsistent version

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.3-2
- Rebuilt for Python 3.10

* Thu Apr 15 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Thu Feb 25 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-1
- Initial package
