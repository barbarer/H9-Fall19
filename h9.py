import unittest
import sqlite3
import json
import os

# 
# Name:
# Who did you work with:
#

def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCateogriesTable(data, cur, conn):
    category_list = []
    for business in data['businesses']:
        business_categories = business['categories']
        for category in business_categories:
            if category['title'] not in category_list:
                category_list.append(category['title'])

    cur.execute("DROP TABLE IF EXISTS Categories")
    cur.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(category_list)):
        cur.execute("INSERT INTO Categories (id,title) VALUES (?,?)",(i,category_list[i]))
    conn.commit()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ DO NOT CHANGE THE CODE ABOVE THIS LINE +++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# [TASK 1]: setUpRestaurantTable() function
# The function takes three arguments as input: the JSON object, the database cursor, and database connection object.
# It loads all of the businesses in the JSON object into a table called Restaurants. The function does not return anything.
# The table should have the following columns:
## restaurant_id (datatype: integer; primary key)
## name (datatype: text)
## address (datatype: text)
## zip (datatype: text)
## category_id (datatype: integer)
## rating (datatype: real)
def setUpRestaurantTable(data, cur, conn):
    pass


# [TASK 2]: getRestaurantsInZipcode() function
# The function takes three arguments as input: the zipcode, the database cursor, and database connection object.
# It selects all the restaurants listed in a particular zipcode and returns a list of tuples.
# Each tuple contains the restaurant name and address
def getRestaurantsInZipcode(zipcode, cur, conn):
    pass

# [TASK 3]: getRestaurantsAboveRating() function
# The function takes three arguments as input: the rating value, the database cursor, and database connection object.
# It selects all the restaurants with a rating greater than or equal to the rating passed to the function and returns a list of tuples.
# The list is sorted by highest rating and each tuple in the list contains the restaurant name, address, zipcode, and rating.
def getRestaurantsAboveRating(rating, cur, conn):
    pass

# [TASK 4]: getRestaurantsAndCategories() function
# The function takes two arguments as input: the database cursor and database connection object.
# It returns a list of all the restaurant names and their categories.
# Note: You will have to use JOIN for this task
def getRestaurantsAndCategories(cur, conn):
    pass

# [EXTRA CREDIT]: setUpCategoryCountTable() function
# The function takes two arguments as input: the database cursor and the database connection object.
# It creates a table CategoryCount with two columns:
## cateogry_title (datatype: text; primary key): This column holds the title of the category (e.g. Bakeries, Pubs, Pizza, etc)
## count (datatype: integer): This column holds the count of total restaurants belonging to that category
# The function does not return anything
# NOTE: You have to use JOIN for this task to get the Categories of all the restaurants
def setUpCategoryCountTable(cur, conn):
     pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ DO NOT CHANGE THE CODE BELOW THIS LINE +++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect('restaurants.db')
        self.cur = self.conn.cursor()
        self.data = readDataFromFile('yelp_data.txt')

    def test_businesses_table(self):
        self.cur.execute('SELECT * from Restaurants')
        resturant_list = self.cur.fetchall()
        self.assertEqual(len(resturant_list), 50)
        self.assertEqual(len(resturant_list[0]),6)
        self.assertIs(type(resturant_list[0][0]), str)
        self.assertIs(type(resturant_list[0][1]), str)
        self.assertIs(type(resturant_list[0][2]), str)
        self.assertIs(type(resturant_list[0][3]), str)
        self.assertIs(type(resturant_list[0][4]), int)
        self.assertIs(type(resturant_list[0][5]), float)

    def test_restaurants_in_zipcode(self):
        self.assertEqual(len(getRestaurantsInZipcode('48104', self.cur, self.conn)),28)
        self.assertEqual(len(getRestaurantsInZipcode('48104', self.cur, self.conn)[0]),2)

    def test_restaurants_rating(self):
        self.assertEqual(len(getRestaurantsAboveRating(5.0, self.cur, self.conn)),1)
        self.assertEqual(len(getRestaurantsAboveRating(3.0, self.cur, self.conn)),50)
        self.assertEqual(len(getRestaurantsAboveRating(3.0, self.cur, self.conn)[0]),4)
        self.assertEqual(getRestaurantsAboveRating(3.0, self.cur, self.conn)[0][3],5.0)
        self.assertEqual(getRestaurantsAboveRating(3.0, self.cur, self.conn)[49][3],3.0)

    def test_restaurants_in_category(self):
        self.assertEqual(len(getRestaurantsAndCategories(self.cur, self.conn)),50)
        self.assertEqual(sorted(getRestaurantsAndCategories(self.cur, self.conn), reverse=True)[0][0], "Zingerman's Delicatessen")

    def test_categorycount_table(self):
        self.cur.execute('SELECT * from CategoryCount')
        category_count_list = self.cur.fetchall()
        self.assertEqual(len(category_count_list),18)
        self.assertIs(type(category_count_list[0][0]), str)
        self.assertIs(type(category_count_list[0][1]), int)
        self.assertEqual(sorted(category_count_list)[0][0],"American (New)")
        self.assertEqual(sorted(category_count_list, key=lambda x:x[1], reverse=True)[0][1],20)

def main():
    json_data = readDataFromFile('yelp_data.txt')
    cur, conn = setUpDatabase('restaurants.db')
    setUpCateogriesTable(json_data, cur, conn)
    setUpRestaurantTable(json_data, cur, conn)

    zipcode = '48198'
    print("Displaying restuarants in the zipcode {}".format(zipcode))
    if getRestaurantsInZipcode(zipcode, cur, conn):
        for r in getRestaurantsInZipcode(zipcode, cur, conn):
            print(r)
        print("\n\n")

    rating = 4.0
    print("Displaying restuarants with rating {} and above".format(str(rating)))
    if getRestaurantsAboveRating(rating, cur, conn):
        for r in getRestaurantsAboveRating(rating, cur, conn):
            print(r)
        print("\n\n")

    if getRestaurantsAndCategories(cur, conn):
        print("Displaying restuarants with their categories")
        for r in getRestaurantsAndCategories(cur, conn):
            print(r)
        print("\n\n")

    setUpCategoryCountTable(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
