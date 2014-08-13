#!/usr/bin/python

import os, fnmatch, re, glob, shutil, logging, sqlobject
from imdb import IMDb
from imdb import helpers
import happy_home
import media

#setting for writing to logs
logger = logging.getLogger('happyhome')
hdlr = logging.FileHandler('/home/aiden/python/udacity_project/happyhome/happyhome.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
#set your log level for the console
logging.basicConfig(level=logging.INFO)

library='/home/aiden/python/udacity_project/happyhome/Library'
#library='/home/aiden/python/udacity_project/happyhome/Testlib'

#===============================================================
# Code:

def chk_for_R(mpaa, title, file_loc):
    logger.info('Checking to see if the film (' + title + ') complies with moral code...')
    if "Rated R" in mpaa and "language" in mpaa:
        logger.warn('1/2 Failed moral code check!. ' + title + " is an R-Rated Film, with bad language!" + str(mpaa))
        logger.warn("Deleting " + title + " from " + file_loc)
        os.remove(file_loc)
    else:
        logger.info('1/2 Passed moral code combination (R-rated+bad Language) -> ' + mpaa)
    if "Rated PG-13" in mpaa and "language" in mpaa:
        logger.warn('2/2 Failed moral code check!. ' + title + " is PG-13 Rated BUT contains bad language! " + mpaa)
        logger.warn("Deleting " + title + " from " + file_loc)
        os.remove(file_loc)
    else:
        logger.info('2/2 Passed moral code combination (Naughty PG-13+bad Language) -> ' + mpaa)
        
def set_movie_params(ti,dict_param):
    try:  #get TITLE
        ti['title']
    except KeyError:
        dict_param['title'] = 'None'
    else:
        dict_param['title'] = ti['title']

    try:  #get YEAR
        ti['year']
    except KeyError:
        dict_param['year'] = 'None'
    else:
        dict_param['year'] = ti['year']

    try:  #get MPAA
        ti['mpaa']
    except KeyError:
        dict_param['mpaa'] = 'None'
    else:
        dict_param['mpaa'] = ti['mpaa']

    try:  #get RATING
        ti['rating']
    except KeyError:
        dict_param['rating'] = 'None'
    else:
        dict_param['rating'] = ti['rating']

    try:  #get KIND
        ti['kind']
    except KeyError:
        dict_param['kind'] = 'None'
    else:
        dict_param['kind'] = ti['kind']

    try:  #get DIRECTOR
        ti['director'][0]
    except KeyError:
        dict_param['director'] = 'None'
    else:
        dict_param['director'] = ti['director']

    try:  #get GENRES
        ti['genres']
    except KeyError:
        dict_param['genres'] = 'None'
    else:
        dict_param['genres'] = ti['genres']

    try:  #get RUNTIME
        ti['runtimes']
    except KeyError:
        dict_param['runtime'] = 'None'
    else:
        dict_param['runtime'] = ti['runtimes'][0]

    try:  #get LANGUAGE
        ti['languages'][0]
    except KeyError:
        dict_param['language'] = 'None'
    else:
        dict_param['runtime'] = ti['languages'][0]
        
    try:  #get PLOT
        ti['plot'][0]
    except KeyError:
        dict_param['plot'] = 'None'
    else:
        dict_param['plot'] = ti['plot'][0]    

    return dict_param
    
def init_check(init):
    if init == 19:
        logger.info('Exhausted possible film matches...')
    else:
        logger.info('Trying next film in result list. init = ' + str(init))
        
def query_movie_name(file_title, file_year, file_loc):
    dict_param = {}
    global i
    i = IMDb('sql', uri='mysql://root:f4tb33@localhost/imdb')
    resList = i.search_movie(file_title) #returns a ist of 20 possible films
    logging.debug(('===>resList ---> ', resList))
    init = 0
    for result in resList:
        ti = resList[init]  # working with film in position {init}
        init = init + 1
        i.update(ti)        # get all film properties for film ti
        
        # Pull out some properties that are needed for checking(imdb_mpaa, imdb_genres, imdb_year)
        try:                
            pre_mpaa = ti['mpaa']
        except KeyError:
            pre_mpaa='None'
        try:                
            pre_genreList = ti['genres']
        except KeyError:
            logger.info(('No Genre Found for Film - ' + str(ti.movieID)))
            pre_genreList = ['None']
        try:                
            pre_imdb_year = ti['year']
        except KeyError:
            logger.info(('No Year Found for Film - ' + str(ti.movieID)))
            pre_imdb_year = ['']
            
        # If any of these match, then the file can't be processed
        if 'Short' in pre_genreList:
            logger.info('Skipping as this is a short Film! ' + str(ti.movieID) + ". Trying next film in result list. init = " + str(init))
            init_check(init)

        
        # Main Logic
        if file_year == '' and ti['kind'] == 'movie':
            logging.debug('============================')
            logging.debug(('Film Name ===> ',ti['title']))
            logging.debug(('Type Needs===> ','movie'))
            logging.debug(('Type Recvd===> ',ti['kind']))
            logging.debug('============================')
            logger.info('MATCH FOUND!')
            logging.debug(('===> MATCH FOUND!. ID ', ti.movieID))
            logger.info('Setting parameters for Film - ' + str(ti['title']))
            set_movie_params(ti,dict_param)
            print(dict_param.items())
            if dict_param['mpaa'] == 'None':
                logger.info("Can't Check against moral code because there is no MPAA rating for this film")
                break
            else:
                chk_for_R(dict_param['mpaa'],dict_param['title'], file_loc )
                break
        elif file_year != '' and ti['kind'] == 'movie' and str(pre_imdb_year) == str(file_year):
            if int(file_year) < 2000:
                logger.info('This version does not support films older than year 2000!')
                break
            logging.debug('============================')
            logging.debug(('Film Name ===> ',ti['title']))
            logging.debug(('Type Needs===> ','movie'))
            logging.debug(('Type Recvd===> ',ti['kind']))
            logging.debug(('Year Needs===> ',str(file_year)))
            logging.debug(('Year Recvd===> ',pre_imdb_year))
            logging.debug('============================')
            logger.info('MATCH FOUND!')
            logging.debug(('===> MATCH FOUND!. ID ', ti.movieID))
            logger.info('Setting parameters for Film - ' + str(ti['title']))
            set_movie_params(ti,dict_param)
            print(dict_param.items())
            if dict_param['mpaa'] == 'None':
                logger.info("Can't Check against moral code because there is no MPAA rating for this film")
                break
            else:
                chk_for_R(dict_param['mpaa'],dict_param['title'], file_loc )
                break
        else:
            logger.info('Film ' + str(ti.movieID) + ' not matched! Reason : '  + " (" + ti['kind'] + ") " + ' != (movie) OR ' + str(pre_imdb_year) + " != " + str(file_year) + ". Trying next film in result list. init = " + str(init))
    




def get_files(ftype):
    list_of_files = [] # create a blank list that will become iterable
    for root , dirs, files in os.walk(library):
        for file in files:
            if file.endswith("." + ftype):
                list_of_files.append(os.path.join(root, file))
    logger.info('================================================================')
    logger.info('Found ' + str(len(list_of_files)) + ' files that match file type ' + ftype)
    logger.info('================================================================')
    # Cycle through the files
    for filename in list_of_files:
        logger.info('Working with file :' + filename)
        # First filter out any sample files
        sample=re.match('.*(?i)sample.*',filename)
        if sample:
            logger.warn("This is a sample file. Deleting file " + filename)
            os.remove(filename) # Remove sample files, then go to the next file
            logger.info('__________________________________________________________________')
            continue
        # Extract Film name and year from the given filename using the first REGEX
        movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?(\w*)' + ftype + "$",filename)
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
            #Submit Film name and year to be queries from the local IMDB
            query_movie_name(clean_txt3mov, clean_txt2year, movie.group(0))
            logger.info('____________________finished______________________________________________')
        else:
            # Extract just the Film name from the given filename using the second REGEX
            movie=re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).' + ftype + "$",filename)
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
                #Submit Film name and year to be queries from the local IMDB
                query_movie_name(clean_txt3mov, clean_txt2year,movie.group(0))
                logger.info('__________________________________________________________________')
            else:
                logger.info('Cannot match the file name to any regular expression! Filename : ' + str(filename))
                logger.info('__________________________________________________________________')


def main ():
    logger.info('----------------------Starting happyhome----------------------')
    file_types = ['mp4', 'mkv', 'avi']
    for ft in file_types:
        logger.info('Checking for films with the extension :' + ft)
        get_files(ft)
    logger.info('----------------------You have a happy home now----------------------')

main()
