#!/usr/bin/env python
# coding=utf8


def parse_arguments(arguments):
    if arguments['init:config']:
        print(arguments)
    if arguments['init:db']:
        from lightningwolf_smp.utils.creator import generate
        generate()
        print "Tables in Database created"
    if arguments['user:create']:
        from lightningwolf_smp.utils.user import create_user
        create_user(
            username=arguments['<username>'],
            email=arguments['<useremail>'],
            password=arguments['<userpass>'],
            credential=arguments['--credential']
        )

        print "User created"

