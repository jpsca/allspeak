
extract:
	pybabel extract -F babel.cfg -o _locale/lucuma.pot lucuma

compile:
	msgfmt.py _locale/en/LC_MESSAGES/lucuma.po -o _locale/en/LC_MESSAGES/lucuma.mo

clean:
	rm -f _locale/lucuma.pot
	rm -f _locale/en/LC_MESSAGES/*.mo
