Summary:                A friendly interactive shell
Name:                   fish

Version:                2.0.GIT
Release:                0%{?dist}

License:                GPL
Group:                  System Environment/Shells
URL:                    http://fishshell.com/

Source0:                http://ridiculousfish.com/shell/files/%{version}/%{name}-%{version}.tar.bz2

BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:          ncurses-devel gettext groff


# Locate correct build time-dependencies for providing X headers
%if "%fedora" >= "5"

# Modern Fedora version, has modular X.org
BuildRequires:          xorg-x11-proto-devel libX11-devel libXt-devel libXext-devel

%endif

%if "%fedora" < "5"
%if "%fedora" >= "3"

# Semi-old Fedora version, has non-modular X.org
BuildRequires:          xorg-x11-devel

%endif
%endif

%if 0%{?fedora}
%if "%fedora" < "3"

# Ancient Fedora version, has XFree86
BuildRequires:          XFree86-devel

%endif
%else

# The %fedora variable has not been correctly defined, or this is is
# not a Fedora system, try guessing BuildRequires by looking at the
# directory structure
%define xinclude /usr%(if [ -d /usr/X11R6/include ]; then echo /X11R6; fi)/include
BuildRequires:          %{xinclude}/X11/StringDefs.h, %{xinclude}/X11/Xlib.h
BuildRequires:          %{xinclude}/X11/Intrinsic.h,  %{xinclude}/X11/Xatom.h

%endif


%description

fish is a shell geared towards interactive use. Its features are
focused on user friendliness and discoverability. The language syntax
is simple but incompatible with other shell languages.


%prep
%setup -q




%build
# The docdir argument is to make the name of the cosumantation
# directory 'fish-VERSION', instead of the default, which is simply
# 'fish'.
%configure docdir=%_datadir/doc/%{name}-%{version}
make %{?_smp_mflags}




%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"

# Find translation files
%find_lang %{name}.\*



%clean
rm -rf $RPM_BUILD_ROOT




%post
# Add fish to the list of allowed shells in /etc/shells
if ! grep %_bindir/fish %_sysconfdir/shells >/dev/null; then
	echo %_bindir/fish >>%_sysconfdir/shells
fi




%postun
# Remove fish from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then
	grep -v %_bindir/fish %_sysconfdir/shells >%_sysconfdir/fish.tmp
	mv %_sysconfdir/fish.tmp %_sysconfdir/shells
fi




%files -f %{name}.\*.lang

%defattr(-,root,root,-)

# The documentation directory
%doc %_datadir/doc/%{name}-%{version}

# man files
%_mandir/man1/fish.1*
%_mandir/man1/fish_pager.1*
%_mandir/man1/fish_indent.1*
%_mandir/man1/fishd.1*
%_mandir/man1/mimedb.1*
%_mandir/man1/set_color.1*

# The program binaries
%attr(0755,root,root) %_bindir/fish
%attr(0755,root,root) %_bindir/fish_indent
%attr(0755,root,root) %_bindir/fish_pager
%attr(0755,root,root) %_bindir/fishd
%attr(0755,root,root) %_bindir/mimedb
%attr(0755,root,root) %_bindir/set_color

# Configuration files
%config %_sysconfdir/fish/config.fish
%dir %_sysconfdir/fish

# Non-configuration initialization files
%dir %_datadir/fish
%_datadir/fish/config.fish

# Program specific tab-completions
%dir %_datadir/fish/completions
%_datadir/fish/completions/*.fish

# Dynamically loaded shellscript functions
%dir %_datadir/fish/functions
%_datadir/fish/functions/*.fish

# Documentation for builtins and shellscript functions
%dir %_datadir/fish/man
%_datadir/fish/man/*.1



%changelog
* Sat Apr 21 2007 Axel Liljencrantz<axel@liljencrantz.se> 1.23.0-0
- Add fish_indent command

* Thu Feb 8 2007 Axel Liljencrantz<axel@liljencrantz.se> 1.22.3-0
- Tell rpm about the help pages in %_datadir/fish/man/

* Sat Oct 14 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.22.0-0
- Update names of various configuration files

* Fri Aug 4 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.21.10-4
- Add better translation finding code from fedora spec to main spec. Thank you to Michael Schwendt.
- Add missing dependency libXext-devel.
- Remove one nesting level from dependency checking code.

* Tue Aug 1 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.21.10-1
- Improved the dependency check for X headers. Thank you to Michael Schwendt for pointers on how to do this

* Mon Jul 31 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.21.10-1
- Fixed spelling and punctuation as a per patch from Paul Howarth
- Fixed dependencies as per patch from Paul Howarth

* Tue Nov 29 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.17.0-0
- 1.17.0

* Sat Sep 24 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.14.0-0
- 1.14.0

* Mon Sep 12 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.4-0
- 1.13.4

* Wed Sep 07 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.3-0
- 1.13.3

* Tue Sep 06 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.2-0
- 1.13.2

* Fri Aug 30 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.1-0
- 1.13.1

* Sun Aug 28 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.0-0
- 1.13.0

* Sat Aug 13 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.0-0
- Add completions subdirectory

* Thu Jul 28 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.12.1-0
- 1.12.1

* Fri Jul 15 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.12.0-1
- 1.12.0

* Thu Jun 30 2005 Michael Schwendt <mschwendt@users.sf.net> 1.11.1-9
- Set CFLAGS the proper way

* Thu Jun 30 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.11.1-8
- Fix revision number in changelog

* Wed Jun 29 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.11.1-7
- Send post-script output to /dev/null

* Wed Jun 29 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.11.1-6
- Add changelog section to spec file
- Add macros to source tags
- Add smp_mflags to 'make all'
- Fix typo in post install scriptlet test
- Set CFLAGS from spec file
