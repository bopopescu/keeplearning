#软件包的名字
Name:           hello
#软件包的主版本号
Version:        2.10
#软件包的次版本号
Release:        1%{?dist}
#软件包简要介绍
Summary:        The "Hello World" program from GUN
Summary(zh_CN): GUN "Hello World" 程序
#授权协议
License:        GPLv3+
#软件源码包的URL地址       
URL:            http://ftp.gnu.org/gnu/hello
#源代码包，默认将在SOURCES目录中寻找
Source0:        %{name}-%{version}.tar.gz
#编译时需要的依赖包
BuildRequires:  gettext
#安装时需要的依赖包
Requires(post): info
Requires(preun): info
#定义临时构建目录，这个地址将作为临时安装目录在后面引用      
BuildRoot:      /tmp/%{name}-%{version}-%{release}-root

#软件包的内容介绍 
%description
The "Hello World" program, done with all bells and whistles of a proper FOSS
project, including configuration, build, internationalization, help files, etc.

%description -l zh_CN
"Hello World"程序, 包含FOSS项目所需的所有部分, 包括配置, 构建, 国际化, 帮助文件等.

#安装前的预操作, 可以使用shell命令, 下面命令表示对SOURCES目录中的源码包进行解包, 解包到BUILD目录中
%prep
%setup -q

#BUILD字段，将通过直接调用源码目录中自动构建工具完成源码编译操作
%build
%configure
make %{?_smp_mflags}

#进行包的安装字段, 可以使用shell命令来进行安装时的操作
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}
rm -f %{buildroot}/%{_infodir}/dir

#安装完成后进行的操作, 可以使用shell命令
%post
install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

#卸载前必须进行的操作, 可以使用shell命令
%preun
if [ $1 = 0 ]; then
  install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

#列出需要打包进RPM包的目录和文件
%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%license COPYING
%{_mandir}/man1/hello.1.*
%{_infodir}/hello.info.*
%{_bindir}/hello

#RPM包的更新日志
%changelog
* Sun Nov 16 2014 The Coon of Ty <Ty@coon.org> - 2.10-1
- Update to 2.10
* Tue Sep 06 2011 The Coon of Ty <Ty@coon.org> - 2.8-1
- Initial version of the package


