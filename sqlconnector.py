import mysql.connector
from difflib import get_close_matches

#storing the connection
conn =''
#list of expressions to crossreference close get_close_matches
expressions=[]

def db_connection():
    """
    Connects to PHPAdmin database set up by course instructor. Database has 2 columns,
    Expressions and definition. Each expressions represents a word in
    the dictionary and has cooresponding defintions.
    """

    con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host="108.167.140.122",
    database = "ardit700_pm1database"
    )
    return con

def query_database(flg, word=None):
    """
    This method opens a cursor object to retrieve defintions for words(flag==1)
    and gathers a list of the expressions(words in dictionary) for the database for close matches.
    """
    cursor=conn.cursor()
    if flg == 1:
        query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word)
    elif flg == 0:
         query = cursor.execute('SELECT DISTINCT EXPRESSION FROM Dictionary')
    return cursor.fetchall()

def matches(word, word_list):
    """
    Function serves to take a word and a list to determine if any words on the list are close matches.
    This uses the get_close_matches function for difflib to generate matches.
    """
    new_word_list = []
    for item in word_list:
        new_word_list.append(item[0])
    matches=get_close_matches(word, new_word_list)
    return matches

def dictionary_sql(word):
    """
    Querys database for word. If no results are found, will try and find matches for expressions
    list.
    """
    result = query_database(1, word)

    if len(result)==0:
        close_words = ", ". join(matches(word, expressions))
        result = f'Did you mean \n{close_words}. \nEnter a word from the list or choose another word:  '
        # if yn != None:
        #     result = query_database(1, yn)

    return result

def user_input():
    """
    Continuously takes user input of words.

    """
    while True:
        try:
            word = input("Please enter a word for a definition or press CTRL+C to exit program:  ")
            results = dictionary_sql(word)
        except ValueError:
            print('The word is not valid or contains invalid characters')
            continue
        except EOFError:
            print("Thank you for using Dictionary")
            break
        else:
            if results:
                for result in results:
                    print(result)
            else:
                print('Word not Found')

conn = db_connection()
expressions=query_database(0, None)
# user_input()
