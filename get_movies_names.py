#!/usr/bin/python

import os, fnmatch, re, glob, shutil
import sqlobject
from imdb import IMDb
from imdb import helpers
import logging

#setting for writing to logs
logger = logging.getLogger('happyhome')
hdlr = logging.FileHandler('/home/aiden/python/udacity_project/happyhome/happyhome.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
#set your log level for the console
logging.basicConfig(level=logging.WARN)
logging.debug('DEBUG IS TURNED ON')

library='/home/aiden/python/udacity_project/happyhome/Library'
#library='/home/aiden/python/udacity_project/happyhome/Testlib'

def chk_for_R(mpaa, title, file_loc):
    logger.info('Checking to see if the film (' + title + ') complies with moral code...')
    if "Rated R" in mpaa and "language" in mpaa:
        logger.warn('Failed moral code check!. ' + title + " is an R-Rated Film, with bad language!" + str(mpaa))
        logger.warn("Deleting " + title + " from " + file_loc)
        os.remove(file_loc)
    else:
        logger.info('Passed moral code combination (R-rated+bad Language)')
    if "Rated PG-13" in mpaa and "language" in mpaa:
        logger.warn('Failed moral code check!. ' + title + " is PG-13 Rated BUT contains bad language! " + mpaa)
        logger.warn("Deleting " + title + " from " + file_loc)
        os.remove(file_loc)
    else:
        logger.info('Passed moral code combination (Naughty PG-13+bad Language)')
    logger.info('MPAA : ' + mpaa)
    
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
        mpaa='None'
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
        
def query_movie_name(mov, file_year, file_loc):
    global i
    logging.info('test')
    i = IMDb('sql', uri='mysql://root:f4tb33@localhost/imdb')
    resList = i.search_movie(mov)
    logging.debug(('===>resList ---> ', resList))

    init = 0
    for result in resList:
        ti = resList[init]
        i.update(ti)
        try:  #get and set MPAA
            mpaa = ti['mpaa']
        except KeyError:
            mpaa='None'
        try:  #get and set GENRES
            genreList = ti['genres']
        except KeyError:
            logger.info(('No Genre Found for Film - ' + str(ti.movieID)))
            genreList = ['None']
        try:  #get and set YEAR
            imdb_year = ti['year']
        except KeyError:
            logger.info(('No Year Found for Film - ' + str(ti.movieID)))
            imdb_year = ['']
            
        if 'Short' not in genreList:
            if file_year == '':
                if ti['kind'] == 'movie':
                    logging.debug('============================')
                    logging.debug(('Film Name ===> ',ti['title']))
                    logging.debug(('Type Needs===> ','movie'))
                    logging.debug(('Type Recvd===> ',ti['kind']))
                    logging.debug('============================')
                    logger.info('MATCH FOUND!')    
                    logging.debug(('===> MATCH FOUND!. ID ', ti.movieID))
                    logger.info('Setting parameters for Film - ' + str(ti['title']))
                    set_movie_params(ti)
                    if mpaa == 'None':
                        logger.info("Can't Check against moral code beccause there is no MPAA rating for this film")
                        break
                    else:
                        chk_for_R(mpaa,ti['title'], file_loc )
                        break
                else:
                    logger.info('Film ' + str(ti.movieID) + ' not matched! Reason : '  + " (" + ti['kind'] + ") " + ' != (movie)')
                    logger.info('Trying next film in result list.')
                    init = init + 1
            else:
                if int(file_year) < 2000:
                    logger.info('This version does not support films older than year 2000!')
                    break
                if ti['kind'] == 'movie' and str(imdb_year) == str(file_year):
                    logging.debug('============================')
                    logging.debug(('Film Name ===> ',ti['title']))
                    logging.debug(('Type Needs===> ','movie'))
                    logging.debug(('Type Recvd===> ',ti['kind']))
                    logging.debug(('Year Needs===> ',str(file_year)))
                    logging.debug(('Year Recvd===> ',imdb_year))
                    logging.debug('============================')
                    logger.info('MATCH FOUND!')
                    logging.debug(('===> MATCH FOUND!. ID ', ti.movieID))
                    set_movie_params(ti)
                    chk_for_R(mpaa,ti['title'], file_loc )
                    break
                else:
                    logger.info('Film ' + str(ti.movieID) + ' not matched! Reason : '  + ' (' + ti['kind'] + ')' + ' != (movie) || file ' + str(file_year) + ' != ' + str(imdb_year))
                    init = init + 1
        else:
            logger.info('Skipping as this is a short Film! ' + str(ti.movieID) + ". Trying next Film..." )
            init = init + 1
            
    
def get_files(ftype):
    list_of_files = [] # create an iterable list
    for root , dirs, files in os.walk(library):
        for file in files:
            if file.endswith("." + ftype):
                list_of_files.append(os.path.join(root, file))
    logger.info('================================================================')
    logger.info('Found ' + str(len(list_of_files)) + ' files that match file type ' + ft)
    logger.info('================================================================')

    for x in list_of_files:
        logger.info('Working with file :' + x)
        movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?(\w*)' + ftype + "$",x)
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
            logger.info('Quering the movie \'' + clean_txt3mov + '\' from year ' + clean_txt2year)
            query_movie_name(clean_txt3mov, clean_txt2year, movie.group(0))
            logger.info('__________________________________________________________________')
        else:
            movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).' + ftype + "$",x)
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
                logger.info('Quering the movie \'' + clean_txt3mov + '\'')
                query_movie_name(clean_txt3mov, clean_txt2year,movie.group(0))
                logger.info('__________________________________________________________________')
            else:
                print "no match"
                logger.info('__________________________________________________________________')


logger.info('----------------------Starting happyhome----------------------')
file_types = ['mp4', 'mkv', 'avi']
for ft in file_types:
    logger.info('Checking for films with the extension :' + ft)
    get_files(ft)
logger.info('----------------------You have a happy home now----------------------')
