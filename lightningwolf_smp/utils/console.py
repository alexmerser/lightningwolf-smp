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
        from lightningwolf_smp.utils.user import create_user, is_unique_user, is_valid_email, is_unique_email

        print "Unique e-mail address"
        valid_email = False
        while not valid_email:
            email = raw_input(prompt)
            if not is_valid_email(email):
                print "This e-mail is not valid. Try again"
            else:
                if not is_unique_email(email):
                    print "This e-mail is not unique in system. Try again"
                else:
                    valid_email = True

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

