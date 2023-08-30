## START: Set by rpmautospec
## (rpmautospec version 0.3.1)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global _description %{expand:
A PEP 518 build backend that uses setuptools_scm to generate a version file
from your version control system, then flit_core to build the package.}

Name:           python-flit-scm
Version:        1.7.0
Release:        %{autorelease}
Summary:        PEP 518 build backend that uses setuptools_scm and flit

License:        MIT
URL:            https://pypi.org/pypi/flit_scm
Source0:        %{pypi_source flit_scm}

BuildArch:      noarch

# Manually added
Provides:  python3dist(flit-scm) = %{version}-%{release}

%description %_description

%package -n python3-flit-scm
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-flit-scm %_description

%prep
%autosetup -n flit_scm-%{version}

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

# see pyproject-rpm-macros documentation for more forms
%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files flit_scm

%check
%pyproject_check_import

%files -n python3-flit-scm -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.7.0-1
- feat: ready for review

* Mon Dec 05 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.8.0-1
- init
