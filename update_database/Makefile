.PHONY: update-university-list

# if you are using Windows, please change 'python3' to 'python'
PYTHON = python

update-university-list: country-info.csv

normalize_authors.csv unnormalize_authors.csv:
	@echo "Gathering authors."
	$(PYTHON) ./author_gather.py

enged-country-info-full-new.csv: normalize_authors.csv unnormalize_authors.csv 
	@echo "Matching complemented authors."
	$(PYTHON) ./author_match1.py
	$(PYTHON) ./author_match2.py
	@echo "Complementing university list."
	$(PYTHON) ./university_complement.py
	$(PYTHON) ./concatenate.py
	@echo "Matching authors again."
	$(PYTHON) ./author_match1.py
	$(PYTHON) ./author_match2.py
	@echo "Complement Done."
	
country-info.csv: enged-country-info-full-new.csv
	$(PYTHON) ./filter_american_schools.py
	mv enged-country-info-full-new.csv enged-country-info-full.csv
	rm -rf normalize_authors.csv
	rm -rf unnormalize_authors.csv


