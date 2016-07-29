'''
- get rid of all -- comment lines
- make the script non case sensitive (force to lowercase?)
- get rid of /* direct */ type statements (use non greedy substitutions)
- substitute \n|\t|\r with spaces
- substitue multiple successive spaces with one space
'''
import re
import pdb


def remove_comments(string):
    '''
        removed sql comments
        example:
            - in:   select * from sometable -- this is a comment
            - out:  select * from sometable
    '''
    return re.sub(r'--[\s|\S]+$', '', string)


def remove_beginning_and_trailing_spaces(string):
    ''' removes spaces at the beginning and end of strings '''
    return re.sub(r'^\s+|\s+$', '', string)


def substitute_tab_newlines_returns(string):
    ''' substitute tabs, newlines, and carriage returns with a space '''
    return re.sub(r'\n|\t|\r', ' ', string)


def remove_vertica_direct_comments(string):
    '''
        removes vertica /* direct */ type comments
        be sure to use non greedy substitutions
    '''
    return re.sub(r'\/\*[\S|\s]+?\*\/', ' ', string)


def remove_multiple_spaces(string):
    return re.sub(r'\s+', ' ', string)


def remove_semicolons(string):
    return re.sub(r'\;', ' ', string)


def add_space_after_string(string):
    ''' adds a space after a string before a ( character. Makes it easier to parse later on '''
    return re.sub(r'(\S)(\)|\()', r'\1 \2', string)


def add_space_before_string(string):
    ''' adds a space before a string before a ( character. Makes it easier to parse later on '''
    return re.sub(r'(\)|\()(\S)', r'\1 \2', string)

def remove_brackets_before_table(string):
    '''
        some views have brackets before the table name. remove those
        example: FROM ((CTG_ANALYTICS.SUB_CUSTOMER_SEGMENT a
    '''
    return re.sub(r'from [\s|\(]+(\S+)', r'from \1', string)

def prepare_sql_statement(string):
    string = remove_comments(string).lower()
    string = remove_brackets_before_table(string)
    string = substitute_tab_newlines_returns(string)
    string = remove_vertica_direct_comments(string)
    string = remove_semicolons(string)
    string = add_space_after_string(string)
    string = add_space_before_string(string)
    string = remove_multiple_spaces(string)
    string = remove_beginning_and_trailing_spaces(string)
    return string


def scan_for_inserts(string):
    results = []
    string = prepare_sql_statement(string)
    matches = re.findall(r'insert into (\S+)', string)

    for m in matches:
            results.append(m)

    return list(set(results))

def scan_for_updates(string):
    results = []
    string = prepare_sql_statement(string)
    matches = re.findall(r'update (\S+)', string)

    for m in matches:
            results.append(m)

    return list(set(results))

def scan_for_froms(string):
    results = []
    string = prepare_sql_statement(string)
    matches = re.findall(r'from (\S+)', string)

    for m in matches:
            results.append(m)

    return list(set(results))

def scan_for_joins(string):
    results = []
    string = prepare_sql_statement(string)
    matches = re.findall(r'join (\S+)', string)

    for m in matches:
            results.append(m)

    return list(set(results))

def test_if_alias_or_table(string):
    m = re.match(r'\<\S+\>|\S+\.\S+', string)
    if m:
        return True
