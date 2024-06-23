## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%bcond_with testcoverage
%if ! 0%{?rhel} || 0%{?rhel} >= 10
%bcond_without pyproject_build
%bcond_without genbrs
%else
%bcond_with pyproject_build
%bcond_with genbrs
%endif

%if 0%{undefined pyproject_files}
%global pyproject_files %{_builddir}/%{name}-%{version}-%{release}.%{_arch}-pyproject-files
%endif

%global srcname rpmautospec_core
%global canonicalname %{py_dist_name %{srcname}}

Name: python-%{canonicalname}
Version: 0.1.4
Release: %autorelease
Summary: Minimum functionality for rpmautospec

License: MIT
URL: https://github.com/fedora-infra/%{canonicalname}
Source0: %{pypi_source %{srcname}}
BuildArch: noarch
BuildRequires: python3-devel >= 3.6.0
# The dependencies needed for testing don’t get auto-generated.
BuildRequires: python3dist(pytest)
%if %{with testcoverage}
BuildRequires: python3dist(pytest-cov)
%endif
BuildRequires: sed

%if %{with genbrs}
%generate_buildrequires
%{pyproject_buildrequires}
%else
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools)
%endif

%global _description %{expand:
This package contains minimum functionality to determine if an RPM spec file
uses rpmautospec features.}

%description %_description

%package -n python3-%{canonicalname}
Summary: %{summary}
%if %{without pyproject_build}
%py_provides python3-%{canonicalname}
%endif

%description -n python3-%{canonicalname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%if %{without testcoverage}
cat << PYTESTINI > pytest.ini
[pytest]
addopts =
PYTESTINI
%endif

%if %{without pyproject_build}
cat << SETUPPY > setup.py
from setuptools import setup

setup(name="%{canonicalname}", version="%{version}", packages=["%{srcname}"])
SETUPPY
%endif

%build
%if %{with pyproject_build}
%pyproject_wheel
%else
%py3_build
%endif

%install
%if %{with pyproject_build}
%pyproject_install
%pyproject_save_files %{srcname}
# Work around poetry not listing license files as such in package metadata.
sed -i -e 's|^\(.*/LICENSE\)|%%license \1|g' %{pyproject_files}
%else
%py3_install
echo '%{python3_sitelib}/%{srcname}*' > %{pyproject_files}
%endif

%check
%pytest

%files -n python3-%{canonicalname} -f %{pyproject_files}
%doc README.md
%if %{without pyproject_build}
%license LICENSE
%endif

%changelog
* Tue Jan 09 2024 Nils Philippsen <nils@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Fri Jan 05 2024 Nils Philippsen <nils@redhat.com> - 0.1.3-1
- Update to 0.1.3

* Fri Dec 15 2023 Nils Philippsen <nils@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Sun Dec 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.1.1-8
- Always disable test coverage checks

* Fri Nov 17 2023 Nils Philippsen <nils@redhat.com> - 0.1.1-6
- Don’t generate build requires on EL <= 9

* Fri Nov 17 2023 Nils Philippsen <nils@redhat.com> - 0.1.1-5
- Build using setuptools on EL <= 9

* Fri Nov 17 2023 Nils Philippsen <nils@redhat.com> - 0.1.1-2
- Make it build on older EL releases

* Wed Nov 15 2023 Nils Philippsen <nils@redhat.com> - 0.1.1-1
- Update to 0.1.1

* Tue Nov 14 2023 Nils Philippsen <nils@redhat.com> - 0.1.0-1
- Initial import
