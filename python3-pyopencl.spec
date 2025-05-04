#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# py.test calls

# FIXME - somehow make build process to leave source C files, so debuginfo will pick these up. For now just disable debuginfo packages
%define		_enable_debug_packages 0

%define		pytools_ver	2025.1.2
%define		pypi_name	pyopencl
Summary:	Python 2 wrapper for OpenCL
Summary(pl.UTF-8):	Interfejs Pythona 2 do OpenCL
Name:		python3-pyopencl
Version:	2025.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pyopencl/
Source0:	https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	405536951035e143f97a415edb64900d
URL:		http://mathema.tician.de/software/pyopencl
BuildRequires:	OpenCL-devel >= 1.2
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	python3-build
BuildRequires:	python3-cffi >= 1.1.0
BuildRequires:	python3-installer
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
%if %{with tests}
BuildRequires:	python3-Mako >= 0.3.6
BuildRequires:	python3-appdirs >= 1.4.0
BuildRequires:	python3-decorator >= 3.2.0
BuildRequires:	python3-pytest >= 2
BuildRequires:	python3-pytools >= %{pytools_ver}
BuildRequires:	python3-six >= 1.9.0
%endif
%if %{with doc}
BuildRequires:	python3-numpy
BuildRequires:	python3-pytools >= %{pytools_ver}
BuildRequires:	python3-six >= 1.9.0
BuildRequires:	python3-sphinx_bootstrap_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	OpenCL >= 1.1
Requires:	python3-appdirs >= 1.4.0
Requires:	python3-decorator >= 3.2.0
Requires:	python3-numpy
Requires:	python3-pytools >= %{pytools_ver}
Suggests:	python3-Mako >= 0.3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyOpenCL lets you access GPUs and other massively parallel compute
devices from Python. It tries to offer computing goodness in the
spirit of its sister project PyCUDA.

%description -l pl.UTF-8
PyOpenCL pozwala na dostęp z poziomu Pythona do GPU i innych znacznie
zrównoleglonych jednostek obliczeniowych. Próbuje zaoferować
możliwości obliczeniowe w tym samym stylu, co siostrzany projekt
PyCUDA.

%package apidocs
Summary:	Documentation for PyOpenCL module
Summary(pl.UTF-8):	Dokumentacja modułu PyOpenCL
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for PyOpenCL module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu PyOpenCL.

%package examples
Summary:	Examples for PyOpenCL module
Summary(pl.UTF-8):	Przykłady do modułu PyOpenCL
Group:		Documentation

%description examples
Examples for PyOpenCL module.

%description examples -l pl.UTF-8
Przykłady do modułu PyOpenCL.

%prep
%setup -q -n pyopencl-%{version}

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' examples/*.py

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
%{__make} -C doc html \
	PYTHONPATH="$(pwd)/build-3-doc" \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/pyopencl
%attr(755,root,root) %{py3_sitedir}/pyopencl/_cl.*.so
%{py3_sitedir}/pyopencl/*.py
%{py3_sitedir}/pyopencl/__pycache__
%{py3_sitedir}/pyopencl/characterize
%{py3_sitedir}/pyopencl/cl
%{py3_sitedir}/pyopencl/compyte
%{py3_sitedir}/pyopencl-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
