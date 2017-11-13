"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this 
          user is following (a list of str)
       
Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)
       
"""

# Write your Twitterverse functions here

def process_data(data_file):
    """(file open for reading) -> Twitterverse dictionary
    
    Percondition: the file is already open for reading.
    
    Read the file and return the data in the Twitterverse dictionary format
    
    Twitterverse Data Dictionary: dict of {str: dict of {str: object}
    Format: (if there is no information, then the object is empty string)
    username: {'name': name,
               'bio': bio,
               'location': location,
               'web': web link,
               'following': following user }
    

    """
    data_dict = {}
    line = ''
    username = data_file.readline().strip()
    while username != '':
        
        data_dict[username] = {}
        data_dict[username]['name'] = data_file.readline().strip()
        data_dict[username]['location'] = data_file.readline().strip()
        data_dict[username]['web'] = data_file.readline().strip()
       
        
        bio = ''
        
        while line.strip() != 'ENDBIO':
            line = data_file.readline()
            bio += line
        
        data_dict[username]['bio'] = bio[:-8]
        following = []
        
        while line.strip() != 'END':
            line = data_file.readline()
            following.append(line.strip())
        data_dict[username]['following'] = following[:-1]
        username = data_file.readline().strip()
        
    return data_dict

def process_query(query_file):
    """(file open for reading) -> query dictionary
    
    percondition: File is already open for read.
    
    Read the file and return the query in the query dictionay format.
    
    Query dictionay format: dict of {str: dict of {str: str or list}} 
    Format:{'search': {'username': str, 'operation': list},
            'filter': {str: str'},
            'present':{'sort-by': str, 'format':str}}
    Keyword: 'SEARCH', 'FILTER', PRESENT'
    
    Note:If there is only one line between SEARCH and FILTER, then it represents the username start at, and there are no operations to be performed in the search step.
    
    """
    line = query_file.readlines()
   
    
    query_dict = {'search': {},
                   'filter': {},
                   'present':{}}

    
    for i in range(len(line)):
        
        if line[i].strip() == 'SEARCH':
            
            query_dict['search']['username'] = line[i + 1].strip()
            
            s = i + 1
            
        elif line[i].strip() == 'FILTER':
            f = i
            
            a = []
            
            for item in line[s + 1 : f]:
                a.append(item.strip())
            query_dict['search']['operations'] = a
            
            
                
        elif line[i].strip() == 'PRESENT':
            
            p = i
            exam = line[f + 1 : p]
            
            for item in exam:
                item = item.strip()
                item = item.split()
                
                query_dict['filter'][item[0]] = item[-1]
                
        elif 'sort-by' in line[i]:
            line[i] = line[i].strip()
            sb = line[i].split()
            query_dict['present']['sort-by'] = sb[-1]
            
        elif 'format' in line[i]:
            line[i] = line[i].strip()
            f = line[i].split()
            query_dict['present']['format'] = f[-1]
            
            

    return query_dict
                
                
                
def all_followers(data_dict, username): 
    """(Twitterverse dictionary, str) -> list of str
    
    Identify all the usernames that are following the user and return them as a list.
    
    >>> data_dict = {'NicoleKidman': {'following': [], 'web': '', 'location': 'Oz', 'name': 'Nicole Kidman', 'bio': "At my house celebrating Halloween! I Know Haven't been on like\\nyears So Sorry,Be safe And have fun tonight"}, 'katieH': {'following': [], 'web': 'www.tomkat.com', 'location': '', 'name': 'Katie Holmes', 'bio': ''}, 'PerezHilton': {'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web': 'http://www.PerezH...', 'location': 'Hollywood, California', 'name': 'Perez Hilton', 'bio': 'Perez Hilton is the creator and writer of one of the most famous websites\\nin the world. And he also loves music - a lot!'}, 'tomCruise': {'following': ['katieH', 'NicoleKidman'], 'web': 'http://www.tomcruise.com', 'location': 'Los Angeles, CA', 'name': 'Tom Cruise', 'bio': 'Official TomCruise.com crew tweets. We love you guys!\\nVisit us at Facebook!'}}
    
    >>> result = all_followers(data_dict, 'katieH')
    >>> result.sort()
    >>> result
    ['PerezHilton', 'tomCruise']
    
    >>> all_followers(data_dict, 'PerezHilton')
    []
    
    >>> all_followers(data_dict, 'tomCruise')
    ['PerezHilton']
    
    """
    follow_lst = []
    for user in data_dict:
        
        if username in data_dict[user]['following']:
            
            follow_lst.append(user)
            
    return follow_lst


def get_search_results(data_dict, search_dict):
    """(Twitterverse dictionary, search specification dictionary) -> list of str
    
    Perform the specified search on the given Twitter data, and return a list of strings representing usernames that match the search criteria.
    
    >>> data_dict = {'NicoleKidman': {'following': [], 'web': '', 'location': 'Oz', 'name': 'Nicole Kidman', 'bio': "At my house celebrating Halloween! I Know Haven't been on like\\nyears So Sorry,Be safe And have fun tonight"}, 'katieH': {'following': [], 'web': 'www.tomkat.com', 'location': '', 'name': 'Katie Holmes', 'bio': ''}, 'PerezHilton': {'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web': 'http://www.PerezH...', 'location': 'Hollywood, California', 'name': 'Perez Hilton', 'bio': 'Perez Hilton is the creator and writer of one of the most famous websites\\nin the world. And he also loves music - a lot!'}, 'tomCruise': {'following': ['katieH', 'NicoleKidman'], 'web': 'http://www.tomcruise.com', 'location': 'Los Angeles, CA', 'name': 'Tom Cruise', 'bio': 'Official TomCruise.com crew tweets. We love you guys!\\nVisit us at Facebook!'}}
    
    >>> search_dict = {'username': 'tomCruise', 'operations': ['following']}
    >>> get_search_results(data_dict, search_dict)
    ['katieH', 'NicoleKidman']

    >>> search_dict = {'username': 'tomCruise', 'operations': ['followers', 'following']}
    >>> get_search_results(data_dict, search_dict)
    ['PerezHilton', 'tomCruise', 'katieH', 'NicoleKidman']
    
    >>> search_dict = {'username': 'tomCruise', 'operations': ['followers', 'followers']}
    >>> get_search_results(data_dict, search_dict)
    ['PerezHilton']
    
    """
    user = search_dict['username']
    
    lst = []
    
    for item in search_dict['operations']:
        if lst == []:
        
            if item == 'followers':
            
                for i in all_followers(data_dict, user):
                
                    if i not in lst:
                        lst.append(i)
                    
            elif item == 'following':
            
                for i in data_dict[user]['following']:
                
                    if i not in lst:
                        lst.append(i)
        else:
            for uid in lst:
                if item == 'followers':
                            
                    for i in all_followers(data_dict, uid):
                                
                        if i not in lst:
                            lst.append(i)
                                    
                elif item == 'following':
                            
                    for i in data_dict[uid]['following']:
                                
                        if i not in lst:
                            lst.append(i)                
                    
    
    return lst

def get_filter_results(data_dict, usernames, filter_dict):
    """(Twitterverse dictionary, list of str, filter specification dictionary) -> list of str
    
    Apply the specified filters to the given username list to determine which usernames to keep, and return the resulting list of usernames.
    
    >>> data_dict = {'NicoleKidman': {'following': [], 'web': '', 'location': 'Oz', 'name': 'Nicole Kidman', 'bio': "At my house celebrating Halloween! I Know Haven't been on like\\nyears So Sorry,Be safe And have fun tonight"}, 'katieH': {'following': [], 'web': 'www.tomkat.com', 'location': '', 'name': 'Katie Holmes', 'bio': ''}, 'PerezHilton': {'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web': 'http://www.PerezH...', 'location': 'Hollywood, California', 'name': 'Perez Hilton', 'bio': 'Perez Hilton is the creator and writer of one of the most famous websites\\nin the world. And he also loves music - a lot!'}, 'tomCruise': {'following': ['katieH', 'NicoleKidman'], 'web': 'http://www.tomcruise.com', 'location': 'Los Angeles, CA', 'name': 'Tom Cruise', 'bio': 'Official TomCruise.com crew tweets. We love you guys!\\nVisit us at Facebook!'}}
    
    >>> filter_dict = {'following': 'katieH'} 
    >>> usernames = ['katieH', 'NicoleKidman', 'tomCruise', 'PerezHilton']
    >>> get_filter_results(data_dict, usernames, filter_dict)
    ['tomCruise', 'PerezHilton']
    """
    lst_name = []
    lst_loc = []
    lst_follower = []
    lst_following = []
    for_all = []
    
    for item in filter_dict:
        
            if item == 'name-includes':
                for user in usernames:
                    if filter_dict['name-includes'].lower() in data_dict[user]['username'].lower():
                        lst_name.append(user)
                if user not in lst_name:
                    usernames.remove(user)
                if for_all == []:
                        for_all =lst_name
                else:
                    for item in for_all:
                        if item not in lst_name:
                            for_all.remove(item)
                                
            elif item == 'location-includes':
                for user in usernames:
                    if filter_dict['location-includes'].lower() in data_dict[user]['location'].lower():
                        lst_loc.append(user)
                        
                if user not in lst_loc:
                    usernames.remove(user)
                    if for_all == []:
                        for_all =lst_loc
                    else:
                        for item in for_all:
                            if item not in lst_loc:
                                for_all.remove(item)                    
                
                                
            elif item == 'following':
                username = filter_dict['following']
                #keeps only users who have the provided username in their 'following' list
                #ie: keeps only users who are in the follower list for the provided username
                follower = all_followers(data_dict, username)
                for user in usernames:
                    if user in follower:
                        lst_following.append(user)
                        
                if for_all == []:
                        for_all =lst_following
                else:
                    for item in for_all:
                        if item not in lst_following:
                            for_all.remove(item)   
                                
            elif item == 'follower':
                username = filter_dict['follower']
                # keeps only users who appear in the 'following' list for the provided username.
                for user in usernames:
                    if user in data_file[username]['following']:
                        lst.follower.append(user)
                if user not in lst_follower:
                    usernames.remove(user) 
                    
                if for_all == []:
                    for_all =lst_follower
                else:
                    for item in for_all:
                        if item not in lst_follower:
                            for_all.remove(item)                    
    if for_all == []:
        for_all = usernames
        
    return for_all
            

def get_present_string(data_dict, usernames, present_dict):
    """(Twitterverse dictionary, list of str, presentation specification dictionary) -> str
    
    Format the results for presentation based on the given presentation specification and return the formatted string.
    
    >>> data_dict = {'NicoleKidman': {'following': [], 'web': '', 'location': 'Oz', 'name': 'Nicole Kidman', 'bio': "At my house celebrating Halloween! I Know Haven't been on like\\nyears So Sorry,Be safe And have fun tonight"}, 'katieH': {'following': [], 'web': 'www.tomkat.com', 'location': '', 'name': 'Katie Holmes', 'bio': ''}, 'PerezHilton': {'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web': 'http://www.PerezH...', 'location': 'Hollywood, California', 'name': 'Perez Hilton', 'bio': 'Perez Hilton is the creator and writer of one of the most famous websites\\nin the world. And he also loves music - a lot!'}, 'tomCruise': {'following': ['katieH', 'NicoleKidman'], 'web': 'http://www.tomcruise.com', 'location': 'Los Angeles, CA', 'name': 'Tom Cruise', 'bio': 'Official TomCruise.com crew tweets. We love you guys!\\nVisit us at Facebook!'}}
    
    >>> present_dict = {'format': 'long', 'sort-by': 'username'}
    >>> usernames = ['tomCruise', 'PerezHilton']
    >>> get_present_string(data_dict, usernames, present_dict)
    "----------\\nPerezHilton\\nname: Perez Hilton\\nlocation: Hollywood, California\\nwebsite: http://www.PerezH...\\nbio:\\nPerez Hilton is the creator and writer of one of the most famous websites\\nin the world. And he also loves music - a lot!\\nfollowing: ['tomCruise', 'katieH', 'NicoleKidman']\\n----------\\ntomCruise\\nname: Tom Cruise\\nlocation: Los Angeles, CA\\nwebsite: http://www.tomcruise.com\\nbio:\\nOfficial TomCruise.com crew tweets. We love you guys!\\nVisit us at Facebook!\\nfollowing: ['katieH', 'NicoleKidman']\\n----------\\n"
    """
    present = '----------\n'
    
    if present_dict['sort-by'] == 'username':
        tweet_sort(data_dict, usernames, username_first)
    elif present_dict['sort-by'] == 'name':
        tweet_sort(data_dict, usernames, name_first)
    elif present_dict['sort-by'] == 'popularity':
        tweet_sort(data_dict, usernames, more_popular)
    
    if present_dict['format'] == 'short':
        return str(usernames)
    elif present_dict['format'] == 'long':
        for user in usernames:
            present += '{0}\nname: {1}\nlocation: {2}\nwebsite: {3}\nbio:\n{4}\nfollowing: {5}\n----------\n'.format(str(user), str(data_dict[user]['name']), str(data_dict[user]['location']), str(data_dict[user]['web']), str(data_dict[user]['bio']), str(data_dict[user]['following']))
            
    return present


# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType
    
    Sort the results list using the comparison function cmp and the data in 
    twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """
    
    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1 
        results[position] = current  
            
def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return -1 if user a has more followers than user b, 1 if fewer followers, 
    and the result of sorting by username if they have the same, based on the 
    data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """
    
    a_popularity = len(all_followers(twitter_data, a)) 
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)
    
def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return 1 if user a has a username that comes after user b's username 
    alphabetically, -1 if user a's username comes before user b's username, 
    and 0 if a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """
    
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
        
    Return 1 if user a's name comes after user b's name alphabetically, 
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """
    
    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)       

if __name__ == '__main__':
    import doctest
    doctest.testmod()