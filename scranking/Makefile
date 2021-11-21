.PHONY: normalize

# if you are using Windows, please change 'python3' to 'python'
PYTHON = python

# do not use this one because you should manually do the normalize step
# normalize: get_authors
# 	@echo "Normalizing authors."
# 	$(PYTHON) ./author_normalize.py 

# get the author infos from the paper urls
get_authors: get_urls
	@echo "Crawling tcss."
	$(PYTHON) ./crawler_tcss.py 
	@echo "Crawling tsc."
	$(PYTHON) ./crawler_tcss.py 
	@echo "Crawling SocNet."
	$(PYTHON) ./crawler_socnet.py 
	@echo "All crawling done."

# get the paper urls from the original dblp sites
get_urls: 
	@echo "Getting URLs."
	$(PYTHON) ./get_urls.py
	@echo "Done."
	



