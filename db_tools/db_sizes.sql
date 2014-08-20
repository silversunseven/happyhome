use imdb
select TABLE_NAME, TABLE_ROWS from `information_schema`.`tables` where `table_schema`= 'imdb' order by TABLE_ROWS DESC;
