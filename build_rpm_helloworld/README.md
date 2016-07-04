制作RPM包的Hello World!教程
===========================

1. 安装rpmdevtools工具, yum install rpmdevtools. rpmdevtools是rpm包的构建工具
2. 安装rpmlint工具, yum install rpmlint. rpmlint是rpm包配置文件的语法校验工具
3. 执行 rpmdev-setuptree 将在当前用户主目录下创建一个RPM构建根目录结构. 注：如需改变默认位置，可以修改配置文件:~/.rpmmacros中变量_topdir对应的值.
```bash
rpmdev-setuptree
ll ~/rpmbuild/
    .
    ├── BUILD (打包过程中的工作目录)
    ├── BUILDROOT (打包过程中的安装目录, 相当于/, 可以修改)
    ├── RPMS (存放生成的二进制包, 不同硬件平台存放在不同文件夹)
    ├── SOURCES (存放打包资源, 包括源码打包文件和补丁文件等)
    ├── SPECS (存放SPEC文档)
    └── SRPMS (存放生成的源码包)
```
4. 进入SOURCE 目录中. 我们获得了一个 tarball 压缩文件, 源代码包. 
```bash
cp hello-2.10.tar.gz ~/rpmbuild/SOURCES
cd ~/rpmbuild
```
5. 使用rpmdev-newspec命令生成一个新的RPM打包配置文件, vim编辑spec文件, 可以参考目录下已经编辑好的spec文件
```bash
cd ~/rpmbuild/SPECS
rpmdev-newspec hello
vim hello.spec
```
6. 检查spec文件是否是正确的, rpmlint hello.spec
7. spec文件如果没有错误, 就可以进行rpm包的构建了. rpmbuild -ba hello.spec. 构建成功后, BUILDROOT下的目录会自动删除, RPMS目录下可以找到构建好的RPM包
8. 进入RPM目录下, 查看构建好的RPM包. rpm -qpl hello-2.10-1.el7.centos.x86_64.rpm
9. 安装测试. sudo rpm -ivh hello-2.10-1.el7.centos.x86_64.rpm
10. Hello world!
```bash
hello
Hello, world!
```