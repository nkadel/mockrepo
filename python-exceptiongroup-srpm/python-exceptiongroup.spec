# Created by pyp2rpm-3.3.5
%global pypi_name exceptiongroup

Name:           python-%{pypi_name}
Version:        1.0.4
Release:        0.1%{?dist}
Summary:        A way to represent multiple things going wrong at the same time, in Python
Group:          Development/Python
License:        MIT
URL:            https://github.com/python-trio/exceptiongroup
Source0:        %{pypi_source}
BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(flit-scm)

%description
This is a backport of the BaseExceptionGroup and ExceptionGroup classes 
from Python 3.11.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:       python3dist(trio)

%description -n python3-%{pypi_name}
This is a backport of the BaseExceptionGroup and ExceptionGroup classes 
from Python 3.11.


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst



%changelog
* Sat Nov 26 2022 papoteur <papoteur> 1.0.4-1.mga9
+ Revision: 1911232
- Fix BR
  remove doc and tests sections
- imported package python-exceptiongroup

