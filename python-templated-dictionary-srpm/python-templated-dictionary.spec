%global srcname templated-dictionary
%global python3_pkgversion 3

%if 0%{?rhel} == 7
%global python3_pkgversion 36
%endif

Name:       python-%{srcname}
Version:    1.1
#Release:    4%%{?dist}
Release:    0.4%{?dist}
Summary:    Dictionary with Jinja2 expansion

License:    GPLv2+
URL:        https://github.com/xsuchy/templated-dictionary

# Source is created by:
# git clone https://github.com/xsuchy/templated-dictionary && cd templated-dictionary
# tito build --tgz --tag %%name-%%version-%%release
Source0:    %name-%version.tar.gz

BuildArch: noarch

BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
Requires:      python%{python3_pkgversion}-jinja2

%global _description\
Dictionary where __getitem__() is run through Jinja2 template.

%description %_description


%package -n python3-%{srcname}
Summary: %{summary}
%{?py_provides:%py_provides python3-%{srcname}}
%description -n python3-%{srcname} %_description


%prep
%setup -q


%build
version="%version" %py3_build

%install
version=%version %py3_install


%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/templated_dictionary-*.egg-info/
%{python3_sitelib}/templated_dictionary/


%changelog
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Miroslav Suchý <msuchy@redhat.com> 1.1-1
- require python3- variants and more specifis files section
- remove python2 support

* Wed Nov 18 2020 Miroslav Suchý <msuchy@redhat.com> 1.0-1
- new package
