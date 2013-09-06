#!/usr/bin/env python
# coding=utf8


prompt = '> '


def parse_arguments(arguments):
    if arguments['init:config']:
        print(arguments)
    if arguments['init:db']:
        from lightningwolf_smp.utils.creator import generate
        generate()
        print "Tables in Database created"
    if arguments['user:create']:
        import getpass
        from lightningwolf_smp.utils.user import create_user, is_valid_email

        password = getpass.getpass()

        user_return = create_user(
            username=arguments['<username>'],
            email=arguments['<useremail>'],
            password=password,
            credential=arguments['--credential']
        )

        if user_return is True:
            print "User created"
        else:
            print user_return

