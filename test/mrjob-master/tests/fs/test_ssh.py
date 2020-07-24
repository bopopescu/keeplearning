# Copyright 2009-2012 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from mrjob.fs.ssh import SSHFilesystem
from mrjob import ssh

from tests.fs import MockSubprocessTestCase
from tests.mockssh import main as mock_ssh_main


class SSHFSTestCase(MockSubprocessTestCase):

    def setUp(self):
        super(SSHFSTestCase, self).setUp()
        self.ec2_key_pair_file = self.makefile('key.pem', 'i am an ssh key')
        self.ssh_key_name = 'key_name.pem'
        self.fs = SSHFilesystem(['ssh'], self.ec2_key_pair_file,
                                self.ssh_key_name)
        self.set_up_mock_ssh()
        self.mock_popen(ssh, mock_ssh_main, self.env)

    def set_up_mock_ssh(self):
        self.main_ssh_root = self.makedirs('testmain')
        self.env = dict(
            MOCK_SSH_VERIFY_KEY_FILE='true',
            MOCK_SSH_ROOTS='testmain=%s' % self.main_ssh_root,
        )
        self.ssh_subordinate_roots = []

    def add_subordinate(self):
        subordinate_num = len(self.ssh_subordinate_roots) + 1
        new_dir = self.makedirs('testsubordinate%d' % subordinate_num)
        self.ssh_subordinate_roots.append(new_dir)
        self.env['MOCK_SSH_ROOTS'] += (':testmain!testsubordinate%d=%s'
                                         % (subordinate_num, new_dir))

    def make_main_file(self, path, contents):
        return self.makefile(os.path.join(self.main_ssh_root, path),
                             contents)

    def make_subordinate_file(self, subordinate_num, path, contents):
        return self.makefile(os.path.join('testsubordinate%d' % subordinate_num, path),
                             contents)

    def test_ls_empty(self):
        self.assertEqual(list(self.fs.ls('ssh://testmain/')), [])

    def test_ls_basic(self):
        self.make_main_file('f', 'contents')
        self.assertEqual(list(self.fs.ls('ssh://testmain/')),
                         ['ssh://testmain/f'])

    def test_ls_basic_2(self):
        self.make_main_file('f', 'contents')
        self.make_main_file('f2', 'contents')
        self.assertItemsEqual(list(self.fs.ls('ssh://testmain/')),
                         ['ssh://testmain/f', 'ssh://testmain/f2'])

    def test_ls_recurse(self):
        self.make_main_file('f', 'contents')
        self.make_main_file('d/f2', 'contents')
        self.assertItemsEqual(list(self.fs.ls('ssh://testmain/')),
                         ['ssh://testmain/f', 'ssh://testmain/d/f2'])

    def test_cat_uncompressed(self):
        # mrjob's ssh doesn't support compressed files.
        self.make_main_file(os.path.join('data', 'foo'), 'foo\nfoo\n')
        remote_path = self.fs.path_join('ssh://testmain/data', 'foo')

        self.assertEqual(list(self.fs._cat_file(remote_path)),
                         ['foo\n', 'foo\n'])

    def test_subordinate_cat(self):
        self.add_subordinate()
        self.make_subordinate_file(1, 'f', 'foo\nfoo\n')
        remote_path = 'ssh://testmain!testsubordinate1/f'

        self.assertRaises(IOError, lambda: list(self.fs._cat_file(remote_path)))

        # it is not SSHFilesystem's responsibility to copy the key.
        self.make_main_file(self.ssh_key_name, 'key')
        self.assertEqual(list(self.fs._cat_file(remote_path)), ['foo\n', 'foo\n'])

    def test_subordinate_ls(self):
        self.add_subordinate()
        self.make_subordinate_file(1, 'f', 'foo\nfoo\n')
        remote_path = 'ssh://testmain!testsubordinate1/'

        self.assertRaises(IOError, list, self.fs.ls(remote_path))

        # it is not SSHFilesystem's responsibility to copy the key.
        self.make_main_file(self.ssh_key_name, 'key')
        self.assertEqual(list(self.fs.ls(remote_path)),
                         ['ssh://testmain!testsubordinate1/f'])

    def test_du(self):
        self.make_main_file('f', 'contents')
        # not implemented
        self.assertRaises(IOError, self.fs.du, 'ssh://testmain/f')

    def test_mkdir(self):
        # not implemented
        self.assertRaises(IOError, self.fs.mkdir, 'ssh://testmain/d')

    def test_path_exists_no(self):
        path = 'ssh://testmain/f'
        self.assertEqual(self.fs.path_exists(path), False)

    def test_path_exists_yes(self):
        self.make_main_file('f', 'contents')
        path = 'ssh://testmain/f'
        self.assertEqual(self.fs.path_exists(path), True)

    def test_rm(self):
        self.make_main_file('f', 'contents')
        # not implemented
        self.assertRaises(IOError, self.fs.rm, 'ssh://testmain/f')

    def test_touchz(self):
        # not implemented
        self.assertRaises(IOError, self.fs.touchz, 'ssh://testmain/d')

    def test_md5sum(self):
        # not implemented
        self.assertRaises(IOError, self.fs.md5sum, 'ssh://testmain/d')
