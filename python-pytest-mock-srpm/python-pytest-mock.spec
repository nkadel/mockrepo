%global pypi_name pytest-mock
%global file_name pytest_mock
%global desc This plugin installs a mocker fixture which is a thin-wrapper around the \
patching API provided by the mock package, but with the benefit of not having \
to worry about undoing patches at the end of a test.


Name:           python-%{pypi_name}
Version:        1.10.1
Release:        1%{?dist}
Summary:        Thin-wrapper around the mock package for easier use with py.test

License:        MIT
URL:            https://pypi.python.org/pypi/pytest-mock
Source0:        https://files.pythonhosted.org/packages/source/p/pytest-mock/pytest-mock-%{version}.tar.gz
BuildArch:      noarch

%description
%{desc}


%package -n     python2-%{pypi_name}
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-pytest >= 2.7
BuildRequires:  python2-mock
BuildRequires:  python2-setuptools_scm
Requires:       python2-pytest >= 2.7
Requires:       python2-mock
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest >= 2.7
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
Requires:       python%{python3_pkgversion}-pytest >= 2.7
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
%{desc}


%prep
%setup -qn %{pypi_name}-%{version}
rm -rf *.egg-info

# Correct end of line encoding for README
sed -i 's/\r$//' README.rst


%build
%py2_build
%py3_build


%install
%py3_install
%py2_install


%check
PYTHONPATH="$(pwd)" py.test-%{python2_version} test_pytest_mock.py
PYTHONPATH="$(pwd)" py.test-%{python3_version} test_pytest_mock.py


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{file_name}-%{version}-py%{python2_version}.egg-info/
%{python2_sitelib}/%{file_name}.py*
%{python2_sitelib}/_pytest_mock_version.py*


%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{file_name}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{file_name}.py*
%{python3_sitelib}/__pycache__/%{file_name}*.py*
%{python3_sitelib}/_pytest_mock_version.py*
%{python3_sitelib}/__pycache__/_pytest_mock_version.cpython*


%changelog
* Sat Feb 23 2019 Julien Enselme <jujens@jujens.eu> - 1.10.1-1
- Update to 1.10.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10.0-2
- Rebuilt for Python 3.7

* Mon May 07 2018 Julien Enselme <jujens@jujens.eu> - 1.10.0-1
- Update to 1.10.0

* Sun Apr 15 2018 Julien Enselme <jujens@jujens.eu> - 1.9.0-1
- Update to 1.9.0

* Thu Mar 01 2018 Julien Enselme <jujens@jujens.eu> - 1.7.1-1
- Update to 1.7.1

* Mon Feb 19 2018 Julien Enselme <jujens@jujesn.eu> - 1.7.0-1
- Update to 1.7.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 16 2017 Julien Enselme <jujens@jujens.eu> - 1.6.3-1
- Update to 1.6.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Julien Enselme <jujens@jujens.eu> - 1.6.2-1
- Update to 1.6.2

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 1.6.0-2
- Add missing BR

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 1.6.0-1
- Update to 1.6.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2-3
- Rebuild for Python 3.6

* Sat Oct 01 2016 Julien Enselme <jujens@jujens.eu> - 1.2-2
- Add patch to fix tests with pytest3

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 1.2-1
- Update to 1.2

* Wed Aug 31 2016 Julien Enselme <jujens@jujens.eu> - 1.1-3
- Use %%summary instead of custom %%sum macro

* Mon Aug 29 2016 Julien Enselme <jujens@jujens.eu> - 1.1-2
- Add python2-mock to BR so %%check passes correctly.

* Tue Jul 26 2016 Julien Enselme <jujens@jujens.eu> - 1.1-1
- Inital package
