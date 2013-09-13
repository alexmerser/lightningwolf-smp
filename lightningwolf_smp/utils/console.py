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
        username = arguments['<username>']
        valid_username = False
        while not valid_username:
            if not is_unique_user(username):
                print "This username %s is not unique in system. Try again" % username
                username = raw_input(prompt)
            else:
                valid_username = True

        print "Unique e-mail address"
        valid_email = False
        while not valid_email:
            email = raw_input(prompt)
            if not is_valid_email(email):
                print "This e-mail: %s is not valid. Try again" % email
            else:
                if not is_unique_email(email):
                    print "This e-mail: %s is not unique in system. Try again" % email
                else:
                    valid_email = True

        password = getpass.getpass()

        user_return = create_user(
            username=username,
            email=email,
            password=password,
            credential='user',
            cli=True
        )

        if user_return is True:
            print "User created"
        else:
            print user_return

