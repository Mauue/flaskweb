import pymysql
def set_conditions(form):

    name = ''
    sort_type = ''
    db_score = ''
    imdb_score = ''
    if form['name'] != '':
        name = '(movie_name REGEXP "%s" OR movie_transname REGEXP "%s")' % (pymysql.escape_string(form['name']), pymysql.escape_string(form['name']))

    if 'dbnull' not in form:
        db_score = '((movie_dbscore IS NOT NULL)'
        if form['dbscore1'] == '' and form['dbscore2'] == '':
            db_score += ')'
        else:
            if form['dbscore1'] == '':
                form['dbscore1'] = 0.0
            if form['dbscore2'] == '':
                form['dbscore2'] = 10.0
            db_score += 'AND(movie_dbscore between %s and %s))' % (pymysql.escape_string(form['dbscore1']), pymysql.escape_string(form['dbscore2']))
    else:
        if form['dbscore1'] == '' and form['dbscore2'] == '':
            pass
        else:
            if form['dbscore1'] == '':
                form['dbscore1'] = 0.0
            if form['dbscore2'] == '':
                form['dbscore2'] = 10.0
            db_score += '((movie_dbscore between %s and %s)OR(movie_dbscore IS NULL))' % (
                pymysql.escape_string(form['dbscore1']), pymysql.escape_string(form['dbscore2']))

    if 'imdbnull' not in form:
        imdb_score = '((movie_imdbscore IS NOT NULL)'
        if form['imdbscore1'] == '' and form['imdbscore2'] == '':
            imdb_score += ')'
        else:
            if form['imdbscore1'] == '': form['imdbscore1'] = 0
            if form['imdbscore2'] == '': form['imdbscore2'] = 10
            imdb_score += 'AND(movie_imdbscore between %s and %s))' % \
                          (pymysql.escape_string(form['imdbscore1']), pymysql.escape_string(form['imdbscore2']))
    else:
        if form['imdbscore1'] == '' and form['imdbscore2'] == '':
            pass
        else:
            if form['imdbscore1'] == '': form['imdbscore1'] = 0
            if form['imdbscore2'] == '': form['imdbscore2'] = 10
            imdb_score += '((movie_imdbscore between %s and %s)OR(movie_imdbscore IS NULL))' % (
                pymysql.escape_string(form['imdbscore1']), pymysql.escape_string(form['imdbscore2']))

    sort_list = ['', 'movie_name', 'movie_name DESC', 'movie_dbscore', 'movie_dbscore DESC', 'movie_imdbscore',
                 'movie_imdbscore DESC']
    if form['sort']!='0':
        sort_type = 'ORDER BY ' + sort_list[int(form['sort'])]

    if name != '' and db_score != '':
        name += ' AND '
    if db_score != '' and imdb_score != '':
        db_score += ' AND '
    print(name + db_score + imdb_score + sort_type)
    if(name==''and db_score==''and imdb_score==''):
        if sort_type=='':
            return ''
        else:
            return sort_type

    else:
        return "WHERE "+name+db_score+imdb_score+sort_type
