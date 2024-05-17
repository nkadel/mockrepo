# Created by pyp2rpm-3.3.5
%global pypi_name exceptiongroup

Name:           python-%{pypi_name}
Version:        1.2.0
Release:        %mkrel 2
Summary:        A way to represent multiple things going wrong at the same time, in Python
Group:          Development/Python
License:        MIT
URL:            https://github.com/python-trio/exceptiongroup
Source0:        %{pypi_source}
BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros

%description
This is a backport of the BaseExceptionGroup and ExceptionGroup classes from
Python 3.11.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
This is a backport of the BaseExceptionGroup and ExceptionGroup classes from
Python 3.11.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst



%changelog
* Mon Dec 25 2023 wally <wally> 1.2.0-2.mga10
+ Revision: 2021343
- rebuild for py3.12
- new version 1.2.0
- use pyproject rpm macros

* Sat Oct 21 2023 papoteur <papoteur> 1.1.3-1.mga10
+ Revision: 2000004
- new 1.1.3

* Sat Nov 26 2022 papoteur <papoteur> 1.0.4-1.mga9
+ Revision: 1911232
- Fix BR
  remove doc and tests sections
- imported package python-exceptiongroup

