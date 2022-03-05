'''
Branching
1. Ordering Example

Write a program that contains a list of menu items and asks the user what would they like to order.
Then display the customers order. Also display a message thanking them.


'''

# menu = ['hamburger', 'fries', 'chicken sandwich', 'coke', 'water']
# print('Menu: \n','\n'.join(menu))

# print('Menu: \n')

# print('Food: ' + ', '.join(menu[:3]))
# print('Drink: ' + ','.join(menu[-2:]))

# meal = input('What would you like?')
# if meal in menu:
#     print('Customer wants a {}'.format(meal))
# else:
#     print('We do not have that item.')
# drink = input(('What drink would you like?'))
# if drink in menu:
#     print('Customer wants a {}'.format(drink))
# else:
#     print('We do not have that item.')


'''
2 Transportation Example

Write a program that asks the user how far they want to travel. If they want to travel less than 3 miles tell them to walk. 
If they want to travel more than 3 miles but lesss than 300 tell them to drive. If they want to travel 300 + miles tell them to fly. 


'''

# distance = int(input('How far do you need to travel?'))



# if distance < 3:
#     mode_of_transport = 'walking'
# elif distance < 300:
#     mode_of_transport = 'driving'
# else:
#     mode_of_transport = 'flying'

# print('I suggest {} to your desitnation'.format(mode_of_transport))


'''
Nested If
3. Movie Database Example

Write a program that asks the ser what film they want to watch. If the film they chose is in the db, ask their age. If they are old enouhg, then check to see if there are seats.
If there are then display a message to enjoy the film, else display the film is sold out. If they are too young, display they are too young to watch. 
If the movie isnt in the db then display a message that it doesnt exist.


Need to debug

'''


movies = {'titanic': [18, 10], 'jurassic park': [13, 10], 'finding nemo': [3,0],}

movie_choice = input('What film would you like to see ').strip().title()

if movie_choice in movies:
    age = int(input('How old are you? ').strip())

    if age >= movies[movie_choice][0]:
        num_seats_bought = movie_choice[movies][1]

        num_seats = int(input("How many tickets do you want? ")).strip()
        if num_seats < num_seats_bought:
            print('Enjoy your film')
            movies[movie_choice][1] = movies[movie_choice][1] - num_seats
        else:
            print('We dont have enough seats available.')
    else:
        print('You are too young to see this movie.')     
else:
    print('That movie isnt showing!')
