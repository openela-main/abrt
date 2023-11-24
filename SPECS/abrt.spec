# http://fedoraproject.org/wiki/Packaging:Guidelines#PIE
# http://fedoraproject.org/wiki/Hardened_Packages
%global _hardened_build 1

%if 0%{?fedora} || 0%{?rhel} > 7
# Enable python3 build by default
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} > 7 || 0%{?fedora} > 28
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

%if 0%{?rhel}%{?suse_version}
    %bcond_with bodhi
%else
    %bcond_without bodhi
%endif

# build abrt-atomic subpackage
%bcond_without atomic

# rpmbuild --define 'desktopvendor mystring'
%if "x%{desktopvendor}" == "x"
    %define desktopvendor %(source /etc/os-release; echo ${ID})
%endif

%if 0%{?suse_version}
%define dbus_devel dbus-1-devel
%define libjson_devel libjson-devel
%define nss_devel mozilla-nss-devel
%define shadow_utils pwdutils
%else
%define dbus_devel dbus-devel
%define libjson_devel json-c-devel
%define nss_devel nss-devel
%define shadow_utils shadow-utils
%endif

# do not append package version to doc directory of subpackages in F20 and later; rhbz#993656
%if "%{_pkgdocdir}" == "%{_docdir}/%{name}"
    %define docdirversion %{nil}
%else
    %define docdirversion -%{version}
%endif

%define libreport_ver 2.9.3
%define satyr_ver 0.24

Summary: Automatic bug detection and reporting tool
Name: abrt
Version: 2.10.9
Release: 24%{?dist}.openela.0.1
License: GPLv2+
URL: https://abrt.readthedocs.org/
Source: https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0001: 0001-Remove-dependency-on-deprecated-nss-pem.patch
#Patch0002: 0002-testsuite-add-test-for-core-template-substitution.patch
Patch0003: 0003-ccpp-add-h-and-e-parameter-into-abrt-hook-ccpp.patch
#Patch0004: 0004-spec-remove-duplicated-python3-devel.patch
#Patch0005: 0005-spec-Switch-hardcoded-python3-shebangs-into-the-__py.patch
#Patch0006: 0006-spec-sed-abrt-action-find-bodhi-update-only-if-with-.patch
#Patch0007: 0007-Sed-shebang-only-if-have_kexec_tools-1-in-some-tools.patch
#Patch0008: 0008-spec-switch-Python-tests-to-use-__python3.patch
Patch0009: 0009-lib-Correct-the-syntax-for-gdb-backtrace-command.patch
#git format-patch 7e9e07dc -N --start-number 10 --topo-order
#Patch0010: 0010-testsuite-fix-path-for-augeas-in-ccpp-plugin-hook.patch
#Patch0011: 0011-testsuite-Remove-abrt-Python2-packages.patch
#Patch0012: 0012-testsuite-Force-grep-to-process-binary-files.patch
#Patch0013: 0013-testsuite-Force-grep-to-process-binary-files-2.patch
#Patch0014: 0014-testsuite-Disable-Python2-integration-tests.patch
#Patch0015: 0015-testsuite-Migrate-integeration-tests-to-Python3.patch
#Patch0016: 0016-testsuite-Open-files-in-binary-mode.patch
#Patch0017: 0017-testsuite-Test-Python3-with-dbus-configuration.patch
#Patch0018: 0018-testsuite-Migrate-helper-scripts-in-tests-to-Python3.patch
#Patch0019: 0019-testsuite-Fix-for-tests-incorrectly-marked-as-failed.patch
#Patch0020: 0020-revert-spec-disable-addon-vmcore-on-aarch64.patch
#Patch0021: 0021-spec-turn-on-enable-native-unwinder-aarch64.patch
#git format-patch b13f52bd5 -N --start-number 21 --topo-order
#Patch0022: 0022-spec-Set-PYTHON-to-python3-during-install.patch
#Patch0023: 0023-spec-Remove-forgotten-have_kexec_tools-check.patch
Patch0024: 0024-dbus-Add-configuration-for-Python3.patch
Patch0025: 0025-daemon-Fix-double-closed-fd-race-condition.patch
#git format-patch 1725bd258 -N --start-number 26 --topo-order
#Patch0026: 0026-cli-list-show-a-hint-about-creating-a-case-in-RHTS.patch
#Patch0027: 0027-cli-mark-the-suggestion-text-for-translation.patch
#Patch0028: 0028-cli-get-list-of-possible-workflows-for-problem_data_.patch
#Patch0029: 0029-spec-Add-explicit-package-version-requirement-of-abr.patch
#git format-patch 2.10.9-10.el8 -N --start-number 30 --topo-order
#Patch030: 0030-testsuite-dbus-element-handling-Use-external-script.patch
#Patch031: 0031-testsuite-reporter-upload-ssh-keys-Don-t-test-curl-o.patch
#Patch032: 0032-testsuite-abrt-action-ureport-Port-fakefaf-to-Python.patch
#Patch033: 0033-testsuite-bugzilla-private-reports-Port-pyserve-to-P.patch
#Patch034: 0034-testsuite-ureport-attachments-Port-pyserve-to-Python.patch
#Patch035: 0035-testsuite-upload-ftp-Drop-in-tree-copy-of-pyftpdlib.patch
#Patch036: 0036-testsuite-rhts-test-Port-pyserve-to-Python-3.patch
#Patch037: 0037-testsuite-dumpdir_completeness-Batch-import-keys.patch
#Patch038: 0038-testsuite-Add-initial-test-order-for-RHEL-8.patch
#Patch039: 0039-testsuite-bugzilla-bt-reattach-Port-pyserve-to-Pytho.patch
#Patch040: 0040-testsuite-reporter-mantisbt-Port-pyserve-to-Python3.patch
#Patch041: 0041-testsuite-reporter-mantisbt-Fix-query-header.patch
#Patch042: 0042-testsuite-abrt-action-ureport-Fix-fakefaf.py.patch
#Patch043: 0043-testsuite-aux-Remove-Python-3-related-packages.patch
#Patch044: 0044-aux-lib.sh-add-generate_python3_segfault.patch
#Patch045: 0045-dont-blame-interpret-switch-to-generate_python3_segf.patch
#Patch046: 0046-duptest-core_backtrace-use-python3-on-rhel8.patch
#Patch047: 0047-ureport-auth-modify-a-pattern-to-match-error-message.patch
#Patch048: 0048-testsuite-Add-abrt-auto-reporting-sanity-authenticat.patch
#Patch049: 0049-runtests-new-test-for-PrivateReports.patch
#Patch050: 0050-dumpoops-make-sure-hostname-matches-in-oops_full_hos.patch
#Patch051: 0051-oops-processing-fixed-oops1.test-handling.-reworked-.patch
#Patch052: 0052-meaningful-logs-check-relative-counts-of-lines-inste.patch
#Patch053: 0053-non-fatal-mce-prepare-oops1.test-from-template-befor.patch
#Patch054: 0054-oops-processing-fix-for-rhel-8.patch
#Patch055: 0055-dumpoops-remove-sed-of-file-not-existing-and-not-nee.patch
Patch056: 0056-a-a-list-dsos-Fix-decoding-of-strings-from-rpm.patch
#git format-patch 2.10.9-11.el8 -N --start-number 57 --topo-order
Patch057: 0057-a-a-save-package-data-Use-regexps-to-match-interpret.patch
Patch058: 0058-harvest_vmcore-Fix-missing-argument-error-during-del.patch
#git format-patch 2.10.9-12.el8 -N --start-number 59 --topo-order
#Patch059: 0059-abrtd-infinite-event-loop-remove-unnecesary-from-REs.patch
#Patch060: 0060-spec-Revert-libreport-dependency-change.patch
#Patch061: 0061-Revert-spec-Revert-libreport-dependency-change.patch
#Patch062: 0062-spec-Revert-libreport-dependency-change.patch
#Patch063: 0063-spec-Don-t-build-with-RHTS-bits-on-CentOS.patch
#Patch064: 0064-dont-blame-interpret-Rename-and-redo.patch
#Patch065: 0065-tests-aux-lib-Add-remove_problem_directory.patch
Patch066: 0066-cli-Add-a-shebang.patch
Patch067: 0067-shellcheck-Use-.-instead-of-legacy-backticked.patch
Patch068: 0068-shellcheck-Suppress-shellcheck-warning-SC1090.patch
Patch069: 0069-shellcheck-Check-exit-code-directly-with-if-mycmd.patch
Patch070: 0070-shellcheck-Use-command-instead-of-type.patch
#git format-patch 2.10.9-13.el8 --no-numbered --start-number=71 --topo-order
Patch071: 0071-plugin-general-from-sos-has-been-split-into-two-new-.patch
#git format-patch 2.10.9-14.el8 --no-numbered --start-number=72 --topo-order
Patch072: 0072-sos-use-services-instead-of-startup.patch
#git format-patch 2.10.9-16.el8 --no-numbered --start-number=73 --topo-order
#Patch0073: 0073-setgid-instead-of-setuid-the-abrt-action-install-deb.patch
#Patch0074: 0074-remove-old-transition-postscriptlet.patch
#Patch0075: 0075-make-sure-that-former-caches-are-group-writable.patch
#Patch0076: 0076-abrt-action-install-debuginfo-Fix-variable-reference.patch
#Patch0077: 0077-Revert-abrt-action-install-debuginfo-Fix-variable-re.patch
#Patch0078: 0078-Revert-make-sure-that-former-caches-are-group-writab.patch
#Patch0079: 0079-Revert-remove-old-transition-postscriptlet.patch
#Patch0080: 0080-Revert-setgid-instead-of-setuid-the-abrt-action-inst.patch
#Patch0081: 0081-Revert-a-a-install-debuginfo-Clean-cache-if-we-need-.patch
Patch0082: 0082-setgid-instead-of-setuid-the-abrt-action-install-deb.patch
Patch0083: 0083-remove-old-transition-postscriptlet.patch
Patch0084: 0084-make-sure-that-former-caches-are-group-writable.patch
Patch0085: 0085-abrt-action-install-debuginfo-Fix-variable-reference.patch
Patch0086: 0086-plugins-sosreport_event-Rename-nfsserver-plugin.patch
# git format-patch 2.10.9-19.el8 --no-numbered --start-number=87 --topo-order
Patch0087: 0087-plugins-abrt-action-install-debuginfo-Fix-reference.patch
Patch0090: 0090-skip-journal-reporting.patch
# rhbz#2137499: Update sosreport command line call.
Patch0091: 0091-plugins-Update-sosreport-event.patch
# git format-patch -1 a58e1fb2 --start-number=92
Patch0092: 0092-abrt-dump-oops-Fix-vmcore-call-trace-parsing.patch

# autogen.sh is need to regenerate all the Makefile files
Patch1000: 1000-Add-autogen.sh.patch

BuildRequires: %{dbus_devel}
BuildRequires: gtk3-devel
BuildRequires: glib2-devel >= 2.43
BuildRequires: rpm-devel >= 4.6
BuildRequires: desktop-file-utils
BuildRequires: libnotify-devel
#why? BuildRequires: file-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: %{nss_devel}
BuildRequires: asciidoc
BuildRequires: doxygen
BuildRequires: xmlto
BuildRequires: libreport-devel >= %{libreport_ver}
BuildRequires: satyr-devel >= %{satyr_ver}
BuildRequires: augeas
BuildRequires: libselinux-devel
BuildRequires: sed
%if %{with python2}
BuildRequires: python2-devel
BuildRequires: python2-systemd
BuildRequires: python2-argcomplete
BuildRequires: python2-argh
BuildRequires: python2-humanize
%endif # with python2
%if %{with python3}
BuildRequires: python3-devel
BuildRequires: python3-systemd
BuildRequires: python3-argcomplete
BuildRequires: python3-argh
BuildRequires: python3-humanize
%endif # with python3
BuildRequires: git

Requires: libreport >= %{libreport_ver}
Requires: satyr >= %{satyr_ver}
# these only exist on suse
%if 0%{?suse_version}
BuildRequires: dbus-1-glib-devel
Requires: dbus-1-glib
%endif

%{?systemd_requires}
Requires: systemd
Requires: %{name}-libs = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
Requires(pre): %{shadow_utils}
%if %{with python2}
Requires: python2-augeas
Requires: python2-dbus
%endif # with python2
%if %{with python3}
Requires: python3-augeas
Requires: python3-dbus
%endif # with python3
%ifarch aarch64 i686 x86_64
Requires: dmidecode
%endif
Requires: libreport-plugin-ureport
#%if 0%{?rhel}
#Requires: libreport-plugin-rhtsupport
#%endif
%if 0%{?fedora}
Requires: libreport-plugin-systemd-journal
%endif

#gui
BuildRequires: libreport-gtk-devel >= %{libreport_ver}
BuildRequires: gsettings-desktop-schemas-devel >= 3.15
#addon-ccpp
BuildRequires: gdb-headless
BuildRequires: libcap-devel
#addon-kerneloops
BuildRequires: systemd-devel
BuildRequires: %{libjson_devel}
%if %{with bodhi}
# plugin-bodhi
BuildRequires: libreport-web-devel >= %{libreport_ver}
%endif
#desktop
#Default config of addon-ccpp requires gdb
BuildRequires: gdb-headless
#dbus
BuildRequires: polkit-devel
%if %{with python2}
#python2-abrt
BuildRequires: python2-sphinx
BuildRequires: python2-libreport
#python2-abrt-doc
BuildRequires: python2-devel
%endif # with python2
%if %{with python3}
#python3-abrt
BuildRequires: python3-nose
BuildRequires: python3-sphinx
BuildRequires: python3-libreport
#python3-abrt-doc
BuildRequires: python3-devel
%endif # with python3

%description
%{name} is a tool to help users to detect defects in applications and
to create a bug report with all information needed by maintainer to fix it.
It uses plugin system to extend its functionality.

%package libs
Summary: Libraries for %{name}

%description libs
Libraries for %{name}.

%package devel
Summary: Development libraries for %{name}
Requires: abrt-libs = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%package gui-libs
Summary: Libraries for %{name}-gui
Requires: %{name}-libs = %{version}-%{release}

%description gui-libs
Libraries for %{name}-gui.

%package gui-devel
Summary: Development libraries for %{name}-gui
Requires: abrt-gui-libs = %{version}-%{release}

%description gui-devel
Development libraries and headers for %{name}-gui.

%package gui
Summary: %{name}'s gui
Requires: %{name} = %{version}-%{release}
Requires: %{name}-dbus = %{version}-%{release}
Requires: gnome-abrt
Requires: gsettings-desktop-schemas >= 3.15
# we used to have abrt-applet, now abrt-gui includes it:
Provides: abrt-applet = %{version}-%{release}
Obsoletes: abrt-applet < 0.0.5
Conflicts: abrt-applet < 0.0.5
Requires: abrt-libs = %{version}-%{release}
Requires: abrt-gui-libs = %{version}-%{release}

%description gui
GTK+ wizard for convenient bug reporting.

%package addon-coredump-helper
Summary: %{name}'s /proc/sys/kernel/core_pattern helper
Requires: abrt-libs = %{version}-%{release}

%description addon-coredump-helper
This package contains hook for C/C++ crashed programs.

%package addon-ccpp
Summary: %{name}'s C/C++ addon
Requires: cpio
Requires: gdb-headless
Requires: elfutils
%if 0%{!?rhel:1}
# abrt-action-perform-ccpp-analysis wants to run analyze_RetraceServer:
Requires: %{name}-retrace-client
%endif
Requires: %{name} = %{version}-%{release}
Requires: %{name}-addon-coredump-helper = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
%if %{with python2}
Requires: python2-libreport
%endif # with python2
%if %{with python3}
Requires: python3-libreport
%endif # with python3
Requires: rpm >= 4.14.2-11

%description addon-ccpp
This package contains %{name}'s C/C++ analyzer plugin.

%package addon-upload-watch
Summary: %{name}'s upload addon
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}

%description addon-upload-watch
This package contains hook for uploaded problems.

%package retrace-client
Summary: %{name}'s retrace client
Requires: %{name} = %{version}-%{release}
Requires: xz
Requires: tar
Requires: p11-kit-trust

%description retrace-client
This package contains the client application for Retrace server
which is able to analyze C/C++ crashes remotely.

%package addon-kerneloops
Summary: %{name}'s kerneloops addon
Requires: curl
Requires: %{name} = %{version}-%{release}
%if 0%{!?rhel:1}
Requires: libreport-plugin-kerneloops >= %{libreport_ver}
%endif
Requires: abrt-libs = %{version}-%{release}

%description addon-kerneloops
This package contains plugin for collecting kernel crash information from
system log.

%package addon-xorg
Summary: %{name}'s Xorg addon
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}

%description addon-xorg
This package contains plugin for collecting Xorg crash information from Xorg
log.

%package addon-vmcore
Summary: %{name}'s vmcore addon
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops
Requires: kexec-tools
%if %{with python2}
Requires: python2-abrt
Requires: python2-augeas
%endif # with python2
%if %{with python3}
Requires: python3-abrt
Requires: python3-augeas
%endif # with python3
Requires: util-linux

%description addon-vmcore
This package contains plugin for collecting kernel crash information from
vmcore files.

%package addon-pstoreoops
Summary: %{name}'s pstore oops addon
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
Requires: abrt-addon-kerneloops
Obsoletes: abrt-addon-uefioops

%description addon-pstoreoops
This package contains plugin for collecting kernel oopses from pstore storage.

%if %{with bodhi}
%package plugin-bodhi
Summary: %{name}'s bodhi plugin
Requires: %{name} = %{version}-%{release}
Obsoletes: libreport-plugin-bodhi > 0.0.1
Provides: libreport-plugin-bodhi = %{version}-%{release}

%description plugin-bodhi
Search for a new updates in bodhi server.
%endif

%if %{with python2}
%package -n python2-abrt-addon
Summary: %{name}'s addon for catching and analyzing Python exceptions
Requires: %{name} = %{version}-%{release}
Requires: python2-systemd
Requires: python2-abrt
# Remove before F30
Provides: abrt-addon-python = %{version}-%{release}
Provides: abrt-addon-python%{?_isa} = %{version}-%{release}
Obsoletes: abrt-addon-python < 2.10.4

%description -n python2-abrt-addon
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package -n python2-abrt-container-addon
Summary: %{name}'s container addon for catching Python 2 exceptions
Conflicts: python2-abrt-addon
Requires: container-exception-logger

%description -n python2-abrt-container-addon
This package contains python 2 hook and handling uncaught exception in python 2
programs in container.
%endif # with python2

%if %{with python3}
%package -n python3-abrt-addon
Summary: %{name}'s addon for catching and analyzing Python 3 exceptions
Requires: %{name} = %{version}-%{release}
Requires: python3-systemd
Requires: python3-abrt
# Remove before F30
Provides: abrt-addon-python3 = %{version}-%{release}
Provides: abrt-addon-python3%{?_isa} = %{version}-%{release}
Obsoletes: abrt-addon-python3 < 2.10.4

%description -n python3-abrt-addon
This package contains python 3 hook and python analyzer plugin for handling
uncaught exception in python 3 programs.

%package -n python3-abrt-container-addon
Summary: %{name}'s container addon for catching Python 3 exceptions
Conflicts: python3-abrt-addon
Requires: container-exception-logger

%description -n python3-abrt-container-addon
This package contains python 3 hook and handling uncaught exception in python 3
programs in container.
%endif # with python3

%package plugin-sosreport
Summary: %{name}'s plugin for building automatic sosreports
Requires: sos
Requires: %{name} = %{version}-%{release}

%description plugin-sosreport
This package contains a configuration snippet to enable automatic generation
of sosreports for abrt events.

%package plugin-machine-id
Summary: %{name}'s plugin to generate machine_id based off dmidecode
Requires: %{name} = %{version}-%{release}

%description plugin-machine-id
This package contains a configuration snippet to enable automatic generation
of machine_id for abrt events.

%package tui
Summary: %{name}'s command line interface
Requires: %{name} = %{version}-%{release}
Requires: libreport-cli >= %{libreport_ver}
Requires: abrt-libs = %{version}-%{release}
Requires: abrt-dbus

%description tui
This package contains a simple command line client for processing abrt reports
in command line environment.

%if %{with python3}
%package cli-ng
Summary: %{name}'s improved command line interface
Requires: %{name} = %{version}-%{release}
Requires: libreport-cli >= %{libreport_ver}
Requires: abrt-libs = %{version}-%{release}
Requires: abrt-dbus
Requires: python3-abrt
Requires: abrt-addon-ccpp
Requires: python3-argh
Requires: python3-argcomplete
Requires: python3-humanize

%description cli-ng
New generation command line interface for ABRT
%endif # with python3

%package cli
Summary: Virtual package to make easy default installation on non-graphical environments
Requires: %{name} = %{version}-%{release}
Requires: abrt-tui
Requires: abrt-addon-kerneloops
Requires: abrt-addon-pstoreoops
Requires: abrt-addon-vmcore
Requires: abrt-addon-ccpp
%if %{with python2}
Requires: python2-abrt-addon
%endif # with python2
%if %{with python3}
Requires: python3-abrt-addon
%endif # with python3
Requires: abrt-addon-xorg
%if 0%{!?rhel}
Requires: abrt-retrace-client
%if %{with bodhi}
Requires: abrt-plugin-bodhi
%endif
%if 0%{!?suse_version:1}
Requires: libreport-plugin-bugzilla >= %{libreport_ver}
%endif
Requires: libreport-plugin-logger >= %{libreport_ver}
Requires: libreport-plugin-ureport >= %{libreport_ver}
%if 0%{?fedora}
Requires: libreport-fedora >= %{libreport_ver}
%endif
%endif

%description cli
Virtual package to install all necessary packages for usage from command line
environment.

%package desktop
Summary: Virtual package to make easy default installation on desktop environments
# This package gets installed when anything requests bug-buddy -
# happens when users upgrade Fn to Fn+1;
# or if user just wants "typical desktop installation".
# Installing abrt-desktop should result in the abrt which works without
# any tweaking in abrt.conf (IOW: all plugins mentioned there must be installed)
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops
Requires: abrt-addon-pstoreoops
Requires: abrt-addon-vmcore
Requires: abrt-addon-ccpp
%if %{with python2}
Requires: python2-abrt-addon
%endif # with python2
%if %{with python3}
Requires: python3-abrt-addon
%endif # with python3
Requires: abrt-addon-xorg
Requires: gdb-headless
Requires: abrt-gui
Requires: gnome-abrt
%if 0%{!?rhel}
Requires: abrt-retrace-client
%if %{with bodhi}
Requires: abrt-plugin-bodhi
%endif
%if 0%{!?suse_version:1}
Requires: libreport-plugin-bugzilla >= %{libreport_ver}
%endif
Requires: libreport-plugin-logger >= %{libreport_ver}
Requires: libreport-plugin-ureport >= %{libreport_ver}
%if 0%{?fedora}
Requires: libreport-fedora >= %{libreport_ver}
%endif
%endif
#Requires: abrt-plugin-firefox
Provides: bug-buddy = %{version}-%{release}

%description desktop
Virtual package to install all necessary packages for usage from desktop
environment.

%if %{with atomic}
%package atomic
Summary: Package to make easy default installation on Atomic hosts.
Requires: %{name}-addon-coredump-helper = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Conflicts: %{name}-addon-ccpp

%description atomic
Package to install all necessary packages for usage from Atomic
hosts.
%endif

%package dbus
Summary: ABRT DBus service
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}

%description dbus
ABRT DBus service which provides org.freedesktop.problems API on dbus and
uses PolicyKit to authorize to access the problem data.

%if %{with python2}
%package -n python2-abrt
Summary: ABRT Python API
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-dbus = %{version}-%{release}
Requires: python2-dbus
Requires: python2-libreport
%if 0%{?rhel:%{rhel} == 7}
Requires: python-gobject-base
%else
Requires: python2-gobject-base
%endif
%{?python_provide:%python_provide python2-abrt}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < 2.10.4

%description -n python2-abrt
High-level API for querying, creating and manipulating
problems handled by ABRT in Python.

%package -n python2-abrt-doc
Summary: ABRT Python API Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: python2-abrt = %{version}-%{release}
# Remove before F30
Provides: %{name}-python-doc = %{version}-%{release}
Obsoletes: %{name}-python-doc < 2.10.4

%description -n python2-abrt-doc
Examples and documentation for ABRT Python API.
%endif # with python2

%if %{with python3}
%package -n python3-abrt
Summary: ABRT Python 3 API
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-dbus = %{version}-%{release}
Requires: python3-dbus
Requires: python3-libreport
%{?python_provide:%python_provide python3-abrt}
# Remove before F30
Provides: %{name}-python3 = %{version}-%{release}
Provides: %{name}-python3%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python3 < 2.10.4
Requires: python3-gobject-base

%description -n python3-abrt
High-level API for querying, creating and manipulating
problems handled by ABRT in Python 3.

%package -n python3-abrt-doc
Summary: ABRT Python API Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
# Remove before F30
Provides: %{name}-python3-doc = %{version}-%{release}
Obsoletes: %{name}-python3-doc < 2.10.4

%description -n python3-abrt-doc
Examples and documentation for ABRT Python 3 API.
%endif # with python3

%package console-notification
Summary: ABRT console notification script
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}

%description console-notification
A small script which prints a count of detected problems when someone logs in
to the shell

%prep
# http://www.rpm.org/wiki/PackagerDocs/Autosetup
# Default '__scm_apply_git' is 'git apply && git commit' but this workflow
# doesn't allow us to create a new file within a patch, so we have to use
# 'git am' (see /usr/lib/rpm/macros for more details)
#%%define __scm_apply_git(qp:m:) %{__git} am --exclude doc/design --exclude doc/project/abrt.tex
%define __scm_apply_git(qp:m:) %{__git} am
%autosetup -S git

%build
export PYTHON_NOSE="%{__python3} -m nose"
./autogen.sh
autoconf

%define var_base_dir spool

CFLAGS="%{optflags} -Werror" %configure \
%if %{without python2}
        --without-python2 \
%endif # with python2
%if %{without python3}
        --without-python3 \
%endif # with python3
%if %{without bodhi}
        --without-bodhi \
%endif
%if %{without atomic}
        --without-atomic \
%endif
%if 0%{?rhel}
        --enable-suggest-autoreporting \
%endif
%ifnarch %{arm}
        --enable-native-unwinder \
%endif
        --with-defaultdumplocation=/var/%{var_base_dir}/abrt \
        --enable-doxygen-docs \
        --enable-dump-time-unwind \
        --disable-silent-rules

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT \
             PYTHON=%{__python3} \
             mandir=%{_mandir} \
             dbusabrtdocdir=%{_defaultdocdir}/%{name}-dbus%{docdirversion}/html/

%find_lang %{name}

# Switch hardcoded python3 shebangs into the %%{__python3} macro
sed -i '1s=^#!/usr/bin/python3\($\|\s\)=#!%{__python3}\1=' \
    %{buildroot}%{_sbindir}/abrt-harvest-pstoreoops \
    %{buildroot}%{_bindir}/abrt \
    %{buildroot}%{_bindir}/abrt-handle-upload \
    %{buildroot}%{_bindir}/abrt-action-analyze-core \
%if %{with bodhi}
    %{buildroot}%{_bindir}/abrt-action-find-bodhi-update \
%endif
    %{buildroot}%{_bindir}/abrt-action-install-debuginfo \
    %{buildroot}%{_bindir}/abrt-action-list-dsos \
    %{buildroot}%{_bindir}/abrt-action-notify \
    %{buildroot}%{_bindir}/abrt-action-perform-ccpp-analysis \
    %{buildroot}%{_libexecdir}/abrt-action-generate-machine-id \
    %{buildroot}%{_libexecdir}/abrt-action-ureport \
    %{buildroot}%{_libexecdir}/abrt-gdb-exploitable \
    %{buildroot}%{_sbindir}/abrt-harvest-vmcore \
    %{buildroot}%{_bindir}/abrt-action-analyze-vmcore \
    %{buildroot}%{_bindir}/abrt-action-check-oops-for-alt-component \
    %{buildroot}%{_bindir}/abrt-action-check-oops-for-hw-error \

# Remove byte-compiled python files generated by automake.
# automake uses system's python for all *.py files, even
# for those which needs to be byte-compiled with different
# version (python2/python3).
# rpm can do this work and use the appropriate python version.
find $RPM_BUILD_ROOT -name "*.py[co]" -delete

# remove all .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p $RPM_BUILD_ROOT/var/cache/abrt-di
mkdir -p $RPM_BUILD_ROOT/var/run/abrt
mkdir -p $RPM_BUILD_ROOT/var/%{var_base_dir}/abrt
mkdir -p $RPM_BUILD_ROOT/var/spool/abrt-upload
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/abrt

desktop-file-install \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
        src/applet/abrt-applet.desktop

ln -sf %{_datadir}/applications/abrt-applet.desktop ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart/

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

%check
make check|| {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    exit 1
}

%pre
#uidgid pair 173:173 reserved in setup rhbz#670231
%define abrt_gid_uid 173
getent group abrt >/dev/null || groupadd -f -g %{abrt_gid_uid} --system abrt
getent passwd abrt >/dev/null || useradd --system -g abrt -u %{abrt_gid_uid} -d /etc/abrt -s /sbin/nologin abrt
exit 0

%post
# $1 == 1 if install; 2 if upgrade
%systemd_post abrtd.service

%post addon-ccpp
%systemd_post abrt-ccpp.service
# migration from 2.14.1.18
if [ ! -e "%{_localstatedir}/cache/abrt-di/.migration-group-add" ]; then
  chmod -R g+w %{_localstatedir}/cache/abrt-di
  touch "%{_localstatedir}/cache/abrt-di/.migration-group-add"
fi

%systemd_post abrt-journal-core.service
%journal_catalog_update

%post addon-kerneloops
%systemd_post abrt-oops.service
%journal_catalog_update

%post addon-xorg
%systemd_post abrt-xorg.service
%journal_catalog_update

%if %{with python2}
%post -n python2-abrt-addon
%journal_catalog_update
%endif # with python2

%if %{with python3}
%post -n python3-abrt-addon
%journal_catalog_update
%endif # with python3

%post addon-vmcore
%systemd_post abrt-vmcore.service
%journal_catalog_update

%post addon-pstoreoops
%systemd_post abrt-pstoreoops.service

%post addon-upload-watch
%systemd_post abrt-upload-watch.service

%preun
%systemd_preun abrtd.service

%preun addon-ccpp
%systemd_preun abrt-ccpp.service
%systemd_preun abrt-journal-core.service

%preun addon-kerneloops
%systemd_preun abrt-oops.service

%preun addon-xorg
%systemd_preun abrt-xorg.service

%preun addon-vmcore
%systemd_preun abrt-vmcore.service

%preun addon-pstoreoops
%systemd_preun abrt-pstoreoops.service

%preun addon-upload-watch
%systemd_preun abrt-upload-watch.service

%postun
%systemd_postun_with_restart abrtd.service

%postun addon-ccpp
%systemd_postun_with_restart abrt-ccpp.service
%systemd_postun_with_restart abrt-journal-core.service

%postun addon-kerneloops
%systemd_postun_with_restart abrt-oops.service

%postun addon-xorg
%systemd_postun_with_restart abrt-xorg.service

%postun addon-vmcore
%systemd_postun_with_restart abrt-vmcore.service

%postun addon-pstoreoops
%systemd_postun_with_restart abrt-pstoreoops.service

%postun addon-upload-watch
%systemd_postun_with_restart abrt-upload-watch.service

%post gui
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%if %{with atomic}
%post atomic
if [ -f /etc/abrt/plugins/CCpp.conf ]; then
    mv /etc/abrt/plugins/CCpp.conf /etc/abrt/plugins/CCpp.conf.rpmsave.atomic || exit 1;
fi
ln -sf /etc/abrt/plugins/CCpp_Atomic.conf /etc/abrt/plugins/CCpp.conf
if [ -f /usr/share/abrt/conf.d/plugins/CCpp.conf ]; then
    mv /usr/share/abrt/conf.d/plugins/CCpp.conf /usr/share/abrt/conf.d/plugins/CCpp.conf.rpmsave.atomic || exit 1;
fi
ln -sf /usr/share/abrt/conf.d/plugins/CCpp_Atomic.conf /usr/share/abrt/conf.d/plugins/CCpp.conf
%systemd_post abrt-coredump-helper.service

%preun atomic
if [ -L /etc/abrt/plugins/CCpp.conf ]; then
    rm /etc/abrt/plugins/CCpp.conf
fi
if [ -L /usr/share/abrt/conf.d/plugins/CCpp.conf ]; then
    rm /usr/share/abrt/conf.d/plugins/CCpp.conf
fi
if [ -f /etc/abrt/plugins/CCpp.conf.rpmsave.atomic ]; then
    mv /etc/abrt/plugins/CCpp.conf.rpmsave.atomic /etc/abrt/plugins/CCpp.conf || exit 1
fi
if [ -f  /usr/share/abrt/conf.d/plugins/CCpp.conf.rpmsave.atomic ]; then
    mv /usr/share/abrt/conf.d/plugins/CCpp.conf.rpmsave.atomic /usr/share/abrt/conf.d/plugins/CCpp.conf || exit 1
fi

%postun atomic
%systemd_postun_with_restart abrt-coredump-helper.service
%endif # with atomic

%if 0%{?fedora} > 27 || 0%{?rhel} > 7
# ldconfigi and gtk-update-icon-cache is not needed
%else
%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post gui-libs -p /sbin/ldconfig

%postun gui-libs -p /sbin/ldconfig

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%endif

%posttrans
# update the old problem dirs to contain "type" element
service abrtd condrestart >/dev/null 2>&1 || :

%posttrans addon-ccpp
# Migrate from abrt-ccpp.service to abrt-journal-core.service
# 'systemctl preset abrt-ccpp.service abrt-journal-core.service'
# is done only for installation by %systemd_post macro but not for package
# upgrade. Following lines affect changes in Fedora preset files in case of
# package upgrade and also starts abrt-journal-core.service and stops
# abrt-ccpp.service if abrt-ccpp.service is running.
# All this has to be done only once because some users want to use
# abrt-ccpp.service instead of the default abrt-journal-core.service.
# Hence we introduced a %{_localstatedir}/lib/abrt/abrt-migrated file to
# mark the migration was done.
if test ! -f %{_localstatedir}/lib/abrt/abrt-migrated ; then
    systemctl --no-reload preset abrt-ccpp.service >/dev/null 2>&1 || : 
    systemctl --no-reload preset abrt-journal-core.service >/dev/null 2>&1 || :
    if service abrt-ccpp status >/dev/null 2>&1 ; then
        systemctl stop abrt-ccpp >/dev/null 2>&1 || :
        systemctl start abrt-journal-core >/dev/null 2>&1 || :
    fi
    touch %{_localstatedir}/lib/abrt/abrt-migrated
fi
systemctl try-restart abrt-journal-core >/dev/null 2>&1 || :
systemctl try-restart abrt-ccpp >/dev/null 2>&1 || :
# Regenerate core_bactraces because of missing crash threads
abrtdir=$(grep "DumpLocation" /etc/abrt/abrt.conf | cut -d'=' -f2 | tr -d ' ')
if test -d "$abrtdir"; then
    for DD in `find "$abrtdir" -mindepth 1 -maxdepth 1 -type d`
    do
        if test -f "$DD/analyzer" && grep -q "^CCpp$" "$DD/analyzer"; then
            /usr/bin/abrt-action-generate-core-backtrace -d "$DD" -- >/dev/null 2>&1 || :
            test -f "$DD/core_backtrace" && chown `stat --format=%U:abrt $DD` "$DD/core_backtrace" || :
        fi
    done
fi

%posttrans addon-kerneloops
service abrt-oops condrestart >/dev/null 2>&1 || :

%posttrans addon-xorg
service abrt-xorg condrestart >/dev/null 2>&1 || :

%posttrans addon-vmcore
service abrt-vmcore condrestart >/dev/null 2>&1 || :
# Copy the configuration file to plugin's directory
test -f /etc/abrt/abrt-harvest-vmcore.conf && {
    echo "Moving /etc/abrt/abrt-harvest-vmcore.conf to /etc/abrt/plugins/vmcore.conf"
    mv -b /etc/abrt/abrt-harvest-vmcore.conf /etc/abrt/plugins/vmcore.conf
}
exit 0

%posttrans addon-pstoreoops
service abrt-pstoreoops condrestart >/dev/null 2>&1 || :

%if 0%{?fedora} > 27
# gtk-update-icon-cache is not needed
%else
%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%posttrans dbus
# Force abrt-dbus to restart like we do with the other services
killall abrt-dbus >/dev/null 2>&1 || :

%files -f %{name}.lang
%doc README.md COPYING
%{_unitdir}/abrtd.service
%{_tmpfilesdir}/abrt.conf
%{_sbindir}/abrtd
%{_sbindir}/abrt-server
%{_sbindir}/abrt-auto-reporting
%{_libexecdir}/abrt-handle-event
%{_libexecdir}/abrt-action-ureport
%{_libexecdir}/abrt-action-save-container-data
%{_bindir}/abrt-handle-upload
%{_bindir}/abrt-action-notify
%{_mandir}/man1/abrt-action-notify.1*
%{_bindir}/abrt-action-save-package-data
%{_bindir}/abrt-watch-log
%{_bindir}/abrt-action-analyze-python
%{_bindir}/abrt-action-analyze-xorg
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.problems.daemon.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-action-save-package-data.conf
%{_datadir}/%{name}/conf.d/abrt-action-save-package-data.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/xorg.conf
%{_datadir}/%{name}/conf.d/plugins/xorg.conf
%{_mandir}/man5/abrt-xorg.conf.5*
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys.conf
%{_datadir}/%{name}/conf.d/gpg_keys.conf
%{_mandir}/man5/gpg_keys.conf.5*
%config(noreplace) %{_sysconfdir}/libreport/events.d/abrt_event.conf
%{_mandir}/man5/abrt_event.conf.5*
%config(noreplace) %{_sysconfdir}/libreport/events.d/smart_event.conf
%{_mandir}/man5/smart_event.conf.5*
%dir %attr(0751, root, abrt) %{_localstatedir}/%{var_base_dir}/%{name}
%dir %attr(0700, abrt, abrt) %{_localstatedir}/spool/%{name}-upload
# abrtd runs as root
%ghost %dir %attr(0755, root, root) %{_localstatedir}/run/%{name}
%ghost %attr(0666, -, -) %{_localstatedir}/run/%{name}/abrt.socket
%ghost %attr(0644, -, -) %{_localstatedir}/run/%{name}/abrtd.pid

%{_mandir}/man1/abrt-handle-upload.1*
%{_mandir}/man1/abrt-server.1*
%{_mandir}/man1/abrt-action-save-package-data.1*
%{_mandir}/man1/abrt-watch-log.1*
%{_mandir}/man1/abrt-action-analyze-python.1*
%{_mandir}/man1/abrt-action-analyze-xorg.1*
%{_mandir}/man1/abrt-auto-reporting.1*
%{_mandir}/man8/abrtd.8*
%{_mandir}/man5/abrt-action-save-package-data.conf.5*
# {_mandir}/man5/pyhook.conf.5*

%files libs
%{_libdir}/libabrt.so.*
%config(noreplace) %{_sysconfdir}/%{name}/abrt.conf
%{_datadir}/%{name}/conf.d/abrt.conf
%{_mandir}/man5/abrt.conf.5*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/conf.d
%dir %{_datadir}/%{name}/conf.d/plugins

# filesystem package should own /usr/share/augeas/lenses directory
%{_datadir}/augeas/lenses/abrt.aug

%files devel
# The complex pattern below (instead of simlpy *) excludes Makefile{.am,.in}:
%doc apidoc/html/*.{html,png,css,js}
%{_includedir}/abrt/abrt-dbus.h
%{_includedir}/abrt/hooklib.h
%{_includedir}/abrt/libabrt.h
%{_includedir}/abrt/problem_api.h
%{_libdir}/libabrt.so
%{_libdir}/pkgconfig/abrt.pc

%files gui-libs
%{_libdir}/libabrt_gui.so.*

%files gui-devel
%{_includedir}/abrt/abrt-config-widget.h
%{_includedir}/abrt/system-config-abrt.h
%{_libdir}/libabrt_gui.so
%{_libdir}/pkgconfig/abrt_gui.pc

%files gui
%dir %{_datadir}/%{name}
# all glade, gtkbuilder and py files for gui
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/status/*
%{_datadir}/%{name}/icons/hicolor/*/status/*
%{_datadir}/%{name}/ui/*
%{_bindir}/abrt-applet
%{_bindir}/system-config-abrt
#%%{_bindir}/test-report
%{_datadir}/applications/abrt-applet.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/abrt-applet.desktop
%{_mandir}/man1/abrt-applet.1*
%{_mandir}/man1/system-config-abrt.1*

%files addon-coredump-helper
%{_libexecdir}/abrt-hook-ccpp
%{_sbindir}/abrt-install-ccpp-hook

%files addon-ccpp
%dir %attr(0775, abrt, abrt) %{_localstatedir}/cache/abrt-di
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%{_datadir}/%{name}/conf.d/plugins/CCpp.conf
%{_mandir}/man5/abrt-CCpp.conf.5*
%{_libexecdir}/abrt-gdb-exploitable
%{_journalcatalogdir}/abrt_ccpp.catalog
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_ccpp_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_journal_ccpp_format.conf
%{_unitdir}/abrt-ccpp.service
%{_unitdir}/abrt-journal-core.service

%dir %{_localstatedir}/lib/abrt

# attr(2755) ~= SETGID
%attr(2755, abrt, abrt) %{_libexecdir}/abrt-action-install-debuginfo-to-abrt-cache

%{_bindir}/abrt-action-analyze-c
%{_bindir}/abrt-action-trim-files
%{_bindir}/abrt-action-analyze-core
%{_bindir}/abrt-action-analyze-vulnerability
%{_bindir}/abrt-action-install-debuginfo
%{_bindir}/abrt-action-generate-backtrace
%{_bindir}/abrt-action-generate-core-backtrace
%{_bindir}/abrt-action-analyze-backtrace
%{_bindir}/abrt-action-list-dsos
%{_bindir}/abrt-action-perform-ccpp-analysis
%{_bindir}/abrt-action-analyze-ccpp-local
%{_bindir}/abrt-dump-journal-core
%config(noreplace) %{_sysconfdir}/libreport/events.d/ccpp_event.conf
%{_mandir}/man5/ccpp_event.conf.5*
%config(noreplace) %{_sysconfdir}/libreport/events.d/gconf_event.conf
%{_mandir}/man5/gconf_event.conf.5*
%config(noreplace) %{_sysconfdir}/libreport/events.d/vimrc_event.conf
%{_mandir}/man5/vimrc_event.conf.5*
%{_datadir}/libreport/events/analyze_CCpp.xml
%{_datadir}/libreport/events/analyze_LocalGDB.xml
%{_datadir}/libreport/events/collect_xsession_errors.xml
%{_datadir}/libreport/events/collect_GConf.xml
%{_datadir}/libreport/events/collect_vimrc_user.xml
%{_datadir}/libreport/events/collect_vimrc_system.xml
%{_datadir}/libreport/events/post_report.xml
%{_mandir}/man*/abrt-action-analyze-c.*
%{_mandir}/man*/abrt-action-trim-files.*
%{_mandir}/man*/abrt-action-generate-backtrace.*
%{_mandir}/man*/abrt-action-generate-core-backtrace.*
%{_mandir}/man*/abrt-action-analyze-backtrace.*
%{_mandir}/man*/abrt-action-list-dsos.*
%{_mandir}/man*/abrt-install-ccpp-hook.*
%{_mandir}/man*/abrt-action-install-debuginfo.*
%{_mandir}/man*/abrt-action-analyze-ccpp-local.*
%{_mandir}/man*/abrt-action-analyze-core.*
%{_mandir}/man*/abrt-action-analyze-vulnerability.*
%{_mandir}/man*/abrt-action-perform-ccpp-analysis.*
%{_mandir}/man1/abrt-dump-journal-core.1*

%files addon-upload-watch
%{_sbindir}/abrt-upload-watch
%{_unitdir}/abrt-upload-watch.service
%{_mandir}/man*/abrt-upload-watch.*


%files retrace-client
%{_bindir}/abrt-retrace-client
%{_mandir}/man1/abrt-retrace-client.1*
%config(noreplace) %{_sysconfdir}/libreport/events.d/ccpp_retrace_event.conf
%{_mandir}/man5/ccpp_retrace_event.conf.5*
%{_datadir}/libreport/events/analyze_RetraceServer.xml

%files addon-kerneloops
%config(noreplace) %{_sysconfdir}/libreport/events.d/koops_event.conf
%{_journalcatalogdir}/abrt_koops.catalog
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_koops_format.conf
%{_mandir}/man5/koops_event.conf.5*
%config(noreplace) %{_sysconfdir}/%{name}/plugins/oops.conf
%{_datadir}/%{name}/conf.d/plugins/oops.conf
%{_unitdir}/abrt-oops.service

%dir %{_localstatedir}/lib/abrt

%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-dump-journal-oops
%{_bindir}/abrt-action-analyze-oops
%{_mandir}/man1/abrt-dump-oops.1*
%{_mandir}/man1/abrt-dump-journal-oops.1*
%{_mandir}/man1/abrt-action-analyze-oops.1*
%{_mandir}/man5/abrt-oops.conf.5*

%files addon-xorg
%config(noreplace) %{_sysconfdir}/libreport/events.d/xorg_event.conf
%{_journalcatalogdir}/abrt_xorg.catalog
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_xorg_format.conf
%{_mandir}/man5/xorg_event.conf.5*
%{_unitdir}/abrt-xorg.service
%{_bindir}/abrt-dump-xorg
%{_bindir}/abrt-dump-journal-xorg
%{_mandir}/man1/abrt-dump-xorg.1*
%{_mandir}/man1/abrt-dump-journal-xorg.1*

%files addon-vmcore
%config(noreplace) %{_sysconfdir}/libreport/events.d/vmcore_event.conf
%{_mandir}/man5/vmcore_event.conf.5*
%config(noreplace) %{_sysconfdir}/%{name}/plugins/vmcore.conf
%{_datadir}/%{name}/conf.d/plugins/vmcore.conf
%{_datadir}/libreport/events/analyze_VMcore.xml
%{_unitdir}/abrt-vmcore.service
%{_sbindir}/abrt-harvest-vmcore
%{_bindir}/abrt-action-analyze-vmcore
%{_bindir}/abrt-action-check-oops-for-alt-component
%{_bindir}/abrt-action-check-oops-for-hw-error
%{_mandir}/man1/abrt-harvest-vmcore.1*
%{_mandir}/man5/abrt-vmcore.conf.5*
%{_mandir}/man1/abrt-action-analyze-vmcore.1*
%{_mandir}/man1/abrt-action-check-oops-for-hw-error.1*
%{_journalcatalogdir}/abrt_vmcore.catalog
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_vmcore_format.conf

%files addon-pstoreoops
%{_unitdir}/abrt-pstoreoops.service
%{_sbindir}/abrt-harvest-pstoreoops
%{_bindir}/abrt-merge-pstoreoops
%{_mandir}/man1/abrt-harvest-pstoreoops.1*
%{_mandir}/man1/abrt-merge-pstoreoops.1*

%if %{with python2}
%files -n python2-abrt-addon
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python.conf
%{_datadir}/%{name}/conf.d/plugins/python.conf
%{_mandir}/man5/abrt-python.conf.5*
%config(noreplace) %{_sysconfdir}/libreport/events.d/python_event.conf
%{_journalcatalogdir}/abrt_python.catalog
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_python_format.conf
%{_mandir}/man5/python_event.conf.5*
%{python_sitearch}/abrt.pth
%{python_sitearch}/abrt_exception_handler.*

%files -n python2-abrt-container-addon
%{python_sitearch}/abrt_container.pth
%{python_sitearch}/abrt_exception_handler_container.*
%endif # with python2

%if %{with python3}
%files -n python3-abrt-addon
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python3.conf
%{_datadir}/%{name}/conf.d/plugins/python3.conf
%{_mandir}/man5/abrt-python3.conf.5*
%config(noreplace) %{_sysconfdir}/libreport/events.d/python3_event.conf
%{_journalcatalogdir}/abrt_python3.catalog
%config(noreplace) %{_sysconfdir}/libreport/plugins/catalog_python3_format.conf
%{_mandir}/man5/python3_event.conf.5*
%{python3_sitearch}/abrt3.pth
%{python3_sitearch}/abrt_exception_handler3.py
%{python3_sitearch}/__pycache__/abrt_exception_handler3.*

%files -n python3-abrt-container-addon
%{python3_sitearch}/abrt3_container.pth
%{python3_sitearch}/abrt_exception_handler3_container.py
%{python3_sitearch}/__pycache__/abrt_exception_handler3_container.*
%endif # with python3

%files plugin-sosreport
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/sosreport_event.conf

%files plugin-machine-id
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/machine-id_event.conf
%{_libexecdir}/abrt-action-generate-machine-id

%files cli

%files tui
%{_bindir}/abrt-cli
%{_mandir}/man1/abrt-cli.1*

%if %{with python3}
%files cli-ng
%config(noreplace) %{_sysconfdir}/bash_completion.d/abrt.bash_completion
%{_bindir}/abrt
%{python3_sitearch}/abrtcli/
%{_mandir}/man1/abrt.1*
%endif # with python3

%files desktop

%if %{with atomic}
%files atomic
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp_Atomic.conf
%{_unitdir}/abrt-coredump-helper.service
%{_datadir}/%{name}/conf.d/plugins/CCpp_Atomic.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-action-save-package-data.conf
%{_bindir}/abrt-action-save-package-data
%{_mandir}/man1/abrt-action-save-package-data.1*
%{_mandir}/man5/abrt-action-save-package-data.conf.5*
%endif

%if %{with bodhi}
%files plugin-bodhi
%{_bindir}/abrt-bodhi
%{_bindir}/abrt-action-find-bodhi-update
%config(noreplace) %{_sysconfdir}/libreport/events.d/bodhi_event.conf
%{_datadir}/libreport/events/analyze_BodhiUpdates.xml
%{_mandir}/man1/abrt-bodhi.1*
%{_mandir}/man1/abrt-action-find-bodhi-update.1*
%endif

%files dbus
%{_sbindir}/abrt-dbus
%{_sbindir}/abrt-configuration
%{_mandir}/man8/abrt-dbus.8*
%{_mandir}/man8/abrt-configuration.8*
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-abrt.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.Entry.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.Session.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.Task.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.abrt.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.ccpp.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.oops.xml
%if %{with python2}
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.python.xml
%endif # with python2
%if %{with python3}
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.python3.xml
%endif # with python3
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.vmcore.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.xorg.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.problems.service
%{_datadir}/dbus-1/system-services/com.redhat.problems.configuration.service
%{_datadir}/polkit-1/actions/abrt_polkit.policy
%dir %{_defaultdocdir}/%{name}-dbus%{docdirversion}/
%dir %{_defaultdocdir}/%{name}-dbus%{docdirversion}/html/
%{_defaultdocdir}/%{name}-dbus%{docdirversion}/html/*.html
%{_defaultdocdir}/%{name}-dbus%{docdirversion}/html/*.css
%config(noreplace) %{_sysconfdir}/libreport/events.d/abrt_dbus_event.conf

%if %{with python2}
%files -n python2-abrt
%{python_sitearch}/problem/
%{_mandir}/man5/abrt-python.5*

%files -n python2-abrt-doc
%{python_sitelib}/problem_examples
%endif # with python2

%if %{with python3}
%files -n python3-abrt
%{python3_sitearch}/problem/
%{_mandir}/man5/abrt-python3.5*

%files -n python3-abrt-doc
%{python3_sitelib}/problem_examples
%endif # with python3

%files console-notification
%config(noreplace) %{_sysconfdir}/profile.d/abrt-console-notification.sh

%changelog
* Fri Dec 17 2023 Louis Abel <label@rockylinux.org> - 2.10.9-24.openela.0.1
- Remove RHT patches

* Thu Feb 16 2023 Matěj Grabovský <mgrabovs@redhat.com> - 2.10.9-24
- Revert part of patch for rhbz#2137499
- Resolves: rhbz#2137499

* Fri Feb 3 2023 Michal Fabík <mfabik@redhat.com> - 2.10.9-23
- Fix vmcore call trace parsing in kernel versions >=4.10
- Resolves: rhbz#1993225

* Tue Jan 31 2023 Matěj Grabovský <mgrabovs@redhat.com> - 2.10.9-22
- Update sos report command line
- Resolves: rhbz#2137499

* Wed Mar 31 2021 Michal Srb <michal@redhat.com> - 2.10.9-21
- Do not report problems to journal as we don't ship the journal reporter
- Resolves: rhbz#1844739

* Wed Aug 19 2020 - Ernestas Kulik <ekulik@redhat.com> - 2.10.9-20
- Something something patch for rhbz#1835388

* Tue Jun 30 2020 - Ernestas Kulik <ekulik@redhat.com> - 2.10.9-19
- Add another patch for #1846272

* Mon Jun 29 2020 - Michal Židek <mzidek@redhat.com> - 2.10.9-18
- Resolves: rhbz#1835388
- This is seccond commit to fix som mess with one missing patch and synchronize
  the internal gitlab patch numbers with this spec file

* Wed Jun 24 2020 - Michal Židek <mzidek@redhat.com> - 2.10.9-17
- Resolves: rhbz#1835388

* Mon Jun 22 2020 - Ernestas Kulik <ekulik@redhat.com> - 2.10.9-16
- Add another patch for #1846272

* Thu Jun 11 2020 Ernestas Kulik <ekulik@redhat.com> - 2.10.9-15
- Remove unintended line change in abrt_event.conf

* Thu Jun 11 2020 Ernestas Kulik <ekulik@redhat.com> - 2.10.9-14
- Add patch for #1846272

* Wed Jun 10 2020 Michal Židek <mzidek@redhat.com> - 2.10.9-13
- Resolves: rhbz#1658685
- shellcheck: Use command instead of type
- shellcheck: Check exit code directly with if mycmd
- shellcheck: Suppress shellcheck warning SC1090
- shellcheck: Use $(...) instead of legacy backticked
- cli: Add a shebang

* Wed Mar 11 2020 Ernestas Kulik <ekulik@redhat.com> - 2.10.9-12
- Fix #1798494, #1805728, #1809949

* Tue Jul 16 2019 Michal Fabik <mfabik@redhat.com> - 2.10.9-11
- a-a-list-dsos: Fix decoding of strings from rpm
Resolves: rhbz#1694970

* Fri Dec 7 2018 Martin Kutlak <mkutlak@redhat.com> - 2.10.9-10
- spec: Add-explicit-package-version-requirement-of-abrt-libs
- cli: get list of possible workflows for problem_data_t
- cli: mark the suggestion text for translation
- cli list: show a hint about creating a case in RHTS
Resolves: #1649753

* Fri Nov 30 2018 Martin Kutlak <mkutlak@redhat.com> - 2.10.9-9
- spec: turn on --enable-native-unwinder aarch64
- spec: enable addon-vmcore on aarch64
- daemon: Fix double closed fd race condition
- dbus: Add configuration for Python3
- Add autogen.sh
- Resolves: #1646569, #1651676, #1650619, #1650622, #1652676

* Tue Nov 20 2018 Martin Kutlak <mkutlak@redhat.com> - 2.10.9-8
- lib: Correct the syntax for gdb backtrace command
- Resolves: #1623960

* Tue Aug 14 2018 Petr Viktorin <pviktori@redhat.com> - 2.10.9-7
- Switch Python tests to use %%{__python3}
- Resolves: #1615505

* Fri Jun 15 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.9-6
- Switch hardcoded python3 shebangs into the %%{__python3}

* Fri Jun 15 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.9-5
- Set PYTHON to python3 during install

* Fri Jun 15 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.9-4
- ccpp: add %h and %e parameter into abrt-hook-ccpp
- Resovles: #1587891

* Thu May 24 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.9-3
- Remove dependency on deprecated nss-pem
- Resovles: #1578427

* Fri Apr 27 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.9-2
- fix python requires in spec file

* Fri Apr 27 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.9-1
- build: conditionalize the Python2 and Python3
- cli-ng,hooks,python-problem: Allow python to be optional at build time
- spec: fix ambiguous Python 2 dependency declarations
- plugins: a-a-g-machine-id use dmidecode command
- spec: use dmidecode instead of python3-dmidecode
- hooks: use container-exception-logger tool
- spec: container python hooks require cel
- hooks: do not write any additional logs
- a-a-s-package-data: add python3.7 to known Interpreters
- autogen: ignore abrt's python packages
- correctly parse buildrequires from spec file

* Wed Mar 21 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.8-1
- Translation updates
- spec: use Python3 as default in abrt-cli-ng
- cli-ng: use Python3 as default
- Add a new element 'interpreter' for python problems
- retrace-client: Require nss-pem

* Mon Feb 26 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.7-1
- Translation updates
- hooks: introduce docker hook for Python2
- hook: add type to Python3 container exception handler
- spec: introduce docker hook for Python2
- Add ABRT hexa stickers
- a-container-logger: workaround permission issue in minishift

* Mon Feb 19 2018 Matej Habrnal <mhabrnal@redhat.com> 2.10.6-1
- Translation updates
- hooks: introduce docker hook for Python3
- spec: introduce Python3 hook for container
- Remove deprecated is_error macro
- ldconfig is not needed in rawhide
- remove python_sitearch macro
- remove python_site macro
- move BuildRequires to top
- remove systemd-units and replace it with systemd macro
- remove init.d services
- a-h-event: Do not deduplicate different containers
- rpm: include epocho in package element if > 0

* Thu Nov 02 2017 Julius Milan <jmilan@redhat.com> 2.10.5-1
- Translation updates
- a-action-ureport: add option 'ProcessUnpackaged'
- spec: change dependency on python{2,3}-gobject
- applet: Additional changes to allow optional polkit
- doc: remove obsolete doxygen tags
- dbus: Additional changes to allow optional polkit
- cli-ng: Explicitly state python version in shebangs
- spec: rename python binary packages
- a-d-journal-core: Save mountinfo from journal
- a-d-journal-core: Save container cmdline
- logging: rename omitted log() to log_warning()

* Mon Aug 28 2017 Matej Habrnal <mhabrnal@redhat.com> 2.10.4-1
- Translation updates
- logging: rename log() to log_warning()
- Quick hack to fix build with rpm >= 4.14
- tests: Crash different binary in infinite event loop
- tests: Revert not sufficient fix
- tests: Reflect field changes in reporter-s-journal
- tests: Get docker-inspect while container is running
- cli,dbus: Allow polkit to be optional at build time
- spec: add dependency for python{3}-gobject
- a-d-journal-core: fix bad condition in creating reason msg
- a-d-journal-core: use pid of crashed process in dumpdir name
- changelog: update CHANGELOG.md

* Thu Jun 15 2017 Martin Kutlak <mkutlak@redhat.com> 2.10.3-1
- Translation updates
- applet: add a default action to a notification
- spec: require libreport-plugin-systemd-journal on Fedoras
- changing load location from bin to libexec
- changing location of abrt-action-save-container-data from bin to libexec
- koops: Improve not-reportable for oopses with taint flags
- This fixes #1173
- python: provide more information about exception
- abrt-journal: adapt to suspicious blacklist addition
- koops: add suspicious strings blacklist
- build: fix changelog adding in release target
- changelog: update CHANGELOG.md

* Tue Apr 25 2017 Matej Habrnal <mhabrnal@redhat.com> 2.10.2-1
- Translation updates
- spec: introduce migration to abrt-journal-core
- abrt_event: Save cpuinfo in problem directories
- koops: Improve fatal MCE check when dumping backtrace
- lib: typo in header
- Spelling fixes
- Python 3.6 invalid escape sequence deprecation fix
- koops_event: add check to restrict reporting of MCEs

* Thu Mar 16 2017 Matej Habrnal <mhabrnal@redhat.com> 2.10.1-1
- changelog: update CHANGELOG.md
- build: create tarball in release-* target
- spec: sosreport is not a package
- Fix Typo
- bodhi: Remove dependency on hawkey
- spec: Remove dependency on hawkey
- build: do not upload tarball to fedorahosted.org
- spec: do not use fedorahosted.org as source
- spec: install new plugins
- plugins: introduce Machine ID and SOS report
- Update CHANGELOG.md
- build: fix generating list of dependences in autogen.sh
- spec: start abrt-journal-core instead of abrt-ccpp
- build: fix scratch-build target
- a-a-ureport: fix calling of run_event_on_problem_dir
- spec: if using systemd, default to os-release ID for desktopvendor
- kernel: modify suspicious string "invalid opcode:"
- daemon: Allow rpm to be optional at build time
- spec: allow any compression of man pages
- spec: remove defattr
- spec: remove cleaning buildroot
- spec: use versioned provides
- spec: remove changelog entries older than 2 years
- remove Buildroot and Groups tags
- spec: recommend libreport-plugin-systemd-journal on Fedoras
- doc: document selinux change needed for automatic deletion of reports
- ccpp: tell gdb to analyze saved binary image

* Sat Dec 03 2016 Jakub Filak <jakub@thefilaks.net> 2.10.0-1
- Translation updates
- spec: bump required libreport and satyr versions
- build: make the release-* targets smarter
- Add CHANGELOG.md
- a-a-notify: set env var before run report_systemd-journal event
- use run_event_on_problem_dir() helper for running events
- notify: do not require package element
- spec: add catalog_journal_ccpp_format.conf file
- reporter-s-journal: add formatting file for abrt-journal-core analyser
- cli-ng: fix --fmt parameter
- python: create analyzer element in dumpdir
- abrt-action-list-dsos: fix typo in vendor variable name
- cli-ng: chown problem before reporting
- lib: stop printing out a debug message 'adding: '
- cli: print out the not-reportable reason
- cli: configure libreport to ignore not-reportable
- cli-ng: force reporting even if not-reportable
- cli-ng: introduce verbose argument
- Import GObject from gi.repository
- ccpp: configure package repositories for correct OS
- a-a-s-c-data: adapt to current docker
- daemon: don't drop problems from unknown containers
- a-a-s-c-data: correct detection of container type
- spec: install Bodhi event files
- bodhi: factor out Bodhi updates lookup into a solo event
- problems2: update the documentation
- a-a-analyze-python: create exception_type element
- a-a-analyze-xorg: create crash_function into dump dir
- koops: create crash_function element
- a-a-analyze-python: create crash_function element
- a-a-analyze-c: create crash_function element
- spec: add formatting files for reporter-systemd-journal
- reporter-systemd-journal: add formatting files
- vmcore: /var/tmp/abrt is no longer a dump location
- events: add event report_systemd-journal to all addons
- abrt-action-notify: notify to systemd journal
- spec: add abrt's catalog source files
- journal-catalog: add abrt's catalog source files
- ccpp: retain partial core_backtrace upon error
- ccpp: log waitpid errors
- ccpp: inform users about not supported unwinding
- ccpp: close stdin when we can let the process die
- daemon: properly shutdown socket connection
- daemon: close forgotten FD to /proc/[pid]
- ccpp: pass proc pid FD instead of pid to *_at fns
- ccpp+daemon: pass valid params to dd_open_item()
- python: remove unused functions from sysexcept hook
- build: add gettext-devel to sysdeps
- spec: add libcap-devel to BRs of addon-ccpp
- ccpp: avoid running elfutils under root
- Add abrt-action-analyze-vulnerability to .gitignore
- build: autoge.sh without args configures for debugging
- conf: increase MaxCrashReportsSize to 5GiB
- ccpp: fast dumping and abrt core limit
- CI: make debugging easier with more log messages
- doc: add a guide for ABRT hackers
- vmcore: fix an undefined variable on error path
- vmcore: read kdump.conf from an arbitrary location
- ccpp: use libreport 'at' functions
- ccpp: use abort() to exit in debug mode
- python2: stop generating dso_list in the process
- python: stop collecting ENVIRON in the process
- abrtd: details of processes from different PID NS
- abrtd: save interesting process details
- a-a-s-package-data: add python3.6 to known Interpreters
- spec: update gdb Requires
- tree-wide: make path to GDB configurable
- a-a-ureport: print out exit codes in verbose mode
- daemon: stop replacing analyzer with type

* Fri Sep 09 2016 Jakub Filak <jfilak@redhat.com> 2.9.0-1
- spec: install abrt_dbus_event.conf
- dbus: use Problems2 API in abrt-dbus
- dbus: Problems2 API implementation
- spec: install Problems2 interfaces
- dbus-doc: rewrite the XML to Problems2
- Fix memory leaks
- lib: introdcue a function checking post-create name
- abrtd: change HTTP response code for duplicate problems to 303
- autogen: fix typo in usage help string
- daemon: send base names from abrt-server to abrtd
- lib: normalize slashes of configured paths
- lib: make configuration paths alterable at runtime
- Add generated CCpp.conf to .gitignore
- abrt-bodhi: use CCpp PackageManager configuration directive from configure
- cli: introduce unsafe reporting for not-reporable problems
- handle-event: stop creating post-create lock
- daemon: trigger dump location cleanup after detection
- hook-ccpp: dump own core file in debug mode

* Mon Jul 18 2016 Matej Habrnal <mhabrnal@redhat.com> 2.8.2-1
- Translation updates
- abrt-hook-ccpp: Fix mismatching argument
- Allow selinux to be optional at build time
- vmcore: use findmnt to get mountpoint
- spec: add utils-linux to vmcore's Require
- vmcore: fix finding partitions by UUID and LABEL
- a-a-install-debuginfo: Exception may not have an argument errno
- koops: do not assume version has 3 levels
- Add ARM specific oops backtrace processing.
- examples: add oops-kernel-panic-hung-tasks-arm
- Add oops processing for kernel panics caused by hung tasks.
- abrt-hook-ccpp: save get_fsuid() return values in int variables

* Wed May 25 2016 Matej Habrnal <mhabrnal@redhat.com> 2.8.1-1
- a-dump-journal-xorg: allow *libexec/X* to be executable element
- a-dump-journal-xorg: add '_COMM=gnome-shell' to journal filter
- build: update pkg names for systemd
- a-d-journal-core: save core dump bytes from the journal field
- a-d-journal-core: support lz4 compressed core dump files
- a-a-install-debuginfo: do not try to split None
- doc: improve documentation of AllowedGroups, AllowedUsers and IgnoredPaths
- testcase: add serial field to uReport check
- a-a-install-debuginfo: correct handling of DebuginfoLocation
- a-a-s-container-data: update docker container ID parser
- abrt-hook-ccpp: drop saving of container env vars
- a-console-notification: do not leak variables
- a-retrace-client: format security
- daemon: avoid infinite crash loops
- spec: drop abrt-action-save-kernel-data bits
- spec: README -> README.md
- Add basic documentation
- a-a-install-debuginfo: fix BrokenPipe error
- a-a-install-debuginfo: make tmpdir variable global
- python3 addon: workaround a bug in traceback
- CCpp: turn off compat cores
- a-a-save-package-data: blacklist /usr/lib(64)/firefox/plugin-container
- Fix minor typo: possition -> position
- translations: add missing new line
- Translation updates
- translations: update zanata configuration
- ccpp: drop %e from the core_pattern
- Save Vendor and GPG Fingerprint

* Wed Feb 03 2016 Matej Habrnal <mhabrnal@redhat.com> 2.8.0-1
- a-a-save-package-data: do not blacklist firefox

* Tue Feb 02 2016 Matej Habrnal <mhabrnal@redhat.com> 2.7.2-1
- ccpp: bug fix - undefined variables
- a-a-c-o-f-hw-error: fix unicode error
- ccpp: use error_msg_ignore_crash() instead of error_msg()
- ccpp: add AllowedUsers and AllowedGroups feature
- doc: fix formatting in abrt.conf man page
- ccpp: use executable name from pid
- a-a-c-o-f-hw-error: do not crash on invalid unicode
- Use %s instead of %d.
- configui: link GUI library with libabrt.so
- Do not include system libabrt.h
- ccpp: unify log message of ignored crashes
- ccpp: add IgnoredPath option
- lib: check_recent_crash_file do not produce error_msg

* Mon Nov 23 2015 Jakub Filak <jfilak@redhat.com> 2.7.1-1
- spec: switch owner of the dump location to 'root'
- abrtd: switch owner of the dump location to 'root'
- lib: add convenient wrappers for ensuring writable dir
- ccpp: save abrt core files only to new files
- ccpp: ignore crashes of ABRT binaries if DebugLevel == 0
- conf: introduce DebugLevel
- a-a-i-d-to-abrt-cache: make own random temporary directory
- update .gitignore
- ccpp: make crashes of processes with locked memory not-reportable
- a-a-s-p-data: fix segfault if GPGKeysDir isn't configured
- a-dump-journal-xorg: make journal filter configurable
- doc: a-a-analyze-xorg fix path to conf file
- abrt-journal: use GList instead of char** in abrt_journal_set_journal_filter()
- xorg: introduce tool abrt-dump-journal-xorg
- abrt-xorg.service: change due to abrt-dump-journal-xorg
- journal: add function abrt_journal_get_next_log_line
- spec: add abrt-dump-journal-xorg to spec file
- xorg: rewrite skip_pfx() function to work with journal msgs
- xorg: introduce library xorg-utils
- dbus: ensure expected bytes width of DBus numbers
- a-d-journal-core: set root owner for created dump directory
- doc: add missing man page for abrt-dump-journal-core
- spec: add missing man page for abrt-dump-journal-core

* Thu Oct 15 2015 Matej Habrnal <mhabrnal@redhat.com> 2.7.0-1
- abrt-python: add problem.chown
- a-a-a-ccpp-local don't delete build_ids
- update .gitignore
- spec: add cli-ng
- cli-ng: initial

* Thu Oct 15 2015 Matej Habrnal <mhabrnal@redhat.com> 2.6.3-1
- bodhi: introduce wrapper for 'reporter-bugzilla -h' and 'abrt-bodhi'
- remove random code example from abrt-server
- spec: introduce abrt-action-find-bodhi-update
- api: fix pths -> paths rename
- handle-event: remove obsolete workaround
- remove 'not needed' code
- events: fix example wording
- doc: change /var/tmp/abrt to /var/spool/abrt
- doc: actualize core_pattern content in documentation
- doc: fix default DumpLocation in abrt.conf man page
- events: improve example
- events: comments not needed anymore
- abrt-retrace-client: use atoll for _size conversion
- abrt-dump-xorg: support Xorg log backtraces prefixed by (EE)
- runtests: more verbose fail in get_crash_path
- ureport-auth: force cp/mv when restoring configuration
- runtests: stick to new BZ password rules
- bodhi: fix typo in error messages
- bodhi: fix a segfault when testing an os-release opt for 'rawhide'
- doc: actualize the abrt-bodhi man page
- autogen: use dnf instead of yum to install dependencies
- bodhi: add parsing of error responses
- bodhi: add ignoring of Rawhide
- ccpp: do not break the reporting if a-bodhi fails
- spec: add hawkey to BRs of abrt-bodhi
- introduce bodhi2 to abrt-bodhi
- a-handle-upload: pass bytes to file.write()
- upload a problem data in the EVENT 'notify'
- turn off several post-create scripts for remote problems
- convert all 'ex.message' stmts to 'str(ex)'
- cli: don't start reporting of not-reportable problems
- a-a-s-p-d: add bash on the package blacklist
- correct usage of abrt-gdb-exploitable
- testsutie: first wait_for_hooks, then get_crash_path
- ccpp: use global TID
- ccpp: fix comment related to 'MakeCompatCore' option in CCpp.conf
- cli: fix testing of DBus API return codes
- dbus-api: unify reporting of errors
- doc: fix related to conditional compilation of man page
- abrt-auto-reporting: fix related to conditional compilation
- vmcore: read vmcore by chunks
- pass encoded Unicode to hashlib.sha1.update()
- abrt-merge-pstoreoops: merge files in descending order
- use gettext instead of lgettext in all python scripts
- gitignore: add a generated man page source file

* Fri Jul 17 2015 Jakub Filak <jfilak@redhat.com> 2.6.2-1
- applet: do not crash if the new problem has no command_line
- ccpp: do not crash if generate_core_backtrace fails
- abrt: Fixup component of select kernel backtraces
- abrtd: de-prioritize post-create event scripts
- spec: switch python Requires to python3
- switch all python scripts to python3
- spec: drop abrt-addon-python requires
- a-dump-oops: allow update the problem, if more then one oops found
- cli: use internal command impl in the command process
- cli: remove useless code from print_crash()
- cli: enable authetication for all commands

* Thu Jul 02 2015 Matej Habrnal <mhabrnal@redhat.com> 2.6.1-1
- dbus: keep the polkit authorization for all clients
- cli: enable polkit authentication on command line
- spec: --enable-dump-time-unwind by default
- ccpp: use TID to find crash thread
- spec: remove PyGObject from all Requires
- spec: update version of gdb because of -ascending
- lib: make it easier to find the backtrace of th crash thread
- ccpp: save TID in the file 'tid'
- ccpp: get TID from correct cmd line argument
- configui: add option always generate backtrace locally
- a-a-p-ccpp-analysis: use ask_yes_no_save_result instead of ask_yes_no_yesforever
- spec: use more appropriate url
- spec: abrt requires libreport-plugin-rhtsupport on rhel
- sosreport: add processor information to sosreport
- doc: update abrt-cli man page

* Tue Jun 09 2015 Jakub Filak <jfilak@redhat.com> 2.6.0-1
- spec: add abrt-dbus to Rs of abrt-python
- vmcore: use libreport dd API in the harvestor
- ccpp: don't save the system logs by default
- cli: exit with the number of unreported problems
- spec: restart abrt-dbus in posttrans
- cli: chown before reporting
- hooks: use root for owner of all dump directories
- ccpp: do not unlink failed and big user cores
- ccpp: include the system logs only with root's coredumps
- koops: don't save dmesg if kernel.dmesg_restrict=1
- daemon, dbus: allow only root to create CCpp, Koops, vmcore and xorg
- daemon: allow only root user to trigger the post-create
- daemon: harden against race conditions in DELETE
- ccpp: revert the UID/GID changes if user core fails
- a-a-i-d-t-a-cache: sanitize umask
- a-a-i-d-t-a-cache: sanitize arguments
- dbus: report invalid element names
- dbus: avoid race-conditions in tests for dum dir availability
- dbus: process only valid sub-directories of the dump location
- lib: add functions validating dump dir
- daemon: use libreport's function checking file name
- configure: move the default dump location to /var/spool
- ccpp: avoid overriding system files by coredump
- spec: add libselinux-devel to BRs
- ccpp: emulate selinux for creation of compat cores
- ccpp: harden dealing with UID/GID
- ccpp: do not use value of /proc/PID/cwd for chdir
- ccpp: do not override existing files by compat cores
- ccpp: stop reading hs_error.log from /tmp
- ccpp: fix symlink race conditions
- turn off exploring crashed process's root directories
- abrt-python: add proper PYTHONPATH to test shellscripts
- abrt-python: unify unknown problem type handling
- abrt-python: add not_reportable properties
- spec: remove analyzer to type conversion
- abrt-python: add Python3 problem type
- abrt-python: add id, short_id and path to problem
- abrt-python: add Problem.prefetch_data function
- abrt-python: handle reconnection gracefully
- config UI: Automatic reporting from GSettings
- doc, polkit: Spelling/grammar fixes
- applet: fix problem info double free
- a-a-s-p-d: add new known interpreter to conf file
- config UI: enable options without config files
- config UI: read glade from a local file first
- applet: migrate Autoreporting options to GSettings
- abrt-action-list-dsos: do not decode not existing object
- spec: add AUTHENTICATED_AUTOREPORTING conditional
- abrt-auto-reporting: require rhtsupport.conf file only on RHEL
- lib: add new kernel taint flags
- spec: add a dependency on abrt-dbus to abrt-cli
- cli: do not exit with segfault if dbus fails
- applet: switch to D-Bus methods
- upload: validate and sanitize uploaded dump directories

* Thu Apr 09 2015 Jakub Filak <jfilak@redhat.com> 2.5.1-1
- Translation updates
- problem: use 'type' element instead of 'analyzer'
- cli-status: don't return 0 if there is a problem older than limit
- journal-oops: add an argument accepting journal directory
- journal: open journal files from directory
- lib: don't expect kernel's version '2.6.*' or '3.*.*'
- cli: use the DBus methods for getting problem information
- libabrt: add wrappers TestElemeExists and GetInfo for one element
- dbus: add new method to test existence of an element
- libabrt: add new function fetching full problem data over DBus
- applet: use a shared function for getting problems over DBus
- vmcore: generate 'reason' file in all cases
- applet: Fix trivial indentation bug
- applet: Don't show report button for unpackaged programs
- applet: fix freeing of the notify problem list
- applet: get the list of problems through D-Bus service
- doc: D-Bus api: make desc of DeleteProblem clearer

* Wed Mar 18 2015 Jakub Filak <jfilak@redhat.com> 2.5.0-1
- applet: cast to correct type to fix a warrning
- applet: Use new problem_create_app_from_env() helper
- doc: add documentation for GetProblemData
- dbus: add a new method GetProblemData
- abrt_event: run save package data event even if component exists
- a-a-s-container-data: add a new argument --root
- spec: add a-a-s-package-data to abrt-atomic
- a-a-s-kernel-data: add --root argument
- journal-oops: add an argument similar to '--merge'
- spec: let configure generate the spec file
- ccpp: create the dump location from standalone hook
- retrace-client: stop failing on SSL2
- spec: changes for Atomic hosts
- add stuff necessary for Project Atomic
- Python 3 fixes
- ccpp: add support for multiple pkg mngrs
- Python 3 compatibility
- Revert "dbus: Allow admins to load problems without a password"
- dbus: Allow admins to load problems without a password
- abrtd: Don't allow users to list problems "by hand"
- spec: Don't allow users to list problems "by hand"
- spec: abrt-python requires libreport-python to build

* Fri Feb 20 2015 Jakub Filak <jfilak@redhat.com> 2.4.0-1
- spec: factor out core_pattern helper from addon-ccpp
- ccpp: standalone hook
- ccpp: save package data from hook in case of crash in container
- a-a-s-package-data: save data from artifical chroots
- spec: install containers tools
- containers: add utility collecting containers info
- ccpp: add support for containers
- spec: install the daemon's D-Bus configuration file
- daemon: add configuration enabling our name on the System bus
- daemon: get rid of own main loop
- init: set Type of abrtd.service to dbus
- applet: Use libreport's helper to find applications
- applet: Remove unused build information
- build: Fix pkg-config warning related to abrt.pc
- applet: Fix a massive leak in the app detection code
- applet: Remove left-over code from the systray icon
- applet: Use the easy way to detect empty lists
- applet: Fix a number of "problems" memory leaks
- applet: Make problem_info_t refcounted
- applet: If gnome-abrt isn't there, don't offer to report
- applet: Fix multiple notifications for the same problem
- applet: Always defer auto-reporting without a network
- applet: Don't ignore foreign problems if an admin
- applet: Rename problem variable to "pi"
- applet: Remove unused "flags" parameters
- applet: Completely ignore incomplete problems
- applet: Don't ignore repeat problems in the same app
- applet: Fix warning when crash doesn't happen in app
- applet: Remove unused functions
- applet: Remove unused flags
- applet: Rewrite notifications
- applet: Don't run full reports from the applet
- applet: Simplify "report" action
- applet: Add helper to guess .desktop for a cmdline
- applet: Get more details from the crash report
- applet: Ignore other people's problems for non-admins
- applet: Remove handling of "ignored" crashes
- applet: Remove specific persistent notifications handling
- applet: Rename applet to match gnome-abrt
- applet: Initialise libnotify on startup
- applet: Use g_new0() instead of xzalloc()
- applet: Use g_strdup_printf()/g_strdup()
- applet: Move variable inside block where it's used
- daemon: process unpackaged by default
- spec: fix abrt-applet requires
- applet: Fix memory leak in fork_exec_gui()
- applet: Detect whether gnome-abrt is available
- applet: Use GUI_EXECUTABLE macro
- autogen: move configure to the default case
- applet: Use GIO to launch gnome-abrt
- applet: Fix typo in "Oterwise"
- applet: Use symbolic icon instead of abrt's in notifications
- applet: Add some debug to new_dir_exists()
- applet: Require at least libnotify 0.7
- applet: Fix typo in "cuurent"
- applet: Don't defer sending out uReports
- applet: Use G_SOURCE_REMOVE in timeout callback
- spec: Bump required glib2 version
- applet: Use g_bus_own_name() for single-instance
- applet: Remove status icon
- applet: Use GDBus to filter crash signals
- applet: Remove XSMP support
- build: Launch configure after autogen.sh
- make: make some python depencies optional
- configure: fix typos
- configure: check for python-sphinx and nose
- spec: add gsettings-desktop-schemas to the build requires
- core: use updated dump_fd_info()
- switch from 'analyzer' to 'type'
- spec: install abrt-dump-journal-core stuff
- init: add abrt-journal-core service
- introduce abrt-dump-journal-core
- applet: Remove the automatic crash reporting message dialog
- applet: Remove pre-glib 2.32 code
- applet: Remove pointless custom signal handling
- applet: Use GNetworkMonitor instead of NM directly
- applet: Use GSettings to check whether to send uReports
- Rewrite journalctl invocations: replace grep/tail pipeline with journalctl builtins.
- Don't slurp unbounded amounts of data when invoking journalctl. Fixes #887.
- console-notifications: add timeout
- cli-status: use will_python_exception
- ccpp-hook: move utility functions to hooklib
- ccpp-hook: move /proc/[pid]/ utils to libreport
- abrt-journal: add functions for reading/saving journald state
- Do not use 'bool' in OPT_BOOL() macro : it expects 'int'
- daemon: Own a D-Bus name
- zanata: add gettext mappings
- auto-reporting: add options to specify auth type
- translations: move from transifex to zanata
- spec: add missing augeas dependency
- Only analyze vulnerabilities when coredump present
- abrt-install-ccpp-hook check configuration
- UUID from core backtrace if coredump is missing
- Create core backtrace in unwind hook
- abrt-hook-ccpp: minor refactoring
- vmcore: remove original vmcore file in the last step
- vmcore: catch IOErrors and OSErrors
- python: load the configuration from correct file
- Remove garbage from ccpp_event.conf
- spec: update the required gdb version
- gdb: make gdb aware of the abrt's debuginfo dir
- Revert "gdb: disable loading of auto-loaded files"
- spec: update the URL
- koops: improve 'reason' text for page faults
- sos: use all valuable plugins
- a-a-g-machine-id: do not print any error from the event handler
- a-a-g-machine-id: omit trailing new-line for one-liners only
- a-a-g-machine-id: suppress its failures in abrt_event.conf
- a-a-g-machine-id: add systemd's machine id
- applet: ensure writable dump directory before reporting
- make ABRT quieter
- journal-oops: use the length result of sd_journal_get_data()
- console-notifications: skip non-interactive shells
- applet: don't show duphash instead of component
- ureport: attach contact email if configured
- console-notifications: use return instead of exit
- Translation updates
- a-a-s-p-d: add firefox on the package blacklist
