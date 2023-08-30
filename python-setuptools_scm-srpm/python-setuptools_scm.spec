%bcond_without tests

Name:           python-setuptools_scm
Version:        7.1.0
Release:        2%{?dist}
Summary:        Blessed package to manage your versions by SCM tags

License:        MIT
URL:            https://pypi.python.org/pypi/setuptools_scm
Source0:        %{pypi_source setuptools_scm}

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
%if %{with tests}
BuildRequires:  git-core
BuildRequires:  mercurial
%endif

%description
Setuptools_scm handles managing your Python package versions in SCM metadata.
It also handles file finders for the supported SCMs.


%package -n python%{python3_pkgversion}-setuptools_scm
Summary:        %{summary}

%description -n python%{python3_pkgversion}-setuptools_scm
Setuptools_scm handles managing your Python package versions in SCM metadata.
It also handles file finders for the supported SCMs.


%pyproject_extras_subpkg -n python%{python3_pkgversion}-setuptools_scm toml


%prep
%autosetup -p1 -n setuptools_scm-%{version}
# In case of a bootstrap loop between toml and setuptools_scm, do:
#   rm pyproject.toml
# That way, toml is not fetched to parse the file.
# That only works assuming the backend in the file remains the default backend.


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-e %{toxenv}-test}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files setuptools_scm


%if %{with tests}
%check
# Both of the skipped tests try to download from the internet
%tox -- -- -v -k 'not test_pip_download and not test_distlib_setuptools_works'
%endif


%files -n python%{python3_pkgversion}-setuptools_scm -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 17 2022 Miro Hrončok <mhroncok@redhat.com> - 7.1.0-1
- Update to 7.1.0
Resolves: rhbz#2154548

* Sat Aug 06 2022 Charalampos Stratakis <cstratak@redhat.com> - 7.0.5-1
- Update to 7.0.5
Resolves: rhbz#2106018

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Charalampos Stratakis <cstratak@redhat.com> - 7.0.4-1
- Update to 7.0.4
Resolves: rhbz#2103092

* Wed Jun 29 2022 Lumír Balhar <lbalhar@redhat.com> - 7.0.3-1
- Update to 7.0.3
Resolves: rhbz#2099730

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 6.4.2-3
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.4.2-2
- Bootstrap for Python 3.11

* Thu Feb 17 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 6.4.2-1
- Update to latest version (#2041601)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 20 2021 Lumír Balhar <lbalhar@redhat.com> - 6.3.2-1
- Update to 6.3.2
Resolves: rhbz#2001028

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 6.0.1-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 6.0.1-2
- Bootstrap for Python 3.10

* Mon Mar 22 2021 Charalampos Stratakis <cstratak@redhat.com> - 6.0.1-1
- Update to 6.0.1
- Fixes: rhbz#1939828

* Fri Jan 29 2021 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-1
- Update to 5.0.1
- Fixes: rhbz#1907070

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 2020 Miro Hrončok <mhroncok@redhat.com> - 4.1.2-4
- BuildRequire six explicitly, for tests

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 4.1.2-2
- Add setuptools_scm[toml] subpackage

* Mon Jun 01 2020 Charalampos Stratakis <cstratak@redhat.com> - 4.1.2-1
- Update to 4.1.2 (#1839497)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-2
- Bootstrap for Python 3.9

* Tue Apr 14 2020 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-1
- Update to 3.5.0 (#1792534)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Orion Poplawski <orion@nwra.com> - 3.3.3-6
- Drop python2 for Fedora 32+/EPEL8+

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.3-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.3-4
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.3-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 12 2019 Orion Poplawski <orion@nwra.com> - 3.3.3-1
- Update to 3.3.3

* Sat May 11 2019 Orion Poplawski <orion@nwra.com> - 3.3.1-1
- Update to 3.3.1

* Tue May  7 2019 Orion Poplawski <orion@nwra.com> - 3.3.0-1
- Update to 3.3.0

* Sat Feb 2 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Sun Jul 29 2018 Orion Poplawski <orion@nwra.com> - 3.0.4-1
- Update to 3.0.4
- Re-enable tests

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-3
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-2
- Bootstrap for Python 3.7

* Mon May 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.15.7-1
- Update to 1.15.7

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.15.6-7
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.15.6-6
- Remove platform-python subpackage

* Thu Aug 24 2017 Miro Hrončok <mhroncok@redhat.com> - 1.15.6-5
- Rebuilt for rhbz#1484607

* Sun Aug 20 2017 Tomas Orsava <torsava@redhat.com> - 1.15.6-4
- Re-enable tests to finish bootstrapping the platform-python stack
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Aug 10 2017 Lumír Balhar <lbalhar@redhat.com> - 1.15.6-3
- Add subpackage for platform-python
- Disable tests so platform-python stack can be bootstrapped
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Orion Poplawski <orion@cora.nwra.com> - 1.15.6-1
- Update to 1.15.6

* Mon Apr 10 2017 Orion Poplawski <orion@cora.nwra.com> - 1.15.5-1
- Update to 1.15.5

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 04 2017 Kevin Fenzi <kevin@scrye.com> - 1.15.0-1
- Update to 1.15.0

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.13.0-2
- Rebuild for Python 3.6

* Mon Oct 10 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.13.0-1
- Update to 1.13.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-2
- No python2 package on EPEL (setuptools too old)

* Thu Dec 17 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-1
- Update to 1.10.1

* Wed Dec 2 2015 Orion Poplawski <orion@cora.nwra.com> - 1.9.0-1
- Update to 1.9.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Oct 19 2015 Orion Poplawski <orion@cora.nwra.com> - 1.8.0-2
- Cleanup stray .pyc files from tests

* Sat Sep 19 2015 Orion Poplawski <orion@cora.nwra.com> - 1.8.0-1
- Update to 1.8.0
- Fix license tag

* Mon Sep 14 2015 Orion Poplawski <orion@cora.nwra.com> - 1.7.0-1
- Initial package
