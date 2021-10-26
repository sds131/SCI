if 'University of California' in item:
    if item == 'University of California' or item == 'The University of California':
        new_item = item
        for temp in range(iter + 1, len(temp_split)):
            campus_name = temp_split[temp]
            if campus_name in uc_names:
                new_item =  item + ' - ' + campus_name
                break
            if 'LA' in campus_name:
                new_item =  item + ' - ' + 'Los Angeles'
                break
            if 'Barrows Hall' in campus_name:
                new_item =  item + ' - ' + 'Berkeley'
                break
    elif 'University of California at' in item:
        new_item = 'University of California' + ' - ' + item[len('University of California at '):]
    elif item == 'University of California - Department of Sociology':
        new_item = 'University of California' + ' - ' + 'Berkeley'
    elif 'University of California -' in item:
        new_item = item
    else:
        new_item = 'University of California' + ' - ' + item[len('University of California '):]
elif 'Maryland' in item:
    new_item = 'University of Maryland - College Park'
else:
    new_item = item
if "Stanford" in new_item:
    new_item = 'Stanford University'
if 'Max-Planck' in new_item:
    new_item = 'Max-Planck Institute for Informatics'
if 'London School' in new_item:
    new_item = 'London School of Economics and Political Science'
if 'MIT ' in new_item:
    new_item = 'Massachusetts Institute of Technology'
if item == 'UC Berkeley':
    new_item = 'University of California - Berkeley'
if item == 'Telefonica Research':
    new_item = 'Telefónica Research'
if 'Johns Hopkins' in item:
    new_item = 'Johns Hopkins University'
if item == 'IIIT-Delhi':
    new_item = 'IIIT Delhi'
if 'Leibniz Institute' in item:
    new_item = 'GESIS - Leibniz Institute for the Social Sciences'
if 'Erasmus University' in item:
    new_item = 'Erasmus University Rotterdam',
if 'China University of Petroleum' in item: 
    new_item = 'China University of Petroleum (Huadong)'
if item == 'Beijing University':
    new_item = 'Peking University'
if 'University of Illinois' in item:
    if 'Champaign' in item:
        new_item = 'University of Illinois at Urbana-Champaign'
    elif 'Chicago' in item:
        new_item = 'University of Illinois at Chicago'
    else:
        for temp in range(iter + 1, len(temp_split)):
            campus_name = temp_split[temp]
            if 'Champaign' in campus_name:
                new_item = 'University of Illinois at Urbana-Champaign'
                break
            if 'Chicago' in campus_name:
                new_item = 'University of Illinois at Chicago'
                break
if 'University of Paris – Dauphine' in item:
    new_item = 'University of Paris - Dauphine'
if 'Université du Québec À' in item:
    new_item = 'Université du Québec à Montréal'
if 'Universidade Federal de Pernambuco' == item:
    new_item = 'Universidade Federal Rural de Pernambuco'
if 'National University of Defence Technology' == item:
    new_item = 'National University of Defense Technology'
if 'Ludwig-Maximilians-University' == item or 'Ludwigs-Maximilians-Universität München' == item:
    new_item = 'LMU Munich'
if 'ISPA– Instituto Universitário' == item:
    new_item = 'ISPA- Instituto Universitário de Ciências Psicológicas'
if 'VU University' in item:
    new_item = 'VU Amsterdam'
if 'University of Hawai’i at Mānoa' == item:
    new_item = 'University of Hawaii at Manoa'
if 'ETH ' in item:
    new_item = 'ETH Zurich'
if 'université de caen' == item:
    new_item = 'Université de Caen'