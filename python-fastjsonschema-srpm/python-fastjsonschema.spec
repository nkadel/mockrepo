# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           python-fastjsonschema
Version:        2.18.0
#Release:        4%%{?dist}
Release:        0.4%{?dist}
Summary:        Fastest Python implementation of JSON schema

License:        BSD-3-Clause
URL:            https://github.com/horejsek/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
fastjsonschema implements validation of JSON documents by JSON schema.
The library implements JSON schema drafts 04, 06 and 07.
The main purpose is to have a really fast implementation.}

%description %_description

%package -n     python%{python3_pkgversion}-fastjsonschema
Summary:        %{summary}

%py_provides python%{python3_pkgversion}-fasstjsonschema

%description -n python%{python3_pkgversion}-fastjsonschema %_description

%prep
%autosetup -p1 -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files fastjsonschema

%check
%pytest -m "not benchmark"

%files -n python%{python3_pkgversion}-fastjsonschema -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Fri Jan 26 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.18.0-4
- Avoid tox dependency

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 11 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.18.0-1
- Update to 2.18.0
- Fixes: rhbz#2128071

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.16.3-2
- Rebuilt for Python 3.12

* Mon Mar 20 2023 Jerry James <loganjerry@gmail.com> - 2.16.3-1
- Version 2.16.3
- Convert License tag to SPDX

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jul 25 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.16.1-1
- Update to 2.16.1
- Fixes: rhbz#2107889

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.15.3-3
- Rebuilt for Python 3.11

* Tue Apr 05 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.15.3-2
- Backport patch to fix failing test

* Mon Jan 31 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Tomas Hrnciar <thrnciar@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.15.0-2
- Rebuilt for Python 3.10

* Thu Feb  4 09:47:59 CET 2021 Tomas Hrnciar <thrnciar@redhat.com> - 2.15.0-1
- Update 2.15.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Tomas Hrnciar <thrnciar@redhat.com> - 2.14.5-1
- Initial package
