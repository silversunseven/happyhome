#!/usr/bin/python
# Uses local IMDB to query most of the movie parameters
# Uses TMDB to query the Poster links and Movie Trailers

import os
import re
import logging
import subprocess

import tmdb3
from imdb import IMDb

import HTML


def del_file(filename):
    os.remove(filename)

#subprocess()
p = subprocess.Popen(["uname", "-s"], stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
if 'Linux' in output:
    Path = '/Users/aidenryan/project/happyhome'
    print('this is Linux. Path set to ' + str(Path))
elif 'Darwin' in output:
    Path = '/Users/aidenryan/project/happyhome'
    print('this is mac. Path set to ' + str(Path))
else:
    print('eeek! no clue...Output is : ' + str(
        output) + 'Try run uname -s on your system and validate the output! Exiting...')
    exit(1)

# setting for writing to logs
if os.path.exists(Path + '/happyhome.log'):
    del_file(Path + '/happyhome.log')
logger = logging.getLogger('happyhome')
hdlr = logging.FileHandler(Path + '/happyhome.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
# set your log level for the console
logging.basicConfig(level=logging.INFO)

library = '/Volumes/LaCie/Downloads/Completed'
# library=Path + '/Testlib'


#================================================================================
# Code:

def get_poster_from_tmdb(file_title, file_year):
    logger.info('Getting Poster info from TMDB (' + str(file_title) + ',' + str(file_year) +')')
    result = tmdb3.searchMovie(file_title, year=file_year)
    try:
        tmdbID = result[0].id
    except IndexError:
        movPosterURL = 'None'
        return movPosterURL
    else:
        tmdbID = result[0].id
        try:
            movPosterURL = tmdb3.Movie(tmdbID).poster.geturl()
        except AttributeError:
            movPosterURL = 'None'
            return movPosterURL
        else:
            movPosterURL = tmdb3.Movie(tmdbID).poster.geturl()
            return movPosterURL


def get_trailer_from_tmdb(file_title, file_year):
    logger.info('Getting Trailer info from TMDB (' + str(file_title) + ',' + str(file_year) +')')
    result = tmdb3.searchMovie(file_title, year=file_year)
    try:
        tmdbID = result[0].id
    except IndexError:
        movTrailerURL = 'None'
        return movTrailerURL
    else:
        tmdbID = result[0].id
        movie = tmdb3.Movie(tmdbID)
        try:
            movTrailerURL = movie.youtube_trailers[0].geturl()
        except IndexError:
            movTrailerURL = 'None'
            return movTrailerURL
        except UnicodeEncodeError:
            movTrailerURL = 'None'
        else:
            movTrailerURL = movie.youtube_trailers[0].geturl()
            return movTrailerURL


def chk_for_R(mpaa, title, file_loc, table_data_rating, dict_param):
    logger.info('Checking to see if the film (' + title + ') complies with moral code...')
    if "Rated R" in mpaa and "language" in mpaa or "Rated PG-13" in mpaa and "language" in mpaa:
        logger.warn('1/2 Failed moral code check!. ' + title + " is an R-Rated Film, with bad language!" + str(mpaa))
        logger.warn("Deleting " + title + " from " + file_loc)
        os.remove(file_loc)
    else:
        logger.info('1/2 Passed moral code combination (R-rated+bad Language) -> ' + mpaa)
        logger.info('2/2 Passed moral code combination (Naughty PG-13+bad Language) -> ' + mpaa)
        table_data_rating.append(
            [dict_param['rating'], dict_param['title'], dict_param['poster'], dict_param['year'], dict_param['mpaa'],
             dict_param['plot'], dict_param['genres'], dict_param['runtime'], dict_param['trailer'],
             dict_param['IMDB_query']])


def set_movie_params(ti, dict_param, movTrailerURL, movPosterURL):
    try:  #get TITLE
        ti['title']
    except KeyError:
        dict_param['title'] = 'None'
    else:
        dict_param['title'] = re.sub('[^\040-\176]', '', ti['title'])
    print(dict_param['title'])

    try:  #get YEAR
        ti['year']
    except KeyError:
        dict_param['year'] = 'None'
    else:
        dict_param['year'] = str(ti['year'])
    print(dict_param['year'])

    try:  #get MPAA
        ti['mpaa']
    except KeyError:
        dict_param['mpaa'] = 'None'
    else:
        dict_param['mpaa'] = str(ti['mpaa'])
    print(dict_param['mpaa'])

    try:  #get RATING
        ti['rating']
    except KeyError:
        dict_param['rating'] = 'None'
    else:
        dict_param['rating'] = str(ti['rating'])
    print(dict_param['rating'])

    try:  #get KIND
        ti['kind']
    except KeyError:
        dict_param['kind'] = 'None'
    else:
        dict_param['kind'] = str(ti['kind'])
    print(dict_param['kind'])

    try:  #get DIRECTOR
        ti['director'][0]
    except KeyError:
        dict_param['director'] = 'None'
    else:
        dict_param['director'] = str(ti['director'])

    try:  #get GENRES
        ti['genres']
    except KeyError:
        dict_param['genres'] = 'None'
    else:
        dict_param['genres'] = str(ti['genres'])
    print(dict_param['genres'])

    try:  #get RUNTIME
        ti['runtimes']
    except KeyError:
        dict_param['runtime'] = 'None'
    else:
        dict_param['runtime'] = str(ti['runtimes'][0])
    print(dict_param['runtime'])

    try:  #get LANGUAGE
        ti['languages'][0]
    except KeyError:
        dict_param['languages'] = 'None'
    else:
        dict_param['languages'] = str(ti['languages'][0])
    print(dict_param['runtime'])

    try:  #get PLOT
        ti['plot'][0]
    except KeyError:
        dict_param['plot'] = 'None'
    else:
        #Plot sometims has funny char's so we need to remove them because the html module doesn't like the special utf-8 chars
        dict_param['plot'] = re.sub('[^\040-\176]', '', ti['plot'][0])
    print(dict_param['plot'])

    if movPosterURL == 'None':
        dict_param['poster'] = 'None'
    else:
        dict_param['poster'] = '<a href="' + str(movPosterURL) + '"><img src="' + str(
            movPosterURL) + '" alt="poster" width="100" height="150"></a>'
    print(dict_param['poster'])

    if movTrailerURL == 'None':
        dict_param['trailer'] = 'None'
    else:
        dict_param['trailer'] = '<a href="' + str(
            movTrailerURL) + '"><img src="http://imaginenews.com/wp-content/uploads/2012/04/ICON.jpg" alt="trailer" width="40" height="40"></a>'
    print(dict_param['trailer'])

    dict_param['IMDB_query'] = '<a href="http://www.imdb.com/find?q=' + dict_param['title'] + ' ">IMDB</a> '
    print(dict_param['IMDB_query'])

    logger.info('Dictionary : ' + str(dict_param))
    return dict_param


def init_check(init):
    if init == 19:
        logger.info('Exhausted possible film matches...')
    else:
        logger.info('Trying next film in result list. init = ' + str(init))


def write_rating_html(table_data_rating, dict_param):
    htmlout = open('happy_home_rating.html', 'a')
    htmlcode = HTML.table(sorted(table_data_rating, reverse=True),
                          header_row=['Rating', 'Title', 'Poster', 'Year', 'MPAA', 'Plot', 'Genres', 'Runtime',
                                      'Trailer', 'IMDB'])
    table_data_rating.append(
        [dict_param['rating'], dict_param['title'], dict_param['poster'], dict_param['year'], dict_param['mpaa'],
         dict_param['plot'], dict_param['genres'], dict_param['runtime'], dict_param['trailer'],
         dict_param['IMDB_query']])
    htmlout.write(htmlcode)
    htmlout.close()


def query_movie_name(file_title, file_year, file_loc, table_data_rating, movTrailerURL, movPosterURL, dict_param):
    global i
    i = IMDb('sql', uri='mysql://root:f4tb33@localhost/imdb')
    resList = i.search_movie(file_title)  #returns a ist of 20 possible films
    logging.debug(('===>resList ---> ', resList))
    init = 0
    for result in resList:
        logger.debug('Starting new cycle with ', result)
        ti = resList[init]  # working with film in position {init}
        init = init + 1
        i.update(ti)  # get all film properties for film ti

        # Pull out some properties that are needed for checking(imdb_mpaa, imdb_genres, imdb_year)
        try:
            pre_mpaa = ti['mpaa']
        except KeyError:
            pre_mpaa = 'None'
        try:
            pre_genreList = ti['genres']
        except KeyError:
            logger.info('No Genre Found for Film ')
            pre_genreList = ['None']
        try:
            pre_imdb_year = ti['year']
        except KeyError:
            logger.info('No Year Found for Film ')
            pre_imdb_year = ['']

        # If any of these match, then the file can't be processed
        logger.debug(pre_genreList, ti.movieID, ti['title'])
        if 'Short' in pre_genreList:
            logger.info('Skipping as this is a short Film! ' + str(ti.movieID))
            init_check(init)
            continue

        # Main Logic
        if file_year == '' and ti['kind'] == 'movie':
            logging.info('============================')
            logging.info(('Film Name ===> ', ti['title']))
            logging.info(('Type Needs===> ', 'movie'))
            logging.info(('Type Recvd===> ', ti['kind']))
            logging.info('============================')
            logger.info('MATCH FOUND! file_year == "" and kind == movie')
            logger.info('Setting parameters for Film - ' + re.sub('[^\040-\176]', '', ti['title']))
            set_movie_params(ti, dict_param, movTrailerURL, movPosterURL)
            if dict_param['mpaa'] == 'None':
                logger.info("Can't Check against moral code because there is no MPAA rating for this film")
                break
            else:
                chk_for_R(dict_param['mpaa'], dict_param['title'], file_loc, table_data_rating, dict_param)
                break
        elif file_year != '' and ti['kind'] == 'movie' and str(pre_imdb_year) == str(file_year):
            if int(file_year) < 2000:
                logger.info('This version does not support films older than year 2000!')
                break
            logging.info('============================')
            logging.info(('Film Name ===> ', ti['title']))
            logging.info(('Type Needs===> ', 'movie'))
            logging.info(('Type Recvd===> ', ti['kind']))
            logging.info(('Year Needs===> ', str(file_year)))
            logging.info(('Year Recvd===> ', pre_imdb_year))
            logging.info('============================')
            logger.info(
                'MATCH FOUND! file_year is !< 2000 and != "" and imdb.kind == "movie" and imdb_year = file_year(' + str(
                    file_year) + ')')
            logger.info('Setting parameters for Film - ' + re.sub('[^\040-\176]', '', ti['title']))
            #logger.info('Setting parameters for Film - ' + str(ti['title']))
            set_movie_params(ti, dict_param, movTrailerURL, movPosterURL)
            if dict_param['mpaa'] == 'None':
                logger.info("Can't Check against moral code because there is no MPAA rating for this film")
                table_data_rating.append(
                    [dict_param['rating'], dict_param['title'], dict_param['poster'], dict_param['year'],
                     dict_param['mpaa'], dict_param['plot'], dict_param['genres'], dict_param['runtime'],
                     dict_param['trailer'], dict_param['IMDB_query']], )
                break
            else:
                chk_for_R(dict_param['mpaa'], dict_param['title'], file_loc, table_data_rating, dict_param)
                break
        else:
            logger.info('Film ' + str(ti.movieID) + ' not matched! Reason : ' + " (" + ti[
                'kind'] + ") " + ' != (movie) OR ' + str(pre_imdb_year) + " != " + str(
                file_year) + ". Trying next film in result list. init = " + str(init))


def get_files(ftype, table_data_rating, dict_param):
    # Create or overwrite the output file
    list_of_files = []  # create a blank list that will become iterable
    for root, dirs, files in os.walk(library):
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
        sample = re.match('.*(?i)sample.*', filename)
        if sample:
            logger.warn("This is a sample file. Deleting file " + filename)
            os.remove(filename)  # Remove sample files, then go to the next file
            logger.info('__________________________________________________________________')
            continue
        # Extract Film name and year from the given filename using the first REGEX
        movie = re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).*(2\d\d\d).*(1080p)?|(720p)?(\w*)' + ftype + "$", filename)
        if movie:
            logging.info("===>Matched first")
            logging.info(('===>group 0 ---> ', movie.group(0)))
            logging.info(('===>group 1 ---> ', movie.group(1)))
            logging.info(('===>group 2 ---> ', movie.group(2)))
            logging.info(('===>group 3 ---> ', movie.group(3)))
            clean_txt1year = movie.group(3)
            clean_txt2year = re.sub('[ ]', '', clean_txt1year)
            clean_txt1mov = re.sub('[.]', ' ', movie.group(2))
            clean_txt2mov = re.sub('[_]', ' ', clean_txt1mov)
            clean_txt3mov = re.sub('\d\d\d\d', '', clean_txt2mov)
            logging.debug(('===>clean_txt3mov ---> ', clean_txt3mov))
            logging.debug(('===>clean_txt2year ---> ', clean_txt2year))
            logger.info('Quering the movie \'' + clean_txt3mov + '\' from year ' + clean_txt2year)
            movPosterURL = get_poster_from_tmdb(clean_txt3mov, clean_txt2year)
            movTrailerURL = get_trailer_from_tmdb(clean_txt3mov, clean_txt2year)
            #Submit Film name and year to be queries from the local IMDB
            query_movie_name(clean_txt3mov, clean_txt2year, movie.group(0), table_data_rating, movTrailerURL,
                             movPosterURL, dict_param)
            logger.info('____________________finished______________________________________________')
        else:
            # Extract just the Film name from the given filename using the second REGEX
            movie = re.match('(.*\/)([a-z,A-Z, ,.\-,\w]*).' + ftype + "$", filename)
            if movie:
                logging.info("===>Matched Second")
                logging.info(('===>group 0 ---> ', movie.group(0)))
                logging.info(('===>group 1 ---> ', movie.group(1)))
                logging.info(('===>group 2 ---> ', movie.group(2)))
                clean_txt2year = ''
                clean_txt1mov = re.sub('[.]', ' ', movie.group(2))
                clean_txt2mov = re.sub('[_]', ' ', clean_txt1mov)
                clean_txt3mov = re.sub('\d\d\d\d', '', clean_txt2mov)
                logging.debug(('===>clean_txt3mov ---> ', clean_txt3mov))
                logger.info('Quering the movie \'' + clean_txt3mov + '\'')
                movPosterURL = get_poster_from_tmdb(clean_txt3mov, clean_txt2year)
                movTrailerURL = get_trailer_from_tmdb(clean_txt3mov, clean_txt2year)
                #Submit Film name and year to be queries from the local IMDB
                query_movie_name(clean_txt3mov, clean_txt2year, movie.group(0), table_data_rating, movTrailerURL,
                                 movPosterURL, dict_param)
                logger.info('__________________________________________________________________')
            else:
                logger.error('Cannot match the file name to any regular expression! Filename : ' + str(filename))
                logger.info('__________________________________________________________________')


def main():
    if os.path.exists(Path + '/happy_home_rating.html'):
        del_file(Path + '/happy_home_rating.html')
    table_data_rating = []
    dict_param = {}
    logger.info('----------------------Starting happyhome----------------------')
    logger.info('Initializing TMDB connection...')
    tmdb3.set_key('9211973b8f075528e041a5d0cc19fb40')
    tmdb3.set_cache(engine='file',
                    filename='/tmp/tmdb_cache')  # Cached data is keyed off the request URL, and is currently stored for one hour
    tmdb3.set_locale('en', 'gb')

    file_types = ['mp4', 'mkv', 'avi']
    for ft in file_types:
        logger.info('Checking for films with the extension :' + ft)
        get_files(ft, table_data_rating, dict_param)
    write_rating_html(table_data_rating, dict_param)
    logger.info('----------------------You have a happy home now----------------------')


main()
