#!/usr/bin/python

import os, fnmatch, re
import sqlobject
from imdb import IMDb
from imdb import helpers
import logging

#set your log level
logging.basicConfig(level=logging.DEBUG)
logging.debug('DEBUG IS TURNED ON')

library='/home/aiden/python/udacity_project/happyhome/Library'
#library='/home/aiden/python/udacity_project/happyhome/Testlib'

def check_results(init, ti):
    ti = resList[init]
    i.update(ti)

def set_movie_params(ti):
    i.update(ti)
    try:  #get TITLE
        ti['title']
    except KeyError:
        print("no title found")
    else:
        title=ti['title']
        print title
        
    try:  #get YEAR
        ti['year']
    except KeyError:
        print("no year found")
    else:
        year=ti['year']
        print year

    try:  #get MPAA
        ti['mpaa']
    except KeyError:
        print("no mpaa found")
    else:
        mpaa=ti['mpaa']
        print mpaa

    try:  #get RATING
        ti['rating']
    except KeyError:
        print("no rating found")
    else:
        rating=ti['rating']
        print rating
                
    try:  #get KIND
        ti['kind']
    except KeyError:
        print("no kind found")
    else:
        kind=ti['kind']

    try:  #get DIRECTOR
        ti['director'][0]
    except KeyError:
        print("no director found")
    else:
        director=ti['director'][0]
        print director
            
    try:  #get GENRES
        ti['genres']
    except KeyError:
        print("no genre found")
    else:
        genres=ti['genres']
        print genres
           
    try:  #get RUNTIME
        ti['runtimes']
    except KeyError:
        print("no runtime found")
    else:
        runtime=ti['runtimes'][0]
        print runtime
          
    try:  #get LANGUAGE
        ti['languages'][0]
    except KeyError:
        print("no language found")
    else:
        language=ti['languages'][0]
        print language
            
    try:  #get PLOT
        ti['plot'][0]
    except KeyError:
        print("no plot found")
    else:
        plot=ti['plot'][0]
        print plot
                
    try:  #get ACTOR0
        ti['cast'][0]
    except KeyError:
        print("no Actor0 found")
    else:
        actor0=ti['cast'][0]
        print actor0
            
    try:  #get ACTOR1
        ti['cast'][1]
    except KeyError:
        print("no Actor1 found")
    except IndexError:
        pass
    else:
        actor1=ti['cast'][1]
        print actor1

    try:  #get ACTOR2
        ti['cast'][2]
    except KeyError:
        print("no Actor2 found")
    except IndexError:
        pass
    else:
        actor2=ti['cast'][2]
        print actor2
            
    try:  #get ACTOR3
        ti['cast'][3]
    except KeyError:
        print("no Actor3 found")
    except IndexError:
        pass
    else:
        actor3=ti['cast'][3]
        print actor3
        
def query_movie_name(mov, file_year):
    global i
    i = IMDb('sql', uri='mysql://root:f4tb33@localhost/imdb')
    resList = i.search_movie(mov)
    logging.debug(('===>resList ---> ', resList))

    init = 0
    for result in resList:
        ti = resList[init]
        i.update(ti)
        try:  #get GENRES
            genreList = ti['genres']
        except KeyError:
            logging.debug(('No Genre Found for Film!', ti.movieID))
            genreList = ['None']
        if 'Short' not in genreList:
            if file_year == '':
                if ti['kind'] == 'movie':
                    logging.debug('============================')
                    logging.debug(('Film Name ===> ',ti['title']))
                    logging.debug(('Type Needs===> ','movie'))
                    logging.debug(('Type Recvd===> ',ti['kind']))
                    logging.debug('============================')
                    logging.debug('MATCH FOUND!')    
                    logging.debug(('===> MATCH FOUND!. ID ', ti.movieID))
                    set_movie_params(ti)
                    break
                else:
                    logging.debug('===>First movie not matched, iterating!')
                    init = init + 1
            else:
                if int(file_year) < 2000:
                    print('This version does not support films older than year 2000!')
                    break
                if ti['kind'] == 'movie' and str(ti['year']) == str(file_year):
                    logging.debug('============================')
                    logging.debug(('Film Name ===> ',ti['title']))
                    logging.debug(('Type Needs===> ','movie'))
                    logging.debug(('Type Recvd===> ',ti['kind']))
                    logging.debug(('Year Needs===> ',str(file_year)))
                    logging.debug(('Year Recvd===> ',ti['year']))
                    logging.debug('============================')
                    logging.debug('MATCH FOUND!')    
                    logging.debug(('===> MATCH FOUND!. ID ', ti.movieID))
                    set_movie_params(ti)
                    break
                else:
                    logging.debug('===>First movie not matched, iterating!')
                    init = init + 1
        else:
            logging.debug(('Skipping as this is a short Film!. Trying next Film', ti.movieID))
            init = init + 1
            


def locate(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)
 
    
#for x in locate("*.avi", library):
    #print x

def get_MKV_files():
    mkv_dict = {}
    mkv_list = locate("*.mkv", library)
    #logging.debug(('===> ####################################List Of Files : ', mkv_list.items()))

    for x in mkv_list:
        print('===>Working with  ---> ', x)
        #movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).*(\d\d\d\d).*.mkv$',x)
        #Matches only movies after year 2000
        #(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?(\w*)mkv$
        #(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?.*mkv$
        movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?(\w*)mkv$',x)
        if movie:
            logging.debug("===>Matched first")
            logging.debug(('===>group 0 ---> ', movie.group(0)))
            logging.debug(('===>group 1 ---> ', movie.group(1)))
            logging.debug(('===>group 2 ---> ', movie.group(2)))
            logging.debug(('===>group 3 ---> ', movie.group(3)))
            clean_txt1year = movie.group(3)
            clean_txt2year = re.sub('[ ]','', clean_txt1year)
            clean_txt1mov = re.sub('[.]',' ', movie.group(2))
            clean_txt2mov = re.sub('[_]',' ', clean_txt1mov)
            clean_txt3mov = re.sub('\d\d\d\d','', clean_txt2mov)
            logging.debug(('===>clean_txt3mov ---> ', clean_txt3mov))
            logging.debug(('===>clean_txt2year ---> ', clean_txt2year))
            query_movie_name(clean_txt3mov, clean_txt2year)
            print("__________________________________________________________________")
        else:
            movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).mkv$',x)
            if movie:
                logging.debug("===>Matched Second")
                logging.debug(('===>group 0 ---> ', movie.group(0)))
                logging.debug(('===>group 1 ---> ', movie.group(1)))
                logging.debug(('===>group 2 ---> ', movie.group(2)))
                clean_txt2year = ''
                clean_txt1mov = re.sub('[.]',' ', movie.group(2))
                clean_txt2mov = re.sub('[_]',' ', clean_txt1mov)
                clean_txt3mov = re.sub('\d\d\d\d','', clean_txt2mov)
                logging.debug(('===>clean_txt3mov ---> ', clean_txt3mov))
                query_movie_name(clean_txt3mov, clean_txt2year)
                mkv_dict[clean_txt3mov] = movie.group(0); # Add new entry
                print("__________________________________________________________________")
            else:
                print "no match"
                print("__________________________________________________________________")

   
def get_AVI_files():
    avi_dict = {}
    avi_list = locate("*.avi", library)
    #logging.debug(('===> ####################################List Of Files : ', avi_list.items()))

    for x in avi_list:
        print('===>Working with  ---> ', x)
        movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?(\w*)avi$',x)
        if movie:
            logging.debug("===>Matched first")
            logging.debug(('===>group 0 ---> ', movie.group(0)))
            logging.debug(('===>group 1 ---> ', movie.group(1)))
            logging.debug(('===>group 2 ---> ', movie.group(2)))
            logging.debug(('===>group 3 ---> ', movie.group(3)))
            clean_txt1year = movie.group(3)
            clean_txt2year = re.sub('[ ]','', clean_txt1year)
            clean_txt1mov = re.sub('[.]',' ', movie.group(2))
            clean_txt2mov = re.sub('[_]',' ', clean_txt1mov)
            clean_txt3mov = re.sub('\d\d\d\d','', clean_txt2mov)
            logging.debug(('===>clean_txt3mov ---> ', clean_txt3mov))
            logging.debug(('===>clean_txt2year ---> ', clean_txt2year))
            query_movie_name(clean_txt3mov, clean_txt2year)
            print("__________________________________________________________________")
        else:
            movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).avi$',x)
            if movie:
                logging.debug("===>Matched Second")
                logging.debug(('===>group 0 ---> ', movie.group(0)))
                logging.debug(('===>group 1 ---> ', movie.group(1)))
                logging.debug(('===>group 2 ---> ', movie.group(2)))
                clean_txt2year = ''
                clean_txt1mov = re.sub('[.]',' ', movie.group(2))
                clean_txt2mov = re.sub('[_]',' ', clean_txt1mov)
                clean_txt3mov = re.sub('\d\d\d\d','', clean_txt2mov)
                logging.debug(('===>clean_txt3mov ---> ', clean_txt3mov))
                query_movie_name(clean_txt3mov, clean_txt2year)
                avi_dict[clean_txt3mov] = movie.group(0); # Add new entry
                print("__________________________________________________________________")
            else:
                print "no match"
                print("__________________________________________________________________")


#get_MKV_files()
get_AVI_files()
