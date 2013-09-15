#!/bin/sh
pybabel extract -F babel.cfg -k gettext -k ngettext -k lazy_gettext -o messages.pot --project lightningwolf-smp ../lightningwolf_smp
